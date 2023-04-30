# Uses python3
import sys
from collections import namedtuple
from typing import List


Test = namedtuple("Test", "n m edges ans")


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

    def dfs(self, v, visited, dfs_order):
        visited[v] = True
        for child, _ in self.adj_list[v]:
            if not visited[child]:
                self.dfs(child, visited, dfs_order)
        dfs_order.append(v)

    def find_strongly_connected_components(self):
        dfs_order = []
        visited = [False for _ in range(self.num_vertices)]
        for v in range(self.num_vertices):
            if not visited[v]:
                self.dfs(v, visited, dfs_order)

        reversed_edges = [Edge(edge.v_end, edge.v_start, edge.weight) for edge in self.edges]
        reversed_graph = Graph(self.num_vertices, self.num_edges, reversed_edges)

        # strongly connected components
        scc = []
        visited = [False for _ in range(self.num_vertices)]
        while dfs_order:
            cur = dfs_order.pop()

            if not visited[cur]:
                component = []
                reversed_graph.dfs(cur, visited, component)
                scc.append(component)
        return scc

    def has_negative_cycles_multiple_scc(self):
        negative_cycles = False

        scc = self.find_strongly_connected_components()
        scc = [set(comp) for comp in scc]

        dist = [sys.maxsize for _ in range(self.num_vertices)]

        for comp in scc:
            # start vertex
            dist[list(comp)[0]] = 0

        edges_between_scc = set()
        for edge in self.edges:
            scc_start = None
            scc_end = None
            for i, comp in enumerate(scc):
                if edge.v_start in comp:
                    scc_start = i
                if edge.v_end in comp:
                    scc_end = i
            if scc_start != scc_end:
                edges_between_scc.add((edge.v_start, edge.v_end))

        for i in range(self.num_vertices):
            for edge in self.edges:
                if (edge.v_start, edge.v_end) not in edges_between_scc:
                    cur_dist = dist[edge.v_end]
                    new_dist = dist[edge.v_start] + edge.weight
                    if new_dist < cur_dist:
                        dist[edge.v_end] = new_dist

                        if i == (self.num_vertices - 1):
                            # change in distance during the last iteration
                            negative_cycles = True
                            break

        return negative_cycles

    def has_negative_cycles_one_scc(self):
        dist = [sys.maxsize for _ in range(self.num_vertices)]
        dist[0] = 0

        negative_cycles = False

        for i in range(self.num_vertices):
            for edge in self.edges:
                cur_dist = dist[edge.v_end]
                new_dist = dist[edge.v_start] + edge.weight
                if new_dist < cur_dist:
                    dist[edge.v_end] = new_dist

                    if i == (self.num_vertices - 1):
                        # change in distance during the last iteration
                        negative_cycles = True
                        break

        return negative_cycles


def run_algo():
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0:2]
    data = data[2:]
    edges_ = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    edges = []
    for ((a, b), w) in edges_:
        edges.append(Edge(a - 1, b - 1, w))

    graph = Graph(n, m, edges)
    print(1 if graph.has_negative_cycles_one_scc() else 0)


def run_test():
    # test = Test(
    #     n=9,
    #     m=7,
    #     edges=[
    #         Edge(0, 1, 2),
    #         Edge(1, 2, 3),
    #         Edge(2, 0, 1),
    #         Edge(3, 0, 15),
    #         Edge(3, 5, -5),
    #         Edge(5, 4, 2),
    #         Edge(4, 3, 1),
    #         # Edge(6, 7, -10),
    #         # Edge(7, 8, 10),
    #         # Edge(8, 6, -1),
    #     ],
    #     ans=1,
    # )
    # test = Test(
    #     n=2,
    #     m=1,
    #     edges=[
    #         Edge(1, 0, -10)
    #     ],
    #     ans=0
    # )
    test = Test(
        n=4,
        m=4,
        edges=[
            Edge(0, 1, 1),
            Edge(3, 0, 2),
            Edge(1, 2, 2),
            Edge(2, 0, -5),
        ],
        ans=1,
    )

    graph = Graph(test.n, test.m, test.edges)
    ans = 1 if graph.has_negative_cycles_one_scc() else 0
    print(ans)
    assert ans == test.ans, f"Answer: {ans}\nExpected: {test.ans}"


if __name__ == "__main__":
    # run_test()
    run_algo()
