# Uses python3
def calc_fib_last_digit(n):
    fib_ld_1 = 0
    fib_ld_2 = 1
    for i in range(2, n + 1):
        fib_ld_new = (fib_ld_1 + fib_ld_2) % 10
        fib_ld_1, fib_ld_2 = fib_ld_2, fib_ld_new
    return fib_ld_2


if __name__ == "__main__":
    n = int(input())
    print(calc_fib_last_digit(n))
