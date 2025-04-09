import math
import re

from rapidfuzz import fuzz

common_surnames = ["bhai", "kumar", "rao", "das", "lal", "iyer"]


def soundex(x):
    x = x.lower()
    first_char = x[0]
    temp = x[1:]
    temp = re.sub("[aeiouyhw]", "", temp)
    if len(temp) == 0:
        first_char = first_char + "000"
    if temp:
        temp = re.sub("[bfpv]", "1", temp)
        temp = re.sub("[cgjkqsxz]", "2", temp)
        temp = re.sub("[dt]", "3", temp)
        temp = re.sub("[l]", "4", temp)
        temp = re.sub("[mn]", "5", temp)
        temp = re.sub("[r]", "6", temp)

        temp = [
            x for ind, x in enumerate(temp) if (ind == len(temp) - 1 or (ind + 1 < len(temp) and x != temp[ind + 1]))
        ]
    temp = list(temp)
    if temp and (temp[0] == first_char):
        temp[0] = x[0]
    else:
        temp.insert(0, x[0])
    if len(temp) <= 3:
        temp.append("0")
        temp.append("0")
        temp.append("0")
    temp = temp[0:4]
    temp = "".join(temp)
    return temp


class NameMatchHelper:

    @staticmethod
    def check_input_name_in_website_name(name_1, name_2):
        list_name_split_by_space = name_1.split()

        is_all_words_matching = True
        for word_in_name in list_name_split_by_space:
            if word_in_name not in name_2:
                is_all_words_matching = False
                break

        return is_all_words_matching

    @staticmethod
    def get_unmatched_single_char_scoring(input_unmatched_words, unmatched_words):
        """
        Calculating score for sort names
        e.g. like 'Raj Kapoor and Raj k' or  'Vishwa k and Vishwa Kumar'

        :param input_unmatched_words:
        :param unmatched_words:
        :return:
        """
        try:
            input_unmatched_words.sort()
            unmatched_words.sort()
            single_char_matched_count = 0
            for k, v in enumerate(input_unmatched_words):
                try:
                    if (v == unmatched_words[k][0]) or (unmatched_words[k] == v[0]):
                        single_char_matched_count += 1
                except:
                    pass

            if single_char_matched_count == len(input_unmatched_words):
                return 90
            if single_char_matched_count == 0:
                score_output = 40
            else:
                score_output = 80
            return score_output
        except Exception as err:
            print(f"Exception Error in get_unmatched_single_char_scoring : {err}")
        return 0

    def process_matched_name_with_first_letter_match(self, input_name, emp_name):
        score_output = 0
        input_request_list = input_name.split(" ")
        resp_list = emp_name.split(" ")

        # this is for calculating initials if name containing single chars
        unmatched_words = list(set(resp_list) - set(input_request_list))
        input_unmatched_words = list(set(input_request_list) - set(resp_list))
        unmatched_words.sort()
        input_unmatched_words.sort()
        if len(unmatched_words) == len(input_unmatched_words):
            if len(input_unmatched_words) > 0:
                single_char_scoring = self.get_unmatched_single_char_scoring(input_unmatched_words, unmatched_words)
                # if this single_char_scoring is >=90 then only we want this score
                # otherwise whatever score we got from "calculating_score" is fine
                if single_char_scoring > 80:
                    score_output = single_char_scoring
                else:
                    score_output = 40
            else:
                # No unmatched words
                score_output = 90

        return score_output

    def dg_cv_check_is_matched_for_names(self, input_name, dg_response_name, allow_retry=True):
        is_matched = False
        sort_ratio = fuzz.token_sort_ratio(input_name, dg_response_name)
        set_ratio = fuzz.token_set_ratio(input_name, dg_response_name)
        temp_score = (sort_ratio + set_ratio) / 2
        base_score = 41
        if input_name.replace(" ", "") == dg_response_name.replace(" ", ""):
            return True, 1.0

        # if the (sort ratio + set ratio) // 2 is greater than 80 then check match with the first letter
        if temp_score > 80:
            score_output = self.process_matched_name_with_first_letter_match(
                str(input_name).lower(), str(dg_response_name).lower()
            )

            if score_output == 40 and temp_score < 95:
                update_score = (base_score + temp_score) // 2
                temp_score = update_score

        # after filtering out the input name, there should be something in the company name
        if input_name:
            if temp_score > 80 or dg_response_name.startswith(input_name) or input_name.startswith(dg_response_name):
                is_matched = True

        match_score = round(temp_score / 100, 2)
        if not is_matched and match_score < 0.8 and allow_retry:
            is_matched, match_score = self.dg_cv_check_is_matched_for_names(
                input_name.replace(" ", ""), dg_response_name.replace(" ", ""), False
            )

        if match_score == 1:
            total_num_of_spaces = (input_name.count(" ") + dg_response_name.count(" ")) or 0.256
            space_weight = 0.2 * (input_name.count(" ") / total_num_of_spaces)
            match_score -= space_weight

        return is_matched, round(match_score, 2)

    @staticmethod
    def dg_cv_filter_employer_name(company_name):
        prefix_names = ["limited", "ltd", "ltd.", "private", "pvt", "pvt.", "co", "co.", "company", "pvt.ltd"]

        company_name_list = company_name.split(" ")

        for common_name in prefix_names:
            if common_name in company_name_list:
                company_name = str(company_name).replace(common_name, "").strip()

        return company_name.strip()

    @staticmethod
    def sc000_permute_matched(input_name, dg_response_name):
        """
        calculate score for joined but same names
        e.g. "Jakeerhussain Shaik" and "SHAIK JAKEER HUSSAIN"
        """
        try:
            is_matched = False
            score_output = 0.0
            name1 = input_name
            name2 = dg_response_name
            name1_list = input_name.split()
            name2_list = dg_response_name.split()
            lhs = [x for x in name1_list if x]
            rhs = [x for x in name2_list if x]
            if not len(lhs) - len(rhs):
                return is_matched, score_output
            if len(rhs) > len(lhs):
                lhs = name2_list
                rhs = name1_list
                name1 = " ".join(lhs)
                name2 = " ".join(rhs)
            for i in range(0, len(lhs)):
                if name2.find(lhs[i]) != -1:
                    name2 = name2.replace(lhs[i], "")
                    name1 = name1.replace(lhs[i], "")
            if name2.isspace() and name1.isspace():
                is_matched = True
                score_output = 0.8
                return is_matched, score_output
            if name1.strip() and name2.strip() and soundex(name1.strip()) == soundex(name2.strip()):
                is_matched = True
                score_output = 0.8
                return is_matched, score_output

            return is_matched, score_output

        except Exception as err:
            print(f"Exception happens while score calculation and error is : {err}")

    @staticmethod
    def sc015_permute_match(input_name, dg_response_name):
        """
        Check if each word of name is present in one another - LHS and RHS.
        If exact - return 1
        If not exact -
            Partial Match - return 0.8
            No Match - return 0.0
        """
        try:
            lhs = input_name.split()
            rhs = dg_response_name.split()
            lhs_matches, rhs_matches = [], []
            if input_name == dg_response_name:
                return True, 1.0
            for word in lhs:
                if word in dg_response_name:
                    lhs_matches.append(word)
            for word in rhs:
                if word in input_name:
                    rhs_matches.append(word)
            score_output = 0
            if dg_response_name[:3] == "".join(lhs)[:3] or input_name[:3] == "".join(rhs)[:3]:
                total_word_length = len(lhs) + len(rhs)
                score_output = (len(lhs_matches) + len(rhs_matches)) / total_word_length
            return score_output > 0.5, round(score_output, 1)

        except Exception:
            print("Error occurred in SC015_permute_match")

    def sc012_common_names(self, input_name, dg_response_name):
        """
        calculate score for names with common surnames
        common_names like "bhai", "kumar", "rao"
        eg . "Tushar Parmar" and "Parmar Tusharbhai"
        """
        try:
            is_matched = False
            score_output = 0.0

            name1_list = input_name.split(" ")
            name2_list = dg_response_name.split(" ")

            if len(name2_list) != len(name1_list):
                return is_matched, score_output

            for i in common_surnames:
                if input_name.count(i) - dg_response_name.count(i):
                    is_matched, score_output = self.compare_name(name1_list, name2_list, i)

            return is_matched, score_output

        except Exception as err:
            print(f"Exception happens while score calculation and error is : {err}")

    @staticmethod
    def compare_name(name1_list, name2_list, common_name):
        name1_sorted_list = sorted(name1_list)
        name2_sorted_list = sorted(name2_list)
        is_same = False
        for i in range(0, len(name1_sorted_list)):
            if name1_sorted_list[i] == name2_sorted_list[i]:
                is_same = True
            elif (
                name1_sorted_list[i] + common_name == name2_sorted_list[i]
                or name2_sorted_list[i] + common_name == name1_sorted_list[i]
            ):
                is_same = True
            else:
                is_same = False
                return is_same, 0.0

        return is_same, 0.8

    @staticmethod
    def sc013_initials_check(input_name, response_name):
        """
        Check initials and calculate score.
        """
        try:
            name1_set = set(input_name.split())
            name2_set = set(response_name.split())
            no_match_1 = name1_set - name2_set
            no_match_2 = name2_set - name1_set

            if not no_match_1 or not no_match_2:
                return False, 0.0

            if len(no_match_1) != len(no_match_2):
                return False, 0.5 if name1_set & name2_set else 0.4  # Partial match

            if no_match_1 == name1_set or no_match_2 == name2_set:
                return False, 0.0  # No commonality
            match_count, uncertainties, mismatched = 0, 0, 0
            for word1, word2 in zip(sorted(no_match_1), sorted(no_match_2)):
                if word1[0] == word2[0]:
                    match_count += 1
                    uncertainties += len(word1) == 1 or len(word2) == 1
                else:
                    mismatched += 1
                    break

            if mismatched > 0:
                return False, 0.0

            if match_count >= 2:
                return True, 0.9 if uncertainties <= 1 else 0.8
            return False, 0.5 if uncertainties <= 1 else 0.4

        except Exception as err:
            print(f"Error in sc013_initials_check: {err}")
            return False, 0.0

    @staticmethod
    def sc013_initials_check_v3(input_name, response_name):
        """
        Check initials and calculate score.
        """
        try:
            name1_set = set(input_name.split())
            name2_set = set(response_name.split())
            no_match_1 = name1_set - name2_set
            no_match_2 = name2_set - name1_set
            if not no_match_1 or not no_match_2:
                return False, 0.0

            if len(no_match_1) != len(no_match_2):
                return False, 0.5 if name1_set & name2_set else 0.4  # Partial match

            if no_match_1 == name1_set or no_match_2 == name2_set:
                return False, 0.0  # No commonality

            match_count, uncertainties, mismatched = 0, 0, 0
            for word1, word2 in zip(sorted(no_match_1), sorted(no_match_2)):
                if word1[0:2] == word2[0:2]:
                    match_count += 1
                    uncertainties += len(word1) == 1 or len(word2) == 1
                else:
                    mismatched += 1
                    break

            if mismatched > 0:
                return False, 0.0
            if match_count >= 2:
                return True, 0.9 if uncertainties <= 1 else 0.8
            return False, 0.5 if uncertainties <= 1 else 0.4

        except Exception as err:
            print(f"Error in sc013_initials_check: {err}")
            return False, 0.0

    @staticmethod
    def sc015_word_missing(input_name, response_name):
        """
        Used for cases where 3 word string and 2 word string for match
           e.g.  "Archana Bholaram Gupta"  and "Archana Gupta"
        """
        try:
            is_matched = False
            score_output = 0
            name1_list = input_name.split()
            name2_list = response_name.split()
            if not ((len(name1_list) == 3 and len(name2_list) == 2) or (len(name1_list) == 2 and len(name2_list) == 3)):
                return is_matched, score_output
            if any(len(item) == 1 for item in (name1_list + name2_list)):
                return is_matched, score_output
            no_match_1 = list(set(name1_list) - set(name2_list))
            no_match_2 = list(set(name2_list) - set(name1_list))
            if (len(no_match_1) == 1) and not len(no_match_2) or (len(no_match_2) == 1 and not len(no_match_1)):
                score_output = 0.8
                is_matched = True
            return is_matched, score_output
        except Exception as err:
            print(f"Exception occurs while calculating the score. Error: {err}")

    @staticmethod
    def sc014_soundex_matched(input_name: str, response_name: str):
        """
        Michael RAMKUMAR - Micheal Ramkumar -> 0.8
        """
        try:
            is_matched = False
            score_output = 0.0
            # Split names into lists
            name1_list = input_name.split()
            name2_list = response_name.split()
            # Check if lists are of equal length
            if len(name1_list) != len(name2_list):
                return is_matched, score_output
            # Identify unmatched words
            no_match_1 = list(set(name1_list) - set(name2_list))
            no_match_2 = list(set(name2_list) - set(name1_list))
            # Handle simple cases: No mismatches or mismatched lengths
            if not no_match_1 and not no_match_2:
                return is_matched, score_output
            if len(no_match_1) != len(no_match_2):
                return is_matched, score_output
            if set(no_match_1) == set(name1_list) or set(no_match_2) == set(name2_list):
                return is_matched, score_output
            # Join and sort unmatched names for comparison
            joined_name1 = "".join(sorted(no_match_1))
            joined_name2 = "".join(sorted(no_match_2))
            if joined_name1 not in joined_name2 and joined_name2 not in joined_name1:
                if (
                    soundex(joined_name1) == soundex(joined_name2)
                    and joined_name1.startswith(joined_name2[:1])
                    and joined_name1.startswith(joined_name2[:-1])
                ):
                    is_matched = True
                    score_output = 0.8
            return is_matched, score_output
        except Exception as err:
            print(f"Exception in SC014_soundex_matched for {input_name}, {response_name}: {err}")
            return False, 0.0

    def re001_soundex_unequal_names(self, input_name, response_name, score):
        is_matched = True

        name1_list = input_name.split()
        name2_list = response_name.split()

        if len(name2_list) != len(name1_list):
            return is_matched, score

        no_match_1 = [word for word in name1_list if word not in name2_list]
        no_match_2 = [word for word in name2_list if word not in name1_list]

        full_list1 = no_match_2 + no_match_1
        full_list2 = [x for x in full_list1 if len(x)]

        if not len(full_list2) or full_list2 != full_list1:
            return is_matched, score

        if set(no_match_1) == set(name1_list) or len(no_match_2) != len(no_match_1):
            # check if there is common names in name1_list and name2_list
            return is_matched, score

        if len(no_match_1) > 1 or no_match_1[0][0] != no_match_2[0][0]:
            is_matched = False
            score -= 0.2
            return is_matched, score

        try:
            if soundex(no_match_1[0]) != soundex(no_match_2[0]):
                score -= 0.1
                return False, score
        except:
            pass

        if self.check_only_vowel(no_match_1[0], no_match_2[0]):
            return is_matched, score

        is_matched = False
        if no_match_1[0][:2] == no_match_2[0][:2]:
            score -= 0.1
        else:
            score -= 0.2

        return is_matched, score

    def re002_initials_check(self, input_name, response_name, score):
        is_matched = True

        name1_list = input_name.split()
        name2_list = response_name.split()
        no_match_1 = [word for word in name1_list if word not in name2_list]
        no_match_2 = [word for word in name2_list if word not in name1_list]
        # Perfect match case
        if not no_match_1 and not no_match_2:
            return is_matched, score
        # No overlap case
        if set(name1_list) == set(no_match_1) or set(name2_list) == set(no_match_2):
            return is_matched, score
        # soundex match for longer names
        if len(name1_list) >= 3 or len(name2_list) >= 3:
            joined_name1, joined_name2 = "".join(name1_list), "".join(name2_list)
            if soundex(joined_name1) == soundex(joined_name2):
                if self.check_only_vowel("".join(no_match_1), "".join(no_match_2)):
                    return is_matched, score
                return is_matched, score - 0.1
            return False, score - 0.1
        # Extra word cases
        matched_count = len(name1_list) - len(no_match_1)
        if (no_match_1 and not no_match_2) or (no_match_2 and not no_match_1):
            score = 0.7 if matched_count >= 2 else 0.8
            return is_matched, score
        # Initials match check
        match_count = sum(1 for ele in no_match_1 for word in no_match_2 if ele[0] == word[0])
        if match_count > 0:
            return is_matched, score
        return is_matched, 0.7

    @staticmethod
    def re002_initials_check_v3(self, input_name, response_name, score):
        is_matched = True
        name1_list = input_name.split()
        name2_list = response_name.split()
        no_match_1 = [word for word in name1_list if word not in name2_list]
        no_match_2 = [word for word in name2_list if word not in name1_list]
        # Perfect match case
        if not no_match_1 and not no_match_2:
            return is_matched, score
        if set(name1_list) == set(no_match_1) or set(name2_list) == set(no_match_2):
            return is_matched, score
        # soundex match for longer names
        if len(name1_list) >= 3 or len(name2_list) >= 3:
            joined_name1, joined_name2 = "".join(name1_list), "".join(name2_list)
            if soundex(joined_name1) == soundex(joined_name2):
                if self.check_only_vowel("".join(no_match_1), "".join(no_match_2)):
                    return is_matched, score
                return is_matched, score - 0.1
            return False, score - 0.1
        # Extra word cases
        matched_count = abs(len(name1_list) - len(no_match_1))
        if (no_match_1 and not no_match_2) or (no_match_2 and not no_match_1):
            score = 0.7 if matched_count >= 2 else 0.8
            return is_matched, score
        # Initials match check
        match_count = sum(1 for ele in no_match_1 for word in no_match_2 if ele[0] == word[0])
        if match_count > 0:
            return is_matched, score

        return is_matched, 0.7

    @staticmethod
    def re008_dec_unequal_names(self, input_name, response_name, score):
        is_matched = True
        if score > 0.7:
            if not input_name.startswith(response_name) or not response_name.startswith(input_name):
                score -= 0.1
        return is_matched, score

    @staticmethod
    def check_only_vowel(name1, name2):
        return name1.replace(name2, "") in {"a", "i"} or name2.replace(name1, "") in {"a", "i"}

    @staticmethod
    def re003_two_words_vs_one(input_name: str, response_name: str, score: float):
        """
        Compares two names with multiple words, and adjusts the score based on phonetic similarity
        using the soundex algorithm. If names are phonetically different, a penalty is applied.

        :param input_name: The first name to compare.
        :param response_name: The second name to compare.
        :param score: The current score to adjust based on the comparison.
        :returns: Tuple indicating if names matched and the updated score.
        """
        name1_list = input_name.split()
        name2_list = response_name.split()
        if len(name1_list) == len(name2_list):
            return True, score
        full_name_parts = name1_list + name2_list
        filtered_name_parts = [word for word in full_name_parts if len(word) > 1]
        # If there are no valid parts or the lists don't match, return the current result
        if not filtered_name_parts or filtered_name_parts != full_name_parts:
            return True, score
        # Join both names into single strings for soundex comparison
        joined_input_name = "".join(name1_list)
        joined_response_name = "".join(name2_list)
        try:
            # Compare soundex of the combined names
            if not (joined_input_name in joined_response_name or joined_response_name in joined_input_name) and soundex(
                joined_input_name
            ) != soundex(joined_response_name):
                score -= 0.1  # Apply penalty for mismatch
                return False, score
        except Exception:
            print(f"soundex Exception | name1: {input_name} | name2: {response_name}")

        return True, score

    @staticmethod
    def re005_single_name_soundex(input_name: str, response_name: str, score: float):
        """
        Compare two names using the soundex algorithm and adjust the score.

        :param input_name: The first name to compare.
        :param response_name: The second name to compare.
        :param score: The current score to adjust if names do not match phonetically.
        :returns: Tuple indicating if names matched and the updated score.
        :rtype: tuple(bool, float)
        """
        is_matched = True

        # Split names into words
        name1_list = input_name.split()
        name2_list = response_name.split()

        # Filter out initials (single-character words)
        filtered_name1 = [word for word in name1_list if len(word) > 1]
        filtered_name2 = [word for word in name2_list if len(word) > 1]

        # Only proceed if both names reduce to a single meaningful word
        if len(filtered_name1) != 1 or len(filtered_name2) != 1:
            return is_matched, score

        input_word = filtered_name1[0]
        response_word = filtered_name2[0]

        try:
            # Compare soundex values
            if soundex(input_word) != soundex(response_word):
                is_matched = False
                score -= 0.1
        except Exception:
            print(f"soundex Exception | name1: {input_name} | name2: {response_name}")

        return is_matched, score

    @staticmethod
    def re006_name_gender_check(input_name: str, response_name: str, score: float):
        """
        Checks name match with gender-based suffix handling.
        Examples:
        - 'Praveen' and 'Praveena' -> -0.3 score penalty.
        - 'Selva Kumar' and 'Selva Kumari' -> -0.3 score penalty.
        - 'Rama Krishna' and 'Rama krishnaa' -> No penalty (last-before letter is 'a').
        """
        is_matched = True

        # Split names into words
        name1_list = input_name.split()
        name2_list = response_name.split()

        # Find unique words in each name
        no_match_1 = set(name1_list) - set(name2_list)
        no_match_2 = set(name2_list) - set(name1_list)

        # Check mismatches
        for word1 in no_match_1:
            for word2 in no_match_2:
                if word1 in word2:
                    diff = word2.replace(word1, "")
                    key_word = word2
                elif word2 in word1:
                    diff = word1.replace(word2, "")
                    key_word = word1
                else:
                    continue

                # Apply penalty only for 'a' or 'i' suffix and last-before letter not 'a'
                if diff in {"a", "i"} and (len(key_word) > 1 and key_word[-2] != "a"):
                    is_matched = False
                    score -= 0.3

        return is_matched, score

    @staticmethod
    def re010_is_exact_match(input_name: str, response_name: str, score: float):
        # Early exit if the score is not 1.0
        if not math.isclose(score, 1.0, abs_tol=1e-9):
            return True, score
        name1_list = input_name.split(" ")
        name2_list = response_name.split(" ")
        # If the number of words in both names is equal, no need to compare further
        if len(name1_list) == len(name2_list):
            # Check for first character match of corresponding words
            if all(n1[0] == n2[0] for n1, n2 in zip(name1_list, name2_list)):
                return True, score
        # Calculate the difference between the names
        no_match_1 = set(name1_list) - set(name2_list)
        no_match_2 = set(name2_list) - set(name1_list)
        # If no differences exist, return early
        if not no_match_1 and not no_match_2:
            return True, score
        # If differences exist, reduce the score
        score -= 0.1
        return True, score
