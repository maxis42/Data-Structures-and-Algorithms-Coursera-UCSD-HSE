# Uses python3
import sys
import random


def partition3(a, left, right):
    x = a[left]
    lt = left
    gt = right
    i = left
    while i <= gt:
        if a[i] < x:
            a[i], a[lt] = a[lt], a[i]
            lt += 1
            i += 1
        elif a[i] > x:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def partition2(a, left, right):
    x = a[left]
    j = left
    for i in range(left + 1, right + 1):
        if a[i] <= x:
            j += 1
            a[i], a[j] = a[j], a[i]
    a[left], a[j] = a[j], a[left]
    return j


def randomized_quick_sort2(a, left, right):
    if left >= right:
        return

    k = random.randint(left, right)
    a[left], a[k] = a[k], a[left]

    # use partition2
    m = partition2(a, left, right)
    randomized_quick_sort2(a, left, m - 1)
    randomized_quick_sort2(a, m + 1, right)


def randomized_quick_sort3(a, left, right):
    if left >= right:
        return

    k = random.randint(left, right)
    a[left], a[k] = a[k], a[left]

    # use partition3
    m1, m2 = partition3(a, left, right)
    randomized_quick_sort3(a, left, m1 - 1)
    randomized_quick_sort3(a, m2 + 1, right)


# without tail recursion
def randomized_quick_sort3_wo_recursion(a, left, right):
    while left <= right:
        k = random.randint(left, right)
        a[left], a[k] = a[k], a[left]

        # use partition3
        m1, m2 = partition3(a, left, right)
        if (m1 - left) < (right - left):
            randomized_quick_sort3_wo_recursion(a, left, m1 - 1)
            left = m2 + 1
        else:
            randomized_quick_sort3_wo_recursion(a, m2 + 1, right)
            right = m1 - 1


def stress_test():
    i = 0
    while(True):
        N = random.randint(1, 4)
        rand_nums = [random.randint(1, 4) for i in range(0, N)]
        print(rand_nums)
        # rand_nums = [10**9] * 10**5

        # randomized_quick_sort2(rand_nums, 0, (len(rand_nums)-1))
        randomized_quick_sort3(rand_nums, 0, (len(rand_nums)-1))

        if rand_nums == sorted(rand_nums):
            print(i, 'OK')
        else:
            print(i, 'Not OK')
            print(N)
            print('my_sort:     ', rand_nums)
            print('python_sort: ', sorted(rand_nums))
            break

        i += 1


if __name__ == '__main__':
    # stress_test()

    input = sys.stdin.read()
    n, *a = list(map(int, input.split()))
    randomized_quick_sort3_wo_recursion(a, 0, n - 1)
    for x in a:
        print(x, end=' ')
