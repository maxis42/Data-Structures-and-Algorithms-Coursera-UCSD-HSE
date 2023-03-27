# Uses python3
import sys
from numpy import random
sys.setrecursionlimit(200000)


def majority_element_fast(arr):
    d = dict()
    for a in arr:
        if a not in d:
            d[a] = 1
        else:
            d[a] += 1

    maj = len(arr) // 2 + 1
    for k, v in d.items():
        if v >= maj:
            return k, v
    return -1, -1


def majority_element_div_and_conq(arr, left, right):
    # last tree level
    if left == right:
        return arr[left], 1
    else:
        # split point
        mid = (left + right) // 2

        left_maj, n_left_maj = majority_element_div_and_conq(arr, left, mid)
        right_maj, n_right_maj = majority_element_div_and_conq(arr, mid + 1, right)

        if left_maj == right_maj:
            if left_maj == -1:
                return -1, -1
            else:
                return left_maj, n_left_maj + n_right_maj

        for i in range(mid + 1, right + 1):
            if arr[i] == left_maj:
                n_left_maj += 1

        for i in range(left, mid + 1):
            if arr[i] == right_maj:
                n_right_maj += 1

        maj = (right - left + 1) // 2 + 1
        if n_left_maj >= maj:
            return left_maj, n_left_maj
        elif n_right_maj >= maj:
            return right_maj, n_right_maj
        else:
            return -1, -1


def stress_test():
    i = 0
    while True:
        N = random.randint(1, 10)
        arr = random.randint(0, 5, size=N)

        print(i)

        maj_fast, n_fast = majority_element_fast(arr)
        maj_div_and_conq, n_div_and_conq = majority_element_div_and_conq(arr, 0, len(arr) - 1)

        if maj_fast != maj_div_and_conq:
            print("Array:", arr)
            print("Fast algorithm:", maj_fast)
            print("Divide & conquer algorithm:", maj_div_and_conq)
            break

        i += 1


if __name__ == "__main__":
    # stress_test()

    n = int(input())
    arr = list(map(int, input().split()))
    if majority_element_div_and_conq(arr, 0, n - 1)[0] != -1:
        print(1)
    else:
        print(0)
