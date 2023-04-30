#!/usr/bin/python3

import sys
import queue
from collections import namedtuple
import heapq
from typing import Dict, List

VertexWeight = namedtuple("VertexWeight", "id weight")
Test = namedtuple("Test", "n m edges queries")


class Edge:
    def __init__(self, start: int, end: int, weight: int):
        self.start = start
        self.end = end
        self.weight = weight


class BidirectionalDijkstra:
    def __init__(self, num_vertices: int, num_edges: int, edges: List[Edge]):
        self.num_vertices = num_vertices
        self.num_edges = num_edges

        # original graph
        self.edges = edges
        self.adj = self.get_adj(self.num_vertices, self.edges)

        # reversed graph
        self.edges_rev = [Edge(edge.end, edge.start, edge.weight) for edge in edges]
        self.adj_rev = self.get_adj(self.num_vertices, self.edges_rev)

        # all distances in the graph are smaller
        self._inf = self.num_vertices * 10 ** 6

        # initialize distances for forward and backward searches
        self._dist_fw = [self._inf] * self.num_vertices
        self._dist_bw = [self._inf] * self.num_vertices

        self._visited_fw = [False] * self.num_vertices
        self._visited_bw = [False] * self.num_vertices

        # all the nodes visited by forward or backward search
        self._workset = set()

        self._clearset = set()

    @staticmethod
    def get_adj(num_vertices: int, edges: List[Edge]) -> Dict[int, List[VertexWeight]]:
        adj = {i: [] for i in range(num_vertices)}
        for edge in edges:
            adj[edge.start].append(VertexWeight(edge.end, edge.weight))
        return adj

    def clear(self):
        """Reinitialize the data structures for the next query after the previous query."""
        for _ in range(len(self._clearset)):
            v = self._clearset.pop()
            self._dist_fw[v] = self._inf
            self._dist_bw[v] = self._inf
            self._visited_fw[v] = False
            self._visited_bw[v] = False

        self._workset = set()

    def visit(self, q, side, v, dist):
        """Try to relax the distance to node v from direction side by value dist."""
        # Implement this method yourself
        pass

    def min_dist(self, start, end):
        # print(f"start={start} end={end}")
        res = -1

        if start == end:
            res = 0
        else:
            self._dist_fw[start] = 0
            self._dist_bw[end] = 0

            pq_fw = [(0, start)]
            pq_bw = [(0, end)]

            self._clearset.add(start)
            self._clearset.add(end)

            while pq_fw or pq_bw:
                # forward iteration
                if pq_fw:
                    # pop element with the smallest distance
                    _, cur_id = heapq.heappop(pq_fw)
                    self._workset.add(cur_id)

                    # check whether item was already processed by the backward pass
                    if self._visited_bw[cur_id]:
                        res = self._calculate_mid_dist(self._workset, self._dist_fw, self._dist_bw)
                        break

                    if not self._visited_fw[cur_id]:
                        self._visited_fw[cur_id] = True

                        # process children
                        for vertex in self.adj[cur_id]:
                            if not self._visited_fw[vertex.id]:
                                new_dist = self._dist_fw[cur_id] + vertex.weight
                                if new_dist < self._dist_fw[vertex.id]:
                                    self._dist_fw[vertex.id] = new_dist
                                    heapq.heappush(pq_fw, (new_dist, vertex.id))
                                    self._clearset.add(vertex.id)

                # backward iteration
                if pq_bw:
                    # pop element with the smallest distance
                    _, cur_id = heapq.heappop(pq_bw)
                    self._workset.add(cur_id)

                    # check whether item was already processed by the forward pass
                    if self._visited_fw[cur_id]:
                        res = self._calculate_mid_dist(self._workset, self._dist_fw, self._dist_bw)
                        break

                    if not self._visited_bw[cur_id]:
                        self._visited_bw[cur_id] = True

                        # process children
                        for vertex in self.adj_rev[cur_id]:
                            if not self._visited_fw[vertex.id]:
                                new_dist = self._dist_bw[cur_id] + vertex.weight
                                if new_dist < self._dist_bw[vertex.id]:
                                    self._dist_bw[vertex.id] = new_dist
                                    heapq.heappush(pq_bw, (new_dist, vertex.id))
                                    self._clearset.add(vertex.id)

            self.clear()

        return res

    def _calculate_mid_dist(self, workset, dist_fw, dist_bw):
        res = self._inf

        for i in list(workset):
            res = min(res, dist_fw[i] + dist_bw[i])

        # nodes unreachable
        if res == self._inf:
            res = -1
        return res


def run_algo():
    num_vertices, num_edges = map(int, sys.stdin.readline().split())

    edges = []
    for i in range(num_edges):
        start, end, weight = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        edges.append(Edge(start, end, weight))

    num_queries = int(sys.stdin.readline())

    bidij = BidirectionalDijkstra(num_vertices, num_queries, edges)
    for i in range(num_queries):
        start, end = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        print(bidij.min_dist(start, end))


def run_tests():
    test = Test(
        n=2,
        m=1,
        edges=[
            Edge(0, 1, 1),
        ],
        queries=(
            (0, 0),
            (1, 1),
            (0, 1),
            (1, 0),
        )
    )

    # test = Test(
    #     n=4,
    #     m=4,
    #     edges=[
    #         Edge(0, 1, 1),
    #         Edge(3, 0, 2),
    #         Edge(1, 2, 2),
    #         Edge(0, 2, 5),
    #     ],
    #     queries=(
    #         # (0, 2),
    #         # (0, 3),
    #         (3, 2),
    #         # (2, 3),
    #     )
    # )

    # test = Test(
    #     n=2,
    #     m=0,
    #     edges=[
    #     ],
    #     queries=((0, 1),),
    # )

    test = Test(
        n=5,
        m=20,
        edges=[
            Edge(0, 1, 667),
            Edge(0, 2, 677),
            Edge(0, 3, 700),
            Edge(0, 4, 622),
            Edge(1, 0, 118),
            Edge(1, 2, 325),
            Edge(1, 3, 784),
            Edge(1, 4, 11),
            Edge(2, 0, 585),
            Edge(2, 1, 956),
            Edge(2, 3, 551),
            Edge(2, 4, 559),
            Edge(3, 0, 503),
            Edge(3, 1, 722),
            Edge(3, 2, 331),
            Edge(3, 4, 366),
            Edge(4, 0, 880),
            Edge(4, 1, 883),
            Edge(4, 2, 461),
            Edge(4, 3, 228),
        ],
        queries=(
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (0, 4),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (1, 4),
        )
    )

    bidij = BidirectionalDijkstra(test.n, test.m, test.edges)
    for i in range(len(test.queries)):
        print(bidij.min_dist(test.queries[i][0], test.queries[i][1]))


if __name__ == "__main__":
    run_algo()
    # run_tests()
