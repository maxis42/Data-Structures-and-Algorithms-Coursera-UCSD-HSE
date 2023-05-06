# python3
import sys
from collections import defaultdict


class InverseBWT:
    def __init__(self, bwt):
        self.bwt = bwt
        self.text = self._text(self.bwt)

    @staticmethod
    def _text(bwt):
        last_col = bwt
        first_col = "".join(sorted(bwt))

        first_char_to_cnt = []
        first_counter = defaultdict(int)

        last_char_to_cnt = []
        last_counter = defaultdict(int)

        for i in range(len(bwt)):
            first_char_to_cnt.append(first_counter[first_col[i]])
            first_counter[first_col[i]] += 1

            last_char_to_cnt.append(last_counter[last_col[i]])
            last_counter[last_col[i]] += 1

        last_char_id_to_id = dict()
        for i in range(len(bwt)):
            last_char_id_to_id[(last_col[i], last_char_to_cnt[i])] = i

        s = ""
        i = 0
        for _ in range(len(bwt)):
            i = last_char_id_to_id[(first_col[i], first_char_to_cnt[i])]
            s += first_col[i]

        return s


def run_test():
    bwt = "SMNPBNNAAAAA$A"
    ibwt = InverseBWT(bwt)
    print(ibwt.text)


def run_algo():
    bwt = sys.stdin.readline().strip()
    ibwt = InverseBWT(bwt)
    print(ibwt.text)


if __name__ == "__main__":
    # run_test()
    run_algo()
