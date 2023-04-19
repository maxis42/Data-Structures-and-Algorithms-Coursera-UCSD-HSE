# Uses python3
from typing import List
import numpy as np


def evalt(a, b, op):
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    else:
        assert False


def get_min_max(
        i: int,
        j: int,
        min_vals: np.array,
        max_vals: np.array,
        operations: List[str]
) -> (int, int):
    min_val = np.iinfo(np.int32).max
    max_val = np.iinfo(np.int32).min

    # iterate by the last possible operation
    for k in range(i, j):
        a = evalt(max_vals[i, k], max_vals[k + 1, j], operations[k])
        b = evalt(max_vals[i, k], min_vals[k + 1, j], operations[k])
        c = evalt(min_vals[i, k], max_vals[k + 1, j], operations[k])
        d = evalt(min_vals[i, k], min_vals[k + 1, j], operations[k])
        min_val = min(min_val, a, b, c, d)
        max_val = max(max_val, a, b, c, d)

    return min_val, max_val


def get_maximum_value(expression: str) -> int:
    digits = [int(c) for i, c in enumerate(expression) if i % 2 == 0]
    operations = [c for i, c in enumerate(expression) if i % 2 != 0]

    n = len(digits)

    min_vals = np.zeros((n, n), dtype=np.int)
    max_vals = np.zeros((n, n), dtype=np.int)

    for i in range(n):
        min_vals[i, i] = digits[i]
        max_vals[i, i] = digits[i]

    for k in range(1, n):
        for i in range(n - k):
            j = k + i
            min_vals[i, j], max_vals[i, j] = get_min_max(i, j, min_vals,
                                                         max_vals, operations)

    res = max_vals[0, n - 1]
    return res


if __name__ == "__main__":
    print(get_maximum_value(input()))
