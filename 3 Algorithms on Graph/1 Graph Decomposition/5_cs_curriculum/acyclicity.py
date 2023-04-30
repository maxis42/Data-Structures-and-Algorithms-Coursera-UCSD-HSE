# Uses python3

import sys
from collections import deque


class Graph:
    def __init__(self, n, m, edges):
        self.n = n  # number of vertices
        self.m = m  # number of edges
        self.edges = edges
        self.adj_list = self.get_adj_list(self.n, self.edges)
        self.cyclic = 1 if self.is_cyclic() else 0

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        edges_new = []
        for v1, v2 in edges:
            edges_new.append((v1-1, v2-1))
        edges_new = tuple(edges_new)
        self._edges = edges_new

    @staticmethod
    def get_adj_list(n, edges):
        adj_list = {i: [] for i in range(n)}
        for v_start, v_end in edges:
            adj_list[v_start].append(v_end)
        return adj_list

    def is_cyclic(self):
        cyclic = False
        for v, children in self.adj_list.items():
            visited = [False for _ in range(self.n)]
            visited[v] = True
            q = deque(children)
            while q:
                current = q.popleft()

                if current == v:
                    cyclic = True
                    break

                if not visited[current]:
                    visited[current] = True
                    for child in self.adj_list[current]:
                        q.append(child)

            if cyclic:
                break
        return cyclic


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    graph = Graph(n, m, edges)
    print(graph.cyclic)


def run_failed_test():
    with open("test2.txt", "r") as f:
        data = f.read()

    # read data
    data = list(map(int, data.split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    graph = Graph(n, m, edges)
    print(graph.cyclic)


if __name__ == "__main__":
    # run_failed_test()
    run_algo()
