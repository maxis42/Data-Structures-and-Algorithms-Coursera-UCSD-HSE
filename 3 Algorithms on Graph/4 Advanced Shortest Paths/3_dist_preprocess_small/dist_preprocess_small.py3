#!/usr/bin/python3
import sys
from typing import List, Dict, Set, Tuple
import heapq
from copy import deepcopy
from collections import namedtuple


Test = namedtuple("Test", "n m edges queries")


class Graph:
    def __init__(
            self,
            vertices: List[int],
            edges: Dict[Tuple[int, int], int],
            adj_list: Dict[int, Set[int]] = None,
            adj_list_r: Dict[int, Set[int]] = None,
            num_vertices: int = None,
            max_vertex: int = None,
    ):
        self.vertices = vertices
        self.edges = edges

        self.adj_list, self.adj_list_r = adj_list, adj_list_r
        if (adj_list is None) or (adj_list_r is None):
            self.adj_list, self.adj_list_r = self._get_adj_list(self.vertices, self.edges)

        self.num_vertices = num_vertices
        if self.num_vertices is None:
            self.num_vertices = len(self.vertices)

        self.max_vertex = max_vertex
        if self.max_vertex is None:
            self.max_vertex = max(self.vertices)

    @staticmethod
    def _get_adj_list(vertices: List[int], edges: Dict[Tuple[int, int], int])\
            -> (Dict[int, Set[int]], Dict[int, Set[int]]):
        adj_list = dict()
        adj_list_r = dict()

        for i in vertices:
            adj_list[i] = set()
            adj_list_r[i] = set()

        for start, end in edges:
            adj_list[start].add(end)
            adj_list_r[end].add(start)
        return adj_list, adj_list_r

    def reverse_graph(self):
        edges_r = {(end, start): weight for (start, end), weight in self.edges.items()}
        graph_r = Graph(
            self.vertices,
            edges_r,
            self.adj_list_r,
            self.adj_list,
            self.num_vertices,
            self.max_vertex,
        )
        return graph_r

    def add_edge(self, start, end, weight):
        if (start, end) not in self.edges:
            self.edges[(start, end)] = weight
            self.adj_list[start].add(end)
            self.adj_list_r[end].add(start)
        else:
            self.edges[(start, end)] = min(self.edges[(start, end)], weight)

    def contract_vertex(self, vertex: int):
        self.vertices.remove(vertex)
        self.num_vertices -= 1

        for v in self.adj_list[vertex]:
            self.adj_list_r[v].remove(vertex)
            del self.edges[(vertex, v)]

        for v in self.adj_list_r[vertex]:
            self.adj_list[v].remove(vertex)
            del self.edges[(v, vertex)]

        del self.adj_list[vertex]
        del self.adj_list_r[vertex]

    def get_predecessors(self, vertex: int) -> Set[int]:
        return self.adj_list_r[vertex]

    def get_successors(self, vertex: int) -> Set[int]:
        return self.adj_list[vertex]


