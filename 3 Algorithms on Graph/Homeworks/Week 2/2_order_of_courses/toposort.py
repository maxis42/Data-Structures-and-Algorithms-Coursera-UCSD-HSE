# Uses python3

import sys


class Graph:
    def __init__(self, n, m, edges):
        self.n = n  # number of vertices
        self.m = m  # number of edges
        self.edges = edges
        self.adj_list, self.sources = self.get_adj_list_and_sources(self.n, self.edges)

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
    def get_adj_list_and_sources(n, edges):
        adj_list = {i: [] for i in range(n)}
        sources = [True for _ in range(n)]
        for v_start, v_end in edges:
            adj_list[v_start].append(v_end)
            sources[v_end] = False

        sources = tuple([i for i in range(n) if sources[i]])
        return adj_list, sources

    def topological_sort(self):
        visited = [False for _ in range(self.n)]
        res = []
        for source in self.sources:
            # print(source+1)
            self.dfs(source, visited, res)

        res = list(reversed(res))
        res = [a+1 for a in res]
        return res

    def dfs(self, source, visited, res):
        for child in self.adj_list[source]:
            if not visited[child]:
                self.dfs(child, visited, res)
        visited[source] = True
        res.append(source)


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    graph = Graph(n, m, edges)
    print(" ".join(map(str, graph.topological_sort())))


def run_test():
    n, m = 4, 3
    edges = (
        (1, 2),
        (4, 1),
        (3, 1),
    )
    graph = Graph(n, m, edges)
    print(" ".join(map(str, graph.topological_sort())))


if __name__ == "__main__":
    # run_test()
    run_algo()
