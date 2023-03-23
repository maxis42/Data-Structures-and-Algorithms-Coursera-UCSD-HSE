# Uses python3


def gcd(a, b):
    if b == 0:
        return a
    a = a % b
    return gcd(b, a)


if __name__ == "__main__":
    a, b = map(int, input().split())
    print(gcd(a, b))
