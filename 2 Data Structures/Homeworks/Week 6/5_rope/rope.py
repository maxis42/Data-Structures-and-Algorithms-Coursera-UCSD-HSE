# python3

import sys

if __name__ == "__main__":
    s = sys.stdin.readline().strip()
    q = int(sys.stdin.readline())
    for _ in range(q):
        i, j, k = map(int, sys.stdin.readline().strip().split())
        part = s[i:j+1]
        rest = s[:i] + s[j+1:]
        s = rest[:k] + part + rest[k:]
    print(s)
