# python3
import sys


class BWMatching:
    def __init__(self, bwt):
        self.bwt = bwt
        self.starts, self.occ_count_before = self._preprocess(self.bwt)

    @staticmethod
    def _preprocess(bwt):
        """
        Preprocess the Burrows-Wheeler Transform (BWT) of some text
        and compute as a result:
          * starts - for each character C in bwt, starts[C] is the first position
              of this character in the sorted array of
              all characters of the text.
          * occ_count_before - for each character C in bwt and each position P in len(bwt) + 1,
              occ_count_before[C][P] is the number of occurrences of character C in bwt
              from position 0 to position P exclusive.
        """
        first_col = sorted(bwt)

        starts = dict()
        unique_chars = set()

        for i in range(len(bwt)):
            char = first_col[i]

            if char not in starts:
                starts[char] = i
                unique_chars.add(char)

        occ_count_before = {char: [0] for char in unique_chars}
        for i in range(len(bwt)):
            cur_char = bwt[i]
            for char in unique_chars:
                value = occ_count_before[char][-1]
                if char == cur_char:
                    value += 1

                occ_count_before[char].append(value)

        # print(f"Starts: {starts}")
        # print(f"Occ. count before: {occ_count_before}")

        return starts, occ_count_before

    def count_occurences(self, pattern):
        """
        Compute the number of occurrences of string pattern in the text
        given only Burrows-Wheeler Transform bwt of the text and additional
        information we get from the preprocessing stage - starts and occ_counts_before.
        """
        num_occ = 0

        top = 0
        bot = len(self.bwt) - 1
        while top <= bot:
            # print(f"Top={top}, bot={bot}")
            if len(pattern):
                char = pattern[-1]
                pattern = pattern[:-1]

                contains_char = False
                for i in range(top, bot + 1):
                    if self.bwt[i] == char:
                        contains_char = True
                        break

                if contains_char:
                    top = self.starts[char] + self.occ_count_before[char][top]
                    bot = self.starts[char] + self.occ_count_before[char][bot + 1] - 1
                else:
                    break
            else:
                num_occ = bot - top + 1
                break

        return num_occ


def run_test():
    bwt = "ATT$AA"
    # bwt = "SMNPBNNAAAAA$A"
    # GGTTCACAAGCGAGTTCATATACTAATACCTCTTCCTGACTCCATCAACT$
    bwt = "TCCTCTATGAGATCCTATTCTATGAAACCTTCA$GACCAAAATTCTCCGGC"
    # bwt = "G$"
    # patterns = ["ATA", "A"]
    patterns = ["CCT", "CAC", "GAG", "CAG", "ATC"]
    # patterns = ["T", "G"]
    bwm = BWMatching(bwt)
    occurrence_counts = []
    for pattern in patterns:
        # print(f"Pattern: {pattern}")
        num_occurrences = bwm.count_occurences(pattern)
        occurrence_counts.append(num_occurrences)
    print(" ".join(map(str, occurrence_counts)))


def run_algo():
    bwt = sys.stdin.readline().strip()
    pattern_count = int(sys.stdin.readline().strip())
    patterns = sys.stdin.readline().strip().split()
    # Preprocess the BWT once to get starts and occ_count_before.
    # For each pattern, we will then use these precomputed values and
    # spend only O(|pattern|) to find all occurrences of the pattern
    # in the text instead of O(|pattern| + |text|).
    bwm = BWMatching(bwt)
    occurrence_counts = []
    for pattern in patterns:
        num_occurrences = bwm.count_occurences(pattern)
        occurrence_counts.append(num_occurrences)
    print(" ".join(map(str, occurrence_counts)))


if __name__ == "__main__":
    # run_test()
    run_algo()
