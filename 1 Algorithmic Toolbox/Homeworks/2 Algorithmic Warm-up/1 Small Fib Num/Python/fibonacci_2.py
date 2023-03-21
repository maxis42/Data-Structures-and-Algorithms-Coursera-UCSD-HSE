# Uses python3
def calc_fib(n):
    fib_1 = 0
    fib_2 = 1
    
    for i in range(2, n + 1):
        fib_new = fib_1 + fib_2
        fib_1, fib_2 = fib_2, fib_new
    
    return fib_2


if __name__ == "__main__":
    n = int(input())
    print(calc_fib(n))