class ContractionHierarchies:
    _inf = 10**9

    def __init__(self, graph: Graph):
        self._dist = [self._inf for _ in range(graph.num_vertices)]
        self._final = [False for _ in range(graph.num_vertices)]
        self._hops = [0 for _ in range(graph.num_vertices)]

        self.graph_aug, self.node_order = self._preprocess(graph)
        self.graph_aug_r = self.graph_aug.reverse_graph()

        self.node_order = {node: i for i, node in enumerate(self.node_order)}

        self._dist_fw = [self._inf for _ in range(self.graph_aug.num_vertices)]
        self._dist_bw = [self._inf for _ in range(self.graph_aug_r.num_vertices)]
        self._final_fw = [False for _ in range(self.graph_aug.num_vertices)]
        self._final_bw = [False for _ in range(self.graph_aug_r.num_vertices)]

    def _preprocess(self, graph: Graph) -> Tuple[Graph, List[int]]:
        graph_aug = deepcopy(graph)

        node_order = []
        node_order_pq = [(-self._inf, i) for i in range(graph.num_vertices)]

        node_level = [0 for _ in range(graph.num_vertices)]

        new_edges = []

        while node_order_pq:
            # extract the least important node
            _, node = heapq.heappop(node_order_pq)

            predecessors = graph.get_predecessors(node)
            successors = graph.get_successors(node)

            shortcuts = self.get_shortcuts(graph, predecessors, successors, node)

            new_imp = self._recompute_importance(graph, node, predecessors, successors,
                                                 shortcuts, node_order, node_level)

            # if new importance is not minimal anymore (compare with the top of the
            # priority queue), put it back into priority queue with the new priority
            # otherwise, contract the node
            if node_order_pq:
                next_imp, _ = node_order_pq[0]
                if new_imp > next_imp:
                    heapq.heappush(node_order_pq, (new_imp, node))
                    continue

            node_order.append(node)

            for predecessor in predecessors:
                node_level[predecessor] = max(node_level[predecessor], node_level[node] + 1)

            self._contract_node(graph, node, shortcuts)
            new_edges.extend(shortcuts)

        for start, end, weight in new_edges:
            graph_aug.add_edge(start, end, weight)

        return graph_aug, node_order

    @staticmethod
    def _recompute_importance(
            graph: Graph,
            node: int,
            predecessors: Set[int],
            successors: Set[int],
            shortcuts: List,
            node_order: List[int],
            node_level: List[int],
    ) -> int:
        # edge difference
        num_shortcuts = len(shortcuts)
        in_deg = len(graph.adj_list_r[node])
        out_deg = len(graph.adj_list[node])
        ed = num_shortcuts - in_deg - out_deg

        # number of contracted neighbors
        cn = len(predecessors.intersection(node_order)) + len(successors.intersection(node_order))

        # shortcut cover - the number of neighbors w of v such
        # that we have to shortcut to or from w after
        # contracting v
        contracted_neighbors = set()
        for start, end, _ in shortcuts:
            contracted_neighbors.add(start)
            contracted_neighbors.add(end)
        sc = len(contracted_neighbors)

        # node level - upper bound on the number of edges in
        # the shortest path from any s to v in the augmented
        # graph
        nl = node_level[node]

        importance = ed + cn + sc + nl
        return importance

    def get_shortcuts(
            self,
            graph: Graph,
            predecessors: Set[int],
            successors: Set[int],
            node: int
    ) -> List:
        shortcuts = []

        for predecessor in predecessors:
            # find nodes which can be accessed from predecessor ignoring
            # current node with the distance smaller or equal to the
            # distance from predecessor to this node via current node
            witnesses = self._witness_search(graph, predecessor, node, successors, max_hops=2)

            for successor in successors:
                if successor not in witnesses:
                    weight = graph.edges[(predecessor, node)] + graph.edges[(node, successor)]
                    shortcuts.append((predecessor, successor, weight))

        return shortcuts

    @staticmethod
    def _contract_node(graph: Graph, node: int, shortcuts: List):
        graph.contract_vertex(node)

        for start, end, weight in shortcuts:
            graph.add_edge(start, end, weight)

    def _witness_search(
            self,
            graph: Graph,
            predecessor: int,
            node: int,
            successors: Set[int],
            max_hops: int = 1
    ) -> List[int]:
        self._dist[predecessor] = 0
        pq = [(0, predecessor)]
        processed = set()
        processed.add(predecessor)

        # max distance is the distance from the "node" to the farthest successor
        # of "forbidden node" via "forbidden node"
        start_to_forbidden_dist = graph.edges[(predecessor, node)]
        forbidden_to_successor_dist = 0
        for v in graph.adj_list[node]:
            forbidden_to_successor_dist = max(forbidden_to_successor_dist,
                                              graph.edges[(node, v)])
        max_dist = start_to_forbidden_dist + forbidden_to_successor_dist

        while pq:
            cur_dist, cur = heapq.heappop(pq)
            self._final[cur] = True

            if cur_dist > max_dist:
                break

            for v in graph.adj_list[cur]:
                # we do not want the path through the "forbidden node"
                if (not self._final[v]) and (v != node):
                    new_hops = self._hops[cur] + 1
                    new_dist = self._dist[cur] + graph.edges[(cur, v)]
                    if new_dist < self._dist[v]:
                        self._hops[cur] = new_hops
                        if new_hops <= max_hops:
                            self._dist[v] = new_dist
                            heapq.heappush(pq, (new_dist, v))
                            processed.add(v)

        witnesses = []
        for i in successors:
            if self._final[i]:
                if self._dist[i] <= (start_to_forbidden_dist + graph.edges[(node, i)]):
                    witnesses.append(i)

        for node in processed:
            self._dist[node] = self._inf
            self._final[node] = False
            self._hops[node] = 0

        return witnesses

    def dist(self, start, end):
        self._dist_fw[start] = 0
        self._dist_bw[end] = 0

        pq_fw = [(0, start)]
        pq_bw = [(0, end)]

        workset = set()

        estimate = self._inf

        while pq_fw or pq_bw:
            if pq_fw:
                cur_dist, cur_vertex = heapq.heappop(pq_fw)
                workset.add(cur_vertex)

                if self._final_bw[cur_vertex]:
                    estimate = min(estimate, cur_dist + self._dist_bw[cur_vertex])

                if not self._final_fw[cur_vertex]:
                    self._final_fw[cur_vertex] = True

                    # skip node farther than the current estimate
                    if cur_dist > estimate:
                        continue

                    # process children
                    for v in self.graph_aug.adj_list[cur_vertex]:
                        if (not self._final_fw[v]) \
                                and (self.node_order[v] > self.node_order[cur_vertex]):
                            new_dist = cur_dist + self.graph_aug.edges[(cur_vertex, v)]
                            if new_dist < self._dist_fw[v]:
                                self._dist_fw[v] = new_dist
                                heapq.heappush(pq_fw, (new_dist, v))

            if pq_bw:
                cur_dist, cur_vertex = heapq.heappop(pq_bw)
                workset.add(cur_vertex)

                if self._final_fw[cur_vertex]:
                    estimate = min(estimate, cur_dist + self._dist_fw[cur_vertex])

                if not self._final_bw[cur_vertex]:
                    self._final_bw[cur_vertex] = True

                    # skip node farther than the current estimate
                    if cur_dist > estimate:
                        continue

                    # process children
                    for v in self.graph_aug_r.adj_list[cur_vertex]:
                        if (not self._final_bw[v]) \
                                and (self.node_order[v] > self.node_order[cur_vertex]):
                            new_dist = cur_dist + self.graph_aug_r.edges[(cur_vertex, v)]
                            if new_dist < self._dist_bw[v]:
                                self._dist_bw[v] = new_dist
                                heapq.heappush(pq_bw, (new_dist, v))

        res = self._calculate_mid_dist(workset, self._dist_fw, self._dist_bw)

        for node in workset:
            self._dist_fw[node] = self._inf
            self._dist_bw[node] = self._inf
            self._final_fw[node] = False
            self._final_bw[node] = False

        return res

    def _calculate_mid_dist(self, workset, dist_fw, dist_bw):
        res = self._inf

        for i in list(workset):
            res = min(res, dist_fw[i] + dist_bw[i])

        # nodes unreachable
        if res == self._inf:
            res = -1
        return res


