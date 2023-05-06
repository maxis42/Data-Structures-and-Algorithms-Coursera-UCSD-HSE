# python3
import sys


class KnuthMorrisPratt:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

        self.pattern_starts = self._get_pattern_starts(self.text, self.pattern)

    def _get_pattern_starts(self, text, pattern):
        """
        Find all the occurrences of the pattern in the text
        and return a list of all positions in the text
        where the pattern starts in the text.
        """
        s = "".join([pattern, "$", text])
        pref_func_arr = self._get_prefix_func_arr(s)

        res = []
        for i in range(len(pattern) + 1, len(s)):
            if pref_func_arr[i] == len(pattern):
                start_pos = i - 2*len(pattern)
                res.append(start_pos)

        return res

    @staticmethod
    def _get_prefix_func_arr(s):
        res = [0]
        border = 0

        for i in range(1, len(s)):
            while (border > 0) and (s[i] != s[border]):
                border = res[border - 1]

            if s[i] == s[border]:
                border += 1
            else:
                border = 0

            res.append(border)

        return res


def run_test():
    text = "GATATATGCATATACTT"
    pattern = "ATAT"
    kmp = KnuthMorrisPratt(text, pattern)
    res = kmp.pattern_starts
    print(" ".join(map(str, res)))


def run_algo():
    pattern = sys.stdin.readline().strip()
    text = sys.stdin.readline().strip()
    kmp = KnuthMorrisPratt(text, pattern)
    res = kmp.pattern_starts
    print(" ".join(map(str, res)))


if __name__ == "__main__":
    # run_test()
    run_algo()
