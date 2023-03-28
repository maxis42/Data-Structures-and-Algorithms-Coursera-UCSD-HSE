# Uses python3


def merge_sort(a):
    n = len(a)
    if n == 1:
        return a
    mid = n // 2
    b = merge_sort(a[:mid])
    c = merge_sort(a[mid:])
    a_new = merge(b, c)
    return a_new


def merge(b, c):
    d = list()
    while (len(b) != 0) and (len(c) != 0):
        if b[0] <= c[0]:
            d.append(b[0])
            b = b[1:]
        else:
            d.append(c[0])
            c = c[1:]
    d.extend(b)
    d.extend(c)
    return d


if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))

    print(merge_sort(arr))
