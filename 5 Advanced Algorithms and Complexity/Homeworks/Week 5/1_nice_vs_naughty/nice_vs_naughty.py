# python3

import sys

D = dict()

n = int(sys.stdin.readline().strip())
t = int(sys.stdin.readline().strip())

for _ in range(n):
    id, value = [int(i) for i in sys.stdin.readline().strip().split()]
    assert(id not in D)
    D[id] = value

for _ in range(n):
    id, value = [int(i) for i in sys.stdin.readline().strip().split()]
    assert(id in D)
    D[id] -= value


num_queries = int(sys.stdin.readline().strip())
queries = list(map(int, sys.stdin.readline().strip().split()))
assert(len(queries) == num_queries)

for query in queries:
    if D[query] >= t:
        print("1 ", end="")
    else:
        print("0 ", end="")
