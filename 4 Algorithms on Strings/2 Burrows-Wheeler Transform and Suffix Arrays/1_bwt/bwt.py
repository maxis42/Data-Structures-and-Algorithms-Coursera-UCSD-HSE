# python3
import sys


class BWT:
    def __init__(self, text):
        self.text = text
        self.bwt = self._bwt(self.text)

    @staticmethod
    def _bwt(text):
        matrix = [text]
        for i in range(len(text) - 1):
            text = text[-1] + text[:-1]
            matrix.append(text)

        matrix.sort()

        res = "".join([s[-1] for s in matrix])
        return res


def run_test():
    text = "ACACACAC$"
    bwt = BWT(text)
    print(bwt.bwt)


def run_algo():
    text = sys.stdin.readline().strip()
    bwt = BWT(text)
    print(bwt.bwt)


if __name__ == "__main__":
    # run_test()
    run_algo()
