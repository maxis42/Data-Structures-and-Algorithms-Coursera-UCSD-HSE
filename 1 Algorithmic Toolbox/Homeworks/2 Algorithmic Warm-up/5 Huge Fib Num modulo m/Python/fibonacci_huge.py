# Uses python3


def get_fibonacci_huge_mod(n, m):
    if n <= 1:
        return n

    remainders = [0, 1]

    period = 0

    for i in range(2, 6*m + 2):
        remainders.append((remainders[i - 1] + remainders[i - 2]) % m)
        period += 1
        if remainders[i - 1] == 0 and remainders[i] == 1:
            break

    return remainders[n % period]


if __name__ == '__main__':
    n, m = map(int, input().split())
    print(get_fibonacci_huge_mod(n, m))
