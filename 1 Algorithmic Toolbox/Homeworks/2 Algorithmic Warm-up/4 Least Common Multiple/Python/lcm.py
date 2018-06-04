# Uses python3
import sys


def gcd(a, b):
    if b == 0:
        return a
    a_remainder = a % b
    return gcd(b, a_remainder)


def lcm(a, b):
    if a == b == 0:
        return 0
    return a * b // gcd(a, b)


if __name__ == '__main__':
    input = sys.stdin.read()
    a, b = map(int, input.split())
    print(lcm(a, b))
