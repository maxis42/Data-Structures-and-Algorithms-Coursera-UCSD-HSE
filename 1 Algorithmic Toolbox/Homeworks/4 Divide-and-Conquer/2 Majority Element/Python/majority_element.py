# Uses python3
import sys
from numpy import random


def get_majority_element_naive(a, left, right):
    if left == right:
        return -1
    if left + 1 == right:
        return a[left]
    # write your code here
    for i in range(right):
        cur_elem = a[i]
        cnt = 0
        for j in range(right):
            if a[j] == cur_elem:
                cnt += 1
        # print('naive:', cur_elem, cnt, right/2)
        if cnt > right/2:
            return cur_elem
    return -1


def get_majority_element(a, left, right):
    # check array on zero elements
    if left == right:
        return -1

    # check array on only one element
    if left + 1 == right:
        return a[left]

    # sort the array to get n*log(n) complexity
    a.sort()

    # initialize counters
    cur_elem = a[0]
    cur_cnt = 1
    max_elem = a[0]
    max_cnt = 1

    # iterate through sorted array
    for i in range(1, right):
        if a[i] == cur_elem:
            cur_cnt += 1
        else:
            if cur_cnt > max_cnt:
                max_elem = cur_elem
                max_cnt = cur_cnt
            cur_elem = a[i]
            cur_cnt = 1

    # last element check
    if cur_cnt > max_cnt:
        max_elem = cur_elem
        max_cnt = cur_cnt

    # print('fast:', max_elem, max_cnt, right/2)

    # check for majority
    if max_cnt > right/2:
        return max_elem

    # return -1 if no majority element
    return -1


def stress_test():
    flag_correct = True
    i = 0
    while flag_correct:
        N = random.randint(1, 10)
        a = random.randint(0, 10, size=N)
        a.sort()

        print(i, a, N)

        alg_naive = get_majority_element_naive(a, 0, N)
        alg_fast = get_majority_element(a, 0, N)

        if alg_naive != alg_fast:
            print('Naive algorithm:', alg_naive)
            print('Fast algorithm:', alg_fast)
            flag_correct = False

        i += 1


if __name__ == '__main__':
    # stress_test()

    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    if get_majority_element(a, 0, n) != -1:
        print(1)
    else:
        print(0)
