# Uses python3
import sys
from collections import deque


class Graph:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        self.adj_list = self.get_adj_list(self.n, self.edges)

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edges):
        new_edges = []
        for v1, v2 in edges:
            new_edges.append((v1-1, v2-1))
        new_edges = tuple(new_edges)
        self._edges = new_edges

    @staticmethod
    def get_adj_list(n, edges):
        adj_list = {i: [] for i in range(n)}
        for v1, v2 in edges:
            adj_list[v1].append(v2)
            adj_list[v2].append(v1)
        return adj_list

    def is_bipartite(self):
        bipartite = True

        visited = [False for _ in range(self.n)]
        color = [False for _ in range(self.n)]

        for v in range(self.n):
            q = deque([v])
            while q:
                cur = q.popleft()
                if not visited[cur]:
                    visited[cur] = True

                    for child in self.adj_list[cur]:
                        if visited[child]:
                            if color[child] == color[cur]:
                                bipartite = False
                                break
                        else:
                            q.append(child)
                            color[child] = not color[cur]

                if not bipartite:
                    break

            if not bipartite:
                break

        return bipartite


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    graph = Graph(n, edges)
    print(1 if graph.is_bipartite() else 0)


def run_test():
    # n, m = 4, 4
    # edges = (
    #     (1, 2),
    #     (4, 1),
    #     (2, 3),
    #     (3, 1),
    # )

    # n, m = 5, 4
    # edges = (
    #     (5, 2),
    #     (4, 2),
    #     (3, 4),
    #     (1, 4),
    # )

    # n, m = 1, 0
    # edges = ()

    # n = 5
    # edges = (
    #     (1, 2),
    #     (2, 3),
    #     (3, 4),
    #     (4, 5),
    #     (5, 1),
    # )
    #
    # n = 6
    # edges = (
    #     (1, 2),
    #     (2, 3),
    #     (3, 4),
    #     (4, 5),
    #     (5, 6),
    #     (6, 1),
    # )

    n = 1
    edges = ((1, 1),)

    graph = Graph(n, edges)
    print(1 if graph.is_bipartite() else 0)


if __name__ == "__main__":
    # run_test()
    run_algo()
