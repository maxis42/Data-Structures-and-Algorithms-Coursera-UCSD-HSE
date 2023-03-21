# Uses python3
import sys


def gcd(a, b):
    if b == 0:
        return a
    a = a % b
    return gcd(b, a)


if __name__ == "__main__":
    input_nums = sys.stdin.read()
    a, b = map(int, input_nums.split())
    print(gcd(a, b))
