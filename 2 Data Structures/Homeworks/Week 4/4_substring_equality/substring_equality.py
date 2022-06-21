# python3
import sys
from collections import namedtuple
import random

import numpy as np

Test = namedtuple("Test", ["string", "n_queries", "queries", "output"])


class Solver:
    # _multiplier = random.randint(1, 10**9)
    _multiplier = 273
    _prime1 = 1000000007
    _prime2 = 1000000009

    def __init__(self, string):
        self.string = string

        self.hashes1 = self._precompute_hashes(self.string, self._prime1)
        self.hashes2 = self._precompute_hashes(self.string, self._prime2)

    def _precompute_hashes(self, string, prime):
        hashes = [0 for _ in range(len(string) + 1)]
        for i in range(1, len(string) + 1):
            hashes[i] = (self._multiplier * hashes[i - 1] + ord(string[i-1])) % prime
        return hashes

    @staticmethod
    def _modular_exponentitation(a, b, n):
        """
        a**b mod n
        """
        c = 0
        d = 1
        b = str(bin(b))[2:]
        for i in range(len(b)):
            c *= 2
            d = (d*d) % n
            if int(b[i]) == 1:
                c += 1
                d = (d*a) % n
        return d

    def _calc_substring_hash(self, hashes, prime, start, length):
        last = hashes[start + length]

        y = self._modular_exponentitation(self._multiplier, length, prime)

        substring_hash = (last - y*hashes[start]) % prime
        return substring_hash

    def check_equality(self, a, b, l):
        if l == 0:
            is_equal = True
        else:
            hash1_a = self._calc_substring_hash(self.hashes1, self._prime1, a, l) % self._prime1
            hash1_b = self._calc_substring_hash(self.hashes1, self._prime1, b, l) % self._prime1

            hash2_a = self._calc_substring_hash(self.hashes2, self._prime2, a, l) % self._prime2
            hash2_b = self._calc_substring_hash(self.hashes2, self._prime2, b, l) % self._prime2

            is_equal = (hash1_a == hash1_b) and (hash2_a == hash2_b)
        return is_equal


def run_algo():
    string = sys.stdin.readline()
    n_queries = int(sys.stdin.readline())

    solver = Solver(string)

    for i in range(n_queries):
        a, b, length = map(int, sys.stdin.readline().split())
        print("Yes" if solver.check_equality(a, b, length) else "No")


def run_tests():
    test1 = Test(
        string="trololo",
        n_queries=4,
        queries=(
            (0, 0, 7),
            (2, 4, 3),
            (3, 5, 1),
            (1, 3, 2),
        ),
        output=("Yes", "Yes", "Yes", "No"),
    )

    test2 = Test(
        string="bbbabbabaa",
        n_queries=10,
        queries=(
            (7, 0, 1),
            (1, 7, 1),
            (2, 7, 1),
            (6, 1, 3),
            (2, 5, 5),
            (4, 6, 4),
            (9, 4, 1),
            (8, 3, 2),
            (5, 4, 4),
            (5, 1, 4),
            (0, 0, 3),
            (3, 4, 6),
            (5, 3, 2),
        ),
        output=("Yes", "Yes", "Yes", "No", "No", "No", "No", "No", "No", "No", "Yes", "No", "No")
    )

    tests = (test1, test2,)

    for test in tests:
        solver = Solver(test.string)
        result = []
        for a, b, length in test.queries:
            res = solver.check_equality(a, b, length)
            result.append("Yes" if res else "No")
        result = tuple(result)
        assert test.output == result, f"""
        Expected: {test.output}
        Got:      {result}
        """
        print("Test passed!\n")


def run_stress_test():
    string = "bbbabbabaa"
    solver = Solver(string)

    while True:
        a = np.random.choice(range(len(string)))
        b = np.random.choice(range(len(string)))
        l = np.random.choice(range(min(len(string) - a, len(string) - b)))
        print(a, b, l)

        pred = solver.check_equality(a, b, l)

        true = (string[a:(a+l)] == string[b:(b+l)])
        if pred != true:
            print(a, b, l, true, pred)
            break


if __name__ == "__main__":
    # run_stress_test()
    # run_tests()
    run_algo()
