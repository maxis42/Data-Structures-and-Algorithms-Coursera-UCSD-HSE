# Uses python3
from typing import List

import numpy as np


def optimal_weight_starter(W, w):
    # write your code here
    result = 0
    for x in w:
        if result + x <= W:
            result = result + x
    return result


def optimal_weight(capacity: int, weights: List[int]) -> int:
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

    #     # initialize
    #     for i in range(n):
    #         value[i, 0] = 0
    #     for j in range(capacity):
    #         value[0, j] = 0

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

    # print(value)
    res = value[n, capacity]
    return res


if __name__ == '__main__':
    W, n = map(int, input().split())
    w = list(map(int, input().split()))
    print(optimal_weight(W, w))
