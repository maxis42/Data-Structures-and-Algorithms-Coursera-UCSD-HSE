# Uses python3
import sys
from collections import deque, namedtuple

Node = namedtuple("Node", "v level")


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

    def distance(self, v1, v2):
        v1 -= 1
        v2 -= 1

        distance = -1
        q = deque([Node(v1, 0)])
        visited = [False for _ in range(self.n)]
        while q:
            cur, level = q.popleft()
            if cur == v2:
                distance = level
                break

            if not visited[cur]:
                visited[cur] = True
                for child in self.adj_list[cur]:
                    q.append(Node(child, level+1))

        return distance


def run_algo():
    # read data
    data = list(map(int, sys.stdin.read().split()))

    # preprocess data
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(data[0:(2 * m):2], data[1:(2 * m):2]))
    v1, v2 = data[2 * m], data[2 * m + 1]

    graph = Graph(n, edges)
    print(graph.distance(v1, v2))


def run_test():
    n, m = 4, 4
    edges = (
        (1, 2),
        (4, 1),
        (2, 3),
        (3, 1),
    )
    graph = Graph(n, edges)
    print(graph.distance(2, 4))


if __name__ == "__main__":
    # run_test()
    run_algo()
