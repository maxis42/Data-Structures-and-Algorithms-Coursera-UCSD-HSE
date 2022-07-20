# Uses python3
import sys
from math import sqrt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Edge:
    def __init__(self, start, end, p_start, p_end):
        self.start = start
        self.end = end
        self.p_start = p_start
        self.p_end = p_end

        self.weight = sqrt((p_end.x - p_start.x)**2 + (p_end.y - p_start.y)**2)

    def __str__(self):
        return f"Edge {self.start}-{self.end} weight={self.weight:.2f}"


class DisjointSet:
    def __init__(self, n):
        self.n = n
        self.ds = [i for i in range(n)]
        self.num_sets = self.n

    def find(self, i):
        while self.ds[i] != i:
            prev = i
            i = self.ds[i]
            # path compression
            self.ds[prev] = i
        return i

    def union(self, i, j):
        i_parent = self.find(i)
        j_parent = self.find(j)

        if i_parent != j_parent:
            self.ds[j_parent] = i_parent
            self.num_sets -= 1


def clustering(x, y, k):
    ans = float("inf")

    n = len(x)

    # create all edges with weights
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            edges.append(Edge(i, j, Point(x[i], y[i]), Point(x[j], y[j])))

    # sort edges by weight
    edges = sorted(edges, key=lambda edge: edge.weight)

    dj = DisjointSet(n)

    for edge in edges:
        if dj.find(edge.start) != dj.find(edge.end):
            if dj.num_sets > k:
                dj.union(edge.start, edge.end)
            else:
                ans = min(ans, edge.weight)

    return ans


def run_algo():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    data = data[1:]
    x = data[0:2 * n:2]
    y = data[1:2 * n:2]
    data = data[2 * n:]
    k = data[0]
    print("{0:.9f}".format(clustering(x, y, k)))


def run_test():
    x = [7, 4, 5, 1, 2, 5, 3, 7, 2, 4, 6, 2]
    y = [6, 3, 1, 7, 7, 7, 3, 8, 8, 4, 7, 6]
    k = 3
    print("{0:.9f}".format(clustering(x, y, k)))


if __name__ == "__main__":
    # run_test()
    run_algo()