def run_test():
    test = Test(
        n=4,
        m=4,
        edges={
            (0, 1): 1,
            (3, 0): 2,
            (1, 2): 2,
            (0, 2): 5,
        },
        queries=(
            (0, 2, 3),
        )
    )

    test = Test(
        n=2,
        m=1,
        edges={
            (0, 1): 1,
        },
        queries=(
            (0, 0, 0),
            (1, 1, 0),
            (0, 1, 1),
            (1, 0, -1),
        )
    )

    test = Test(
        n=5,
        m=20,
        edges={
            (0, 1): 667,
            (0, 2): 677,
            (0, 3): 700,
            (0, 4): 622,
            (1, 0): 118,
            (1, 2): 325,
            (1, 3): 784,
            (1, 4): 11,
            (2, 0): 585,
            (2, 1): 956,
            (2, 3): 551,
            (2, 4): 559,
            (3, 0): 503,
            (3, 1): 722,
            (3, 2): 331,
            (3, 4): 366,
            (4, 0): 880,
            (4, 1): 883,
            (4, 2): 461,
            (4, 3): 228,
        },
        queries=(
            (0, 0, 0),
            (0, 1, 667),
            (0, 2, 677),
            (0, 3, 700),
            (0, 4, 622),
            (1, 0, 118),
            (1, 1, 0),
            (1, 2, 325),
            (1, 3, 239),
            (1, 4, 11),
        )
    )

    graph = Graph(list(range(test.n)), test.edges)
    ch = ContractionHierarchies(graph)

    print(f"Node order: {ch.node_order}")
    print(f"Augmented graph: {ch.graph_aug.adj_list}")
    print()

    for i in range(len(test.queries)):
        start, end, ans = test.queries[i]
        print(f"True: {ans}, ans: {ch.dist(start, end)}")


def run_algo():
    num_vertices, num_edges = map(int, sys.stdin.readline().split())

    edges = dict()
    for _ in range(num_edges):
        start, end, weight = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        edges[(start, end)] = weight

    graph = Graph(list(range(num_vertices)), edges)
    ch = ContractionHierarchies(graph)

    print("Ready")
    sys.stdout.flush()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        start, end = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        print(ch.dist(start, end))


if __name__ == "__main__":
    run_algo()
    # run_test()
