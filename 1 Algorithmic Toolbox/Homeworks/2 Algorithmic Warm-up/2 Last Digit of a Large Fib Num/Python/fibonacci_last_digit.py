# Uses python3
def calc_fib_last_digit(n):
    fib_nums_last_dig = []
    fib_nums_last_dig.append(0)
    fib_nums_last_dig.append(1)
    for i in range(2, n + 1):
        fib_nums_last_dig.append((fib_nums_last_dig[i - 1] + fib_nums_last_dig[i - 2]) % 10)
    return fib_nums_last_dig[n]


if __name__ == "__main__":
    n = int(input())
    print(calc_fib_last_digit(n))
