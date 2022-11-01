# python3
from math import log
from statistics import median
from random import randint


class CountSketch:
    prime = 10000019

    def __init__(self):
        self.n = int(input())  # number of children
        self.t = int(input())  # change threshold

        self.num_hashes = 80
        self.num_buckets = 10000

        self.hash_functions_pos_ab = tuple(
            (randint(1, CountSketch.prime - 1), randint(0, CountSketch.prime - 1))
            for _ in range(self.num_hashes)
        )
        self.hash_functions_sign_ab = tuple(
            (randint(1, CountSketch.prime - 1), randint(0, CountSketch.prime - 1))
            for _ in range(self.num_hashes)
        )

        self.good_things = [[0]*self.num_buckets for _ in range(self.num_hashes)]
        self.bad_things = [[0]*self.num_buckets for _ in range(self.num_hashes)]

    def process_data(self):
        for _ in range(self.n):
            child_id, num_good_things = map(int, input().split())

            for i in range(self.num_hashes):
                pos, sign = self._get_pos_sign(i, child_id)
                self.good_things[i][pos] += sign * num_good_things

        for _ in range(self.n):
            child_id, num_bad_things = map(int, input().split())

            for i in range(self.num_hashes):
                pos, sign = self._get_pos_sign(i, child_id)
                self.bad_things[i][pos] += sign * num_bad_things

    def process_queries(self):
        num_queries = int(input())
        queries = list(map(int, input().split()))

        ans = []
        for child_id in queries:
            good_things_est = []
            for i in range(self.num_hashes):
                pos, sign = self._get_pos_sign(i, child_id)
                est = sign * self.good_things[i][pos]
                good_things_est.append(est)
            good_things_approx = median(good_things_est)

            bad_things_est = []
            for i in range(self.num_hashes):
                pos, sign = self._get_pos_sign(i, child_id)
                est = sign * self.bad_things[i][pos]
                bad_things_est.append(est)
            bad_things_approx = median(bad_things_est)

            if good_things_approx - bad_things_approx >= self.t:
                ans.append(1)
            else:
                ans.append(0)
        return ans

    def _get_pos_sign(self, hash_i, hash_v):
        a1, b1 = self.hash_functions_pos_ab[hash_i]
        a2, b2 = self.hash_functions_sign_ab[hash_i]

        bucket = (a1 * hash_v + b1) % CountSketch.prime % self.num_buckets
        sign = 1 if (a2 * hash_v + b2) % CountSketch.prime % 2 == 0 else -1
        return bucket, sign


def count_sketch_naive():
    num_children = int(input())
    threshold = int(input())

    good_things = dict()
    bad_things = dict()

    for _ in range(num_children):
        child_id, num_good_things = map(int, input().split())
        good_things[child_id] = num_good_things

    for _ in range(num_children):
        child_id, num_bad_things = map(int, input().split())
        bad_things[child_id] = num_bad_things

    num_queries = int(input())
    queries = list(map(int, input().split()))

    ans = []
    for child_id in queries:
        if good_things[child_id] - bad_things[child_id] >= threshold:
            ans.append(1)
        else:
            ans.append(0)

    print(" ".join(map(str, ans)))


def run_test():
    pass


def run_algo():
    # count_sketch_naive()

    cs = CountSketch()
    cs.process_data()
    ans = cs.process_queries()
    print(" ".join(map(str, ans)))


if __name__ == "__main__":
    # run_test()
    run_algo()
