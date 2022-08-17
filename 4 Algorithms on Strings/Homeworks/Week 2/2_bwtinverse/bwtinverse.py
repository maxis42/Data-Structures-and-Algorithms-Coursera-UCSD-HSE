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

        first_d = dict()
        first_d_extra = []
        first_cnt = 0
        first_char = first_col[0]
        last_d = dict()
        last_d_extra = []
        last_cnt = dict()
        for i in range(len(bwt)):
            if first_col[i] != first_char:
                first_char = first_col[i]
                first_cnt = 0

            first_d[(first_char, first_cnt)] = i
            first_d_extra.append((first_char, first_cnt))
            first_cnt += 1

            last_char = last_col[i]
            if last_char not in last_cnt:
                last_cnt[last_char] = 0

            last_d[(last_char, last_cnt[last_char])] = i
            last_d_extra.append((last_char, last_cnt[last_char]))
            last_cnt[last_char] += 1

        key = ("$", 0)
        s = ""
        for i in range(len(bwt)):
            next_id = last_d[key]
            next_char = first_col[next_id]
            s += next_char
            key = first_d_extra[next_id]

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
