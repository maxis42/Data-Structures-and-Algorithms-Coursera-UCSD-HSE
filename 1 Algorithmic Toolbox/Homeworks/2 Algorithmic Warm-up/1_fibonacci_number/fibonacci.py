# Uses python3
def calc_fib(n):
    fib_nums = []
    fib_nums.append(0)
    fib_nums.append(1)
    for i in range(2, n + 1):
        fib_nums.append(fib_nums[i - 1] + fib_nums[i - 2])
    return fib_nums[n]


if __name__ == "__main__":
    n = int(input())
    print(calc_fib(n))
