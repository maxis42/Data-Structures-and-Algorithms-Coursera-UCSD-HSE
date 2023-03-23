# Uses python3


def max_dot_product(a, b):
    a.sort(reverse=True)
    b.sort(reverse=True)

    res = 0

    for i in range(len(a)):
        res += a[i] * b[i]
    return res


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    print(max_dot_product(a, b))
