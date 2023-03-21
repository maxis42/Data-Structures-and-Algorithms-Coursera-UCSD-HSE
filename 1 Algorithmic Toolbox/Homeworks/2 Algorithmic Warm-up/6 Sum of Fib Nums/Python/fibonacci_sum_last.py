# Uses python3


def get_remainders(n, m):
    if n <= 1:
        return n, n

    remainders = [0, 1]
    period = 0

    for i in range(2, 6*m + 2):
        remainders.append((remainders[i - 1] + remainders[i - 2]) % m)
        period += 1
        if remainders[i - 1] == 0 and remainders[i] == 1:
            break

    return remainders, period


def get_fibonacci_sum_last_digit(n):
    if n <= 1:
        return n
    remainders, period = get_remainders(n, 10)
    remainder_sum = 0

    for i in range(0, n % period+1):
        remainder_sum += remainders[i]

    remainders_period_sum = sum(remainders) - sum(remainders[:2])

    return (remainders_period_sum * (n // period) + remainder_sum) % 10


if __name__ == '__main__':
    n = int(input())
    print(get_fibonacci_sum_last_digit(n))
