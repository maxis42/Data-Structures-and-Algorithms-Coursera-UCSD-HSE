import itertools
from typing import List

import numpy as np


def partition3_starter(A):
    for c in itertools.product(range(3), repeat=len(A)):
        sums = [None] * 3
        for i in range(3):
            sums[i] = sum(A[k] for k in range(len(A)) if c[k] == i)

        if sums[0] == sums[1] and sums[1] == sums[2]:
            return 1

    return 0


def optimal_weight_matrix(capacity: int, weights: List[int]) -> np.array:
    """
    You are given a set of bars of gold and your goal is to take as much gold
    as possible into your bag. There is just one copy of each bar and for each
    bar you can either take it or not (hence you cannot take a fraction of a
    bar).

    :param capacity: bag capacity
    :param weights: bar weights

    :return: max amount of gold
    """
    n = len(weights)

    value = np.zeros((n + 1, capacity + 1), dtype=np.int)

    for i in range(1, n + 1):
        elem = weights[i - 1]
        for w in range(1, capacity + 1):
            # do not use the new elem (default case)
            value[i, w] = value[i - 1, w]

            # if elem fits into w try to use it
            if elem <= w:
                val = value[i - 1, w - elem] + elem

                # if result with the new elem better, use it
                if value[i, w] < val:
                    value[i, w] = val

    return value


def reconstruct_solution(weights, value_matrix):
    n, w = value_matrix.shape

    solution = np.full(n - 1, False)

    row = n - 1
    weight = w - 1
    while row != 0:
        value = value_matrix[row, weight]

        if value == value_matrix[row - 1, weight]:
            pass
        else:
            weight -= weights[row - 1]
            solution[row - 1] = True

        row -= 1
    return solution


def drop_used_bars(weights, solution):
    return weights[~solution.astype(bool)]


def is_partition3(weights):
    weights = np.array(weights)
    capacity3 = weights.sum()

    if capacity3 % 3 != 0:
        return False

    weights_counts = dict()
    for w in weights:
        if w not in weights_counts:
            weights_counts[w] = 1
        else:
            weights_counts[w] += 1

    weights = []
    for w, cnt in weights_counts.items():
        cnt = cnt % 3
        for _ in range(cnt):
            weights.append(w)

    weights = np.array(weights)

    if len(weights) == 0:
        return True

    if capacity3 % 3 != 0:
        return False
    capacity = capacity3 // 3

    for _ in range(3):
        value_matrix = optimal_weight_matrix(capacity, weights)
        if value_matrix[len(weights), capacity] != capacity:
            return False
        solution = reconstruct_solution(weights, value_matrix)
        weights = drop_used_bars(weights, solution)

    return True


if __name__ == '__main__':
    n = int(input())
    A = list(map(int, input().split()))
    if is_partition3(A):
        print(1)
    else:
        print(0)
