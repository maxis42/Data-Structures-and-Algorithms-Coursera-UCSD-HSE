# Uses python3
from numpy import random


def binary_search(a, x):
    left, right = 0, len(a)-1

    while left <= right:
        mid = (left + right) // 2
        if x == a[mid]:
            return mid
        elif x < a[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return -1


def linear_search(a, x):
    for i in range(len(a)):
        if a[i] == x:
            return i
    return -1


def stress_test():
    flag_correct = True
    i = 0
    while flag_correct:
        N = random.randint(1, 10)
        x = random.randint(1, 10)
        a = random.randint(0, 10, size=N)
        a.sort()

        print(i, a, x, N)

        ls_res = linear_search(a, x)
        bs_res = binary_search(a, x)

        if ls_res != bs_res:
            print(i, a, x, N)
            print('Linear search:', ls_res)
            print('Binary search:', bs_res)
            flag_correct = False

        i += 1


if __name__ == '__main__':
    # stress_test()

    arr = list(map(int, input().split()))[1:]
    val = list(map(int, input().split()))[1:]

    for v in val:
        print(binary_search(arr, v), end=' ')
