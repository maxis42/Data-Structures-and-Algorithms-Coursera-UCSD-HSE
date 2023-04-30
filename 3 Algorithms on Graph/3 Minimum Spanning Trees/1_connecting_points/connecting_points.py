# Uses python3
import sys
import heapq
from math import sqrt


def minimum_distance(x, y):
    result = 0
    n = len(x)

    cost = [float("inf") for _ in range(n)]
    cost[0] = 0

    visited = [False for _ in range(n)]

    pq = []
    # (priority, ID)
    start = (0, 0)
    heapq.heappush(pq, start)

    while pq:
        w, cur = heapq.heappop(pq)

        # Check whether the node was already visited.
        # It allows to use "lazy" priority queue.
        if not visited[cur]:
            visited[cur] = True

            result += w

            for i in range(n):
                if not visited[i]:
                    dist = sqrt((x[i] - x[cur])**2 + (y[i] - y[cur])**2)
                    if dist < cost[i]:
                        cost[i] = dist
                        # We do not update the priority (cost) of the vertex.
                        # Instead, we push the same vertex with updated priority.
                        # As the updated priority is smaller than the previous
                        # one, the new entry will be processed first. And then
                        # the vertex will be marked as visited.
                        heapq.heappush(pq, (dist, i))

    return result


def run_algo():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(minimum_distance(x, y)))


def run_test():
    x = [0, 0, 1, 1]
    y = [0, 1, 0, 1]

    x = [0, 0, 1, 3, 3]
    y = [0, 2, 1, 0, 2]

    print("{0:.9f}".format(minimum_distance(x, y)))


if __name__ == "__main__":
    run_algo()
    # run_test()
