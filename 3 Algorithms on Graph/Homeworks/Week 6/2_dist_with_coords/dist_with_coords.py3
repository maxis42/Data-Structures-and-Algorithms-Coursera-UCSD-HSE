#!/usr/bin/python3
import sys
import heapq
from math import sqrt
from typing import List, Dict
from collections import namedtuple


Test = namedtuple("Test", "n m nodes edges queries")


class Node:
    def __init__(self, id_: int, x: int, y: int):
        self.id_ = id_
        self.x = x
        self.y = y


class Edge:
    def __init__(self, start: Node, end: Node, length: int):
        self.start = start
        self.end = end
        self.length = length


class AStar:
    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = nodes
        self.edges = edges

        self.num_vertices = len(self.nodes)
        self.num_edges = len(self.edges)

        # all distances in the graph are smaller
        self._inf = self.num_vertices * 10 ** 6

        self.adj = self.get_adj(self.num_vertices, self.edges)

    @staticmethod
    def get_adj(num_vertices: int, edges: List[Edge]) -> Dict[int, List[Edge]]:
        adj = {i: [] for i in range(num_vertices)}
        for edge in edges:
            adj[edge.start.id_].append(edge)
        return adj

    @staticmethod
    def pf(current: Node, end: Node) -> float:
        res = sqrt((end.x - current.x)**2 + (end.y - current.y)**2)
        return res

    def dist(self, start, end):
        ans = -1

        pot = [self._inf for _ in range(self.num_vertices)]
        dist = [self._inf for _ in range(self.num_vertices)]
        final = [False for _ in range(self.num_vertices)]
        pot[start] = 0
        dist[start] = 0

        pq = [(0, start)]
        while pq:
            _, cur = heapq.heappop(pq)
            final[cur] = True

            if cur == end:
                ans = int(dist[cur])
                break

            for edge in self.adj[cur]:
                if not final[edge.end.id_]:
                    new_dist = dist[cur] + edge.length
                    new_pot = new_dist + self.pf(self.nodes[edge.end.id_], self.nodes[end])
                    if new_dist < dist[edge.end.id_]:
                        dist[edge.end.id_] = new_dist
                    if new_pot < pot[edge.end.id_]:
                        pot[edge.end.id_] = new_pot
                        heapq.heappush(pq, (new_pot, edge.end.id_))

        return ans


def run_test():
    test = Test(
        n=2,
        m=1,
        nodes=(
            (0, 0),
            (0, 1),
        ),
        edges=(
            (1, 2, 1),
        ),
        queries=(
            (1, 1, 0),
            (2, 2, 0),
            (1, 2, 1),
            (2, 1, -1),
        )
    )

    test = Test(
        n=4,
        m=4,
        nodes=(
            (0, 0),
            (0, 1),
            (2, 1),
            (2, 0),
        ),
        edges=(
            (1, 2, 1),
            (4, 1, 2),
            (2, 3, 2),
            (1, 3, 6),
        ),
        queries=(
            (1, 3, 3),
        )
    )

    test = Test(
        n=18,
        m=36,
        nodes=(
            (-74258291, 40695601),
            (-74259991, 40694901),
            (-74257543, 40695865),
            (-74260991, 40694301),
            (-74256591, 40696201),
            (-74261991, 40694501),
            (-74261391, 40694201),
            (-74259891, 40694101),
            (-74254991, 40696501),
            (-74262191, 40694601),
            (-74263591, 40693401),
            (-74259091, 40695901),
            (-74262491, 40693501),
            (-74258091, 40693501),
            (-74254887, 40696033),
            (-74254891, 40697301),
            (-74253490, 40697001),
            (-74262591, 40694701),
        ),
        edges=(
            (1, 2, 1839),
            (1, 3, 794),
            (2, 4, 1167),
            (2, 1, 1839),
            (3, 1, 794),
            (3, 5, 1010),
            (4, 6, 1020),
            (4, 2, 1167),
            (4, 7, 413),
            (4, 8, 1119),
            (5, 9, 1628),
            (5, 3, 1010),
            (6, 10, 224),
            (6, 11, 1942),
            (6, 4, 1020),
            (6, 12, 3221),
            (7, 4, 413),
            (7, 13, 1304),
            (8, 4, 1119),
            (8, 14, 1898),
            (9, 15, 480),
            (9, 16, 807),
            (9, 5, 1628),
            (9, 17, 1583),
            (10, 18, 413),
            (10, 6, 224),
            (10, 12, 3362),
            (11, 6, 1942),
            (12, 10, 3362),
            (12, 6, 3221),
            (13, 7, 1304),
            (14, 8, 1898),
            (15, 9, 480),
            (16, 9, 807),
            (17, 9, 1583),
            (18, 10, 413),
        ),
        queries=(
            (2, 17, 6854),
            (10, 8, 2363),
            (6, 8, 2139),
            (11, 13, 4679),
            (16, 2, 6078),
            (15, 14, 9935),
            (15, 8, 8037),
            (6, 5, 5830),
            (7, 1, 3419),
            (17, 11, 10983),
        )
    )

    nodes = []
    for i in range(test.n):
        nodes.append(Node(i, test.nodes[i][0], test.nodes[i][1]))

    edges = []
    for i in range(test.m):
        edges.append(Edge(nodes[test.edges[i][0] - 1], nodes[test.edges[i][1] - 1], test.edges[i][2]))

    astar = AStar(nodes, edges)

    for i in range(len(test.queries)):
        start, end, ans = test.queries[i]
        start, end = start - 1, end - 1
        res = astar.dist(start, end)
        print(ans, res)


def run_algo():
    num_vertices, num_edges = map(int, sys.stdin.readline().split())

    nodes = []
    for i in range(num_vertices):
        x, y = map(int, sys.stdin.readline().split())
        nodes.append(Node(i, x, y))

    edges = []
    for _ in range(num_edges):
        start, end, length = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        edges.append(Edge(nodes[start], nodes[end], length))

    astar = AStar(nodes, edges)

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        start, end = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        print(astar.dist(start, end))


if __name__ == "__main__":
    run_algo()
    # run_test()
