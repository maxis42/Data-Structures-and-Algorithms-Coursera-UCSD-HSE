# Uses python3
import sys


def gcd(a, b):
    if b == 0:
        return a
    a_remainder = a % b
    return gcd(b, a_remainder)


input_nums = sys.stdin.read()
a, b = map(int, input_nums.split())
print(gcd(a, b))
