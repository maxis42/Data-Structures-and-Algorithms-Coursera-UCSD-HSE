# Uses python3


def optimal_summands(n):
    summands = []
    p = 1
    while n > 0:
        n -= p
        if (p + 1) > n:
            p_last = p + n
            summands.append(p_last)
            n = 0
        else:
            summands.append(p)
            p += 1
    return summands


if __name__ == '__main__':
    n = int(input())

    summands = optimal_summands(n)

    print(len(summands))
    for x in summands:
        print(x, end=' ')
