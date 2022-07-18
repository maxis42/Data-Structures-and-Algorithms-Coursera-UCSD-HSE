# Uses python3
import sys
from collections import namedtuple, deque
from typing import List


Test = namedtuple("Test", "n m edges s")


class Vertex:
    def __init__(self, vertex, dist):
        self.vertex = vertex
        self.dist = dist


class Edge:
    def __init__(self, v_start, v_end, weight):
        self.v_start = v_start
        self.v_end = v_end
        self.weight = weight


class Graph:
    def __init__(self, num_vertices: int, num_edges: int, edges: List[Edge]):
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.edges = edges

        self.adj_list = self.get_adj_list(self.num_vertices, self.edges)

    @staticmethod
    def get_adj_list(num_vertices: int, edges: List[Edge]) -> dict:
        adj_list = {i: [] for i in range(num_vertices)}
        for edge in edges:
            adj_list[edge.v_start].append((edge.v_end, edge.weight))
        return adj_list

    def shortest_dist(self, s):
        dist = [float("inf") for _ in range(self.num_vertices)]
        dist[s] = 0

        for _ in range(self.num_vertices - 1):
            for edge in self.edges:
                cur_dist = dist[edge.v_end]
                new_dist = dist[edge.v_start] + edge.weight
                if new_dist < cur_dist:
                    dist[edge.v_end] = new_dist

        neg_inf_vertices_sources = set()

        for edge in self.edges:
            cur_dist = dist[edge.v_end]
            new_dist = dist[edge.v_start] + edge.weight
            if new_dist < cur_dist:
                neg_inf_vertices_sources.add(edge.v_start)

        # find all negative inf vertices
        neg_inf_vertices = set()
        neg_inf_vertices_sources = deque(neg_inf_vertices_sources)
        visited = [False for _ in range(self.num_vertices)]
        while neg_inf_vertices_sources:
            cur = neg_inf_vertices_sources.popleft()
            visited[cur] = True
            neg_inf_vertices.add(cur)
            for child, _ in self.adj_list[cur]:
                if not visited[child]:
                    neg_inf_vertices_sources.append(child)

        ans = []
        for i in range(self.num_vertices):
            if i in neg_inf_vertices:
                # distance from s to u is -inf
                ans.append("-")
            elif dist[i] == float("inf"):
                # no path from s to u
                ans.append("*")
            else:
                # output shortest distance
                ans.append(dist[i])

        return ans


def run_algo():
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0:2]
    data = data[2:]
    edges_ = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    edges = []
    for ((a, b), w) in edges_:
        edges.append(Edge(a - 1, b - 1, w))
    data = data[3 * m:]
    s = data[0] - 1

    graph = Graph(n, m, edges)
    ans = graph.shortest_dist(s)
    for a in ans:
        print(a)


def run_test():
    test = Test(
        n=6,
        m=7,
        edges=[
            Edge(0, 1, 10),
            Edge(1, 2, 5),
            Edge(0, 2, 100),
            Edge(2, 4, 7),
            Edge(4, 3, 10),
            Edge(3, 2, -18),
            Edge(5, 0, -1),
        ],
        s=0,
    )
    # test = Test(
    #     n=5,
    #     m=4,
    #     edges=[
    #         Edge(0, 1, 1),
    #         Edge(3, 0, 2),
    #         Edge(1, 2, 2),
    #         Edge(2, 0, -5),
    #     ],
    #     s=3,
    # )
    # test = Test(
    #     n=2,
    #     m=0,
    #     edges=[
    #     ],
    #     s=1,
    # )
    # test = Test(
    #     n=5,
    #     m=7,
    #     edges=[
    #         Edge(0, 1, 40),
    #         Edge(2, 1, 4),
    #         Edge(1, 3, -2),
    #         Edge(3, 2, -3),
    #         Edge(2, 4, 2),
    #         Edge(0, 3, 3),
    #         Edge(3, 4, 1),
    #     ],
    #     s=0,
    # )
    graph = Graph(test.n, test.m, test.edges)
    ans = graph.shortest_dist(test.s)
    for a in ans:
        print(a)


if __name__ == "__main__":
    # run_test()
    run_algo()
