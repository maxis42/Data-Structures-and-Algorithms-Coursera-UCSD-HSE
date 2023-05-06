# python3
import sys
from collections import defaultdict
from time import sleep


class SuffixArrayMatching:
    """
    Find matches of patterns in text with the help of suffix array.
    """

    def __init__(self, text, alphabet):
        self.text = text
        self._text = self.text + "$"
        self.alphabet = "$" + alphabet
        self.suffix_array = self._build_suffix_array(self._text)
        # print(f"Suffix array: {self.suffix_array}\n")

    def _build_suffix_array(self, text):
        """
        Build suffix array of the string text and
        return a list result of the same length as the text
        such that the value result[i] is the index (0-based)
        in text where the i-th lexicographically smallest
        suffix of text starts.
        """
        order = self._sort_characters(text)
        equiv_class = self._compute_char_equiv_class(text, order)

        cur_len = 1

        while cur_len < len(text):
            order = self._sort_doubled(text, cur_len, order, equiv_class)
            equiv_class = self._update_equiv_classes(order, equiv_class, cur_len)
            cur_len *= 2

        return order

    def _sort_characters(self, text):
        """
        Counting sort.
        """
        counter = defaultdict(list)
        for i, c in enumerate(text):
            counter[c].append(i)

        order = []
        for c in self.alphabet:
            for i in counter[c]:
                order.append(i)

        return order

    def _compute_char_equiv_class(self, text, order):
        equiv_class = [-1 for _ in range(len(text))]

        cur_class = 0
        prev_c = text[order[0]]
        for o in order:
            cur_c = text[o]
            if cur_c != prev_c:
                cur_class += 1
                prev_c = cur_c
            equiv_class[o] = cur_class

        return equiv_class

    @staticmethod
    def _sort_doubled(text, cur_len, order, equiv_class):
        # start indices of the string extended
        # to the left by cur_len positions
        starts = []
        for i in range(len(text)):
            start = (order[i] - cur_len) % len(text)
            starts.append(start)

        # collect all first parts with the same equivalence
        # class preserving the same order as before (stable sort)
        counter = defaultdict(list)
        for i, s in enumerate(starts):
            counter[equiv_class[s]].append(i)

        # unpack counter with indices
        new_order = []
        for eq_cl in range(len(text)):
            if eq_cl not in counter:
                # max equivalence class was excedeed
                break
            for pos in counter[eq_cl]:
                new_order.append(starts[pos])
        return new_order

    def _update_equiv_classes(self, order, equiv_class, cur_len):
        new_equiv_class = [-1 for _ in range(len(order))]
        cur_equiv_class = 0
        new_equiv_class[order[0]] = cur_equiv_class
        for i in range(1, len(order)):
            prev = order[i - 1]
            cur = order[i]
            mid_prev = (prev + cur_len) % len(order)
            mid_cur = (cur + cur_len) % len(order)
            # print(f"prev={prev}, cur={cur}, mid_prev={mid_prev}, mid_cur={mid_cur}")

            if (equiv_class[prev] != equiv_class[cur]) \
                    or (equiv_class[mid_prev] != equiv_class[mid_cur]):
                cur_equiv_class += 1

            new_equiv_class[cur] = cur_equiv_class
        return new_equiv_class

    def find_occurrences(self, pattern):
        # the first index of suffix array where
        # text[suffix_array[index]:] starts with pattern
        # if no such suffix than its possible position
        # use binary search
        min_index = 1
        max_index = len(self._text) - 1

        while min_index < max_index:
            mid_index = (min_index + max_index) // 2

            start_pos = self.suffix_array[mid_index]
            suf_len = min(len(pattern), len(self._text) - start_pos - 1)
            end_pos = start_pos + suf_len
            mid_suffix = self._text[start_pos:end_pos]

            if mid_suffix < pattern:
                min_index = mid_index + 1
            else:
                max_index = mid_index

        start = min_index

        start_pos = self.suffix_array[start]
        suf_len = min(len(pattern), len(self._text) - start_pos - 1)
        end_pos = start_pos + suf_len
        start_suffix = self._text[start_pos:end_pos]
        if start_suffix != pattern:
            # START index suffix doesn't contain pattern
            return set()

        # the first index of suffix array where
        # text[suffix_array[index]:] doesn't start with pattern
        # and text[suffix_array[index]:] > pattern
        # if no such suffix than its possible position
        # use binary search
        max_index = len(self._text)

        while min_index < max_index:
            mid_index = (min_index + max_index) // 2

            start_pos = self.suffix_array[mid_index]
            suf_len = min(len(pattern), len(self._text) - start_pos - 1)
            end_pos = start_pos + suf_len
            mid_suffix = self._text[start_pos:end_pos]

            if mid_suffix <= pattern:
                min_index = mid_index + 1
            else:
                max_index = mid_index

        end = min_index

        # get the result indices
        res = {self.suffix_array[i] for i in range(start, end)}
        return res


def run_test():
    alphabet = "ACGT"

    text = "TCCTCTATGAGATCCTATTCTATGAAACCTTCAGACCAAAATTCTCCGGC"
    patterns = ["CCT", "CAC", "GAG", "CAG", "ATC"]  # 1 8 11 13 27 31

    # text = "ATATATA"
    # patterns = ["ATA", "C", "TATAT"]
    sa = SuffixArrayMatching(text, alphabet)
    occs = set()
    for pattern in patterns:
        print(pattern)
        matches = sa.find_occurrences(pattern)
        print(matches)
        occs = occs.union(matches)
    print(" ".join(map(str, occs)))


def run_algo():
    text = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    alphabet = "ACGT"
    sa = SuffixArrayMatching(text, alphabet)
    occs = set()
    for pattern in patterns:
        matches = sa.find_occurrences(pattern)
        occs = occs.union(matches)
    print(" ".join(map(str, occs)))


if __name__ == "__main__":
    # run_test()
    run_algo()
