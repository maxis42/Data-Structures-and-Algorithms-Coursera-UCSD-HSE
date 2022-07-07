# Uses python3

import sys

sys.setrecursionlimit(200000)


class Graph:
    def __init__(self, n, m, edges):
        self.n = n  # number of vertices
        self.m = m  # number of edges
        self.edges = edges
        self.adj_list = self.get_adj_list(self.n, self.edges)

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

    def dfs(self, v, visited, dfs_order):
        visited[v] = True
        for child in self.adj_list[v]:
            if not visited[child]:
                self.dfs(child, visited, dfs_order)
        dfs_order.append(v)

    def find_strongly_connected_components(self):
        dfs_order = []
        visited = [False for _ in range(self.n)]
        for v in range(self.n):
            if not visited[v]:
                self.dfs(v, visited, dfs_order)

        reversed_edges = tuple((b+1, a+1) for (a, b) in self.edges)
        reversed_graph = Graph(self.n, self.m, reversed_edges)

        # strongly connected components
        scc = []
        visited = [False for _ in range(self.n)]
        while dfs_order:
            cur = dfs_order.pop()
            component = []

            if not visited[cur]:
                reversed_graph.dfs(cur, visited, component)

            if component:
                scc.append(component)
        return scc


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))

    graph = Graph(n, m, edges)
    print(len(graph.find_strongly_connected_components()))


def run_test():
    n, m = 8, 9
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (2, 4),
        (4, 5),
        (5, 6),
        (6, 4),
        (6, 7),
    )
    edges = tuple((a+1, b+1) for (a, b) in edges)
    graph = Graph(n, m, edges)
    print(graph.find_strongly_connected_components())


if __name__ == "__main__":
    # run_test()
    run_algo()
