# Uses python3
import sys
from collections import namedtuple, deque

Test = namedtuple("Test", "n m u v edges output")


class Graph:
    def __init__(self, n, m, edges):
        self.n = n  # number of vertices
        self.m = m  # number of edges
        self.edges = edges

        self._edges = []
        for v1, v2 in self.edges:
            self._edges.append((v1 - 1, v2 - 1))

        self.adj_list = self.make_adj_list(self.n, self._edges)
        self.connected_components = self.make_connected_components()

    @staticmethod
    def make_adj_list(n, edges):
        adj_list = {i: set() for i in range(n)}
        for v1, v2 in edges:
            adj_list[v1].add(v2)
            adj_list[v2].add(v1)
        return adj_list

    def make_connected_components(self):
        cc = [-1 for _ in range(self.n)]
        visited = [False for _ in range(self.n)]

        cc_i = 0

        for v, neighbours in self.adj_list.items():
            if not visited[v]:
                visited[v] = True
                cc[v] = cc_i

                q = deque(neighbours)
                while q:
                    cur = q.popleft()
                    visited[cur] = True
                    cc[cur] = cc_i
                    for neighbour in self.adj_list[cur]:
                        if not visited[neighbour]:
                            q.append(neighbour)

                cc_i += 1
        return cc

    def has_path(self, v1, v2):
        v1 -= 1
        v2 -= 1

        path_exists = 0
        if self.connected_components[v1] == self.connected_components[v2]:
            path_exists = 1
        return path_exists


def run_tests():
    test = Test(
        n=4, m=4, u=1, v=4,
        edges=((1, 2), (3, 2), (4, 3), (1, 4)),
        output=1
    )
    test = Test(
        n=4, m=3, u=1, v=4,
        edges=((1, 2), (3, 2), (4, 3)),
        output=1
    )
    graph = Graph(test.n, test.m, test.edges)
    assert graph.has_path(test.u, test.v) == test.output
    print("Passed!")


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    x, y = data[2 * m:]

    graph = Graph(n, m, edges)
    print(graph.has_path(x, y))


if __name__ == "__main__":
    # run_tests()
    run_algo()
