#!/usr/bin/python3
import sys
from typing import List, Dict, Set, Tuple
import heapq
from copy import deepcopy
from collections import namedtuple


Test = namedtuple("Test", "n m edges queries")


class Edge:
    def __init__(self, start: int, end: int, weight: int):
        self.start = start
        self.end = end
        self.weight = weight

    def __str__(self):
        return f"Edge(start={self.start}, end={self.end}, weight={self.weight})"

    def __repr__(self):
        return f"Edge(start={self.start}, end={self.end}, weight={self.weight})"

    def same_edge(self, other):
        res = (
            (self.start == other.start)
            and (self.end == other.end)
        )
        return res


class Graph:
    def __init__(self, vertices: List[int], edges: List[Edge]):
        self.vertices = vertices
        self.edges = {(edge.start, edge.end): edge.weight for edge in edges}
        self.adj_list, self.adj_list_r = self._get_adj_list(self.vertices, self.edges)
        self.num_vertices = len(self.vertices)
        self.max_vertex = max(self.vertices)

    @staticmethod
    def _get_adj_list(vertices: List[int], edges: Dict[Tuple[int, int], int])\
            -> (Dict[int, List[Edge]], Dict[int, List[Edge]]):
        adj_list = {i: set() for i in vertices}
        adj_list_r = {i: set() for i in vertices}
        for start, end in edges:
            adj_list[start].add(end)
            adj_list_r[end].add(start)
        return adj_list, adj_list_r

    def reverse_graph(self):
        edges_r = [Edge(end, start, weight) for (start, end), weight in self.edges.items()]
        graph_r = Graph(self.vertices, edges_r)
        return graph_r

    def add_edge(self, edge: Edge):
        if edge.end not in self.adj_list[edge.start]:
            self.edges[(edge.start, edge.end)] = edge.weight
            self.adj_list[edge.start].add(edge.end)
            self.adj_list_r[edge.end].add(edge.start)
        else:
            self.edges[(edge.start, edge.end)] = min(self.edges[(edge.start, edge.end)],
                                                     edge.weight)

    def contract_vertex(self, vertex: int):
        self.vertices.remove(vertex)
        self.num_vertices -= 1

        for v in self.adj_list[vertex]:
            self.adj_list_r[v].remove(vertex)
            del self.edges[(vertex, v)]

        for v in self.adj_list_r[vertex]:
            self.adj_list[v].remove(vertex)
            del self.edges[(v, vertex)]

    def get_predecessors(self, vertex: int) -> Set[int]:
        return self.adj_list_r[vertex]

    def get_successors(self, vertex: int) -> Set[int]:
        return self.adj_list[vertex]


class ContractionHierarchies:
    _inf = 10**9

    def __init__(self, graph: Graph):
        self.graph = graph
        self.graph_r = self.graph.reverse_graph()

        self.graph_aug, self.node_order = self._preprocess()
        self.graph_aug_r = self.graph_aug.reverse_graph()

    def _preprocess(self):
        graph_pre = deepcopy(self.graph)

        node_order = []
        node_order_pq = [(-self._inf, i) for i in range(self.graph.num_vertices)]

        node_level = [0 for _ in range(self.graph.num_vertices)]

        new_edges = []

        while node_order_pq:
            # extract the least important node
            _, node = heapq.heappop(node_order_pq)

            predecessors = graph_pre.get_predecessors(node)
            successors = graph_pre.get_successors(node)

            shortcuts = self.get_shortcuts(graph_pre, predecessors, successors, node)

            new_imp = self._recompute_importance(node, predecessors, successors,
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
            self._contract_node(graph_pre, node, shortcuts)
            new_edges.extend(shortcuts)

        graph_aug = self.graph
        for edge in new_edges:
            graph_aug.add_edge(edge)

        return graph_aug, node_order

    def _recompute_importance(
            self,
            node: int,
            predecessors: Set[int],
            successors: Set[int],
            shortcuts: List[Edge],
            node_order: List[int],
            node_level: List[int],
    ) -> int:
        # edge difference
        num_shortcuts = len(shortcuts)
        in_deg = len(self.graph_r.adj_list[node])
        out_deg = len(self.graph.adj_list[node])
        ed = num_shortcuts - in_deg - out_deg

        # number of contracted neighbors
        cn = len(predecessors.intersection(node_order)) + len(successors.intersection(node_order))

        # shortcut cover - the number of neighbors w of v such
        # that we have to shortcut to or from w after
        # contracting v
        contracted_neighbors = set()
        for edge in shortcuts:
            contracted_neighbors.add(edge.start)
            contracted_neighbors.add(edge.end)
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
    ) -> List[Edge]:
        shortcuts = []

        for predecessor in predecessors:
            # find nodes which can be accessed from predecessor ignoring
            # current node with the distance smaller or equal to the
            # distance from predecessor to this node via current node
            witnesses = self._witness_search(graph, predecessor, node, successors)

            for successor in successors:
                if successor not in witnesses:
                    weight = graph.edges[(predecessor, node)] + graph.edges[(node, successor)]
                    shortcuts.append(Edge(predecessor, successor, weight))

        return shortcuts

    @staticmethod
    def _contract_node(graph: Graph, node: int, shortcuts: List[Edge]):
        graph.contract_vertex(node)

        for edge in shortcuts:
            graph.add_edge(edge)

    def _witness_search(
            self,
            graph: Graph,
            node: int,
            forbidden_node: int,
            successors: Set[int],
            max_hops: int = 1
    ) -> List[int]:
        dist = [self._inf for _ in range(graph.max_vertex + 1)]
        dist[node] = 0
        final = [False for _ in range(graph.max_vertex + 1)]
        pq = [(0, node)]
        hops = [0 for _ in range(graph.max_vertex + 1)]

        # max distance is the distance from the "node" to the farthest successor
        # of "forbidden node" via "forbidden node"
        start_to_forbidden_dist = graph.edges[(node, forbidden_node)]
        forbidden_to_successor_dist = 0
        for v in graph.adj_list[forbidden_node]:
            forbidden_to_successor_dist = max(forbidden_to_successor_dist,
                                              graph.edges[(forbidden_node, v)])
        max_dist = start_to_forbidden_dist + forbidden_to_successor_dist

        while pq:
            cur_dist, cur = heapq.heappop(pq)
            final[cur] = True

            if cur_dist > max_dist:
                break

            for v in graph.adj_list[cur]:
                # we do not want the path through the "forbidden node"
                if (not final[v]) and (v != forbidden_node):
                    new_hops = hops[cur] + 1
                    new_dist = dist[cur] + graph.edges[(cur, v)]
                    if new_dist < dist[v]:
                        hops[cur] = new_hops
                        if new_hops <= max_hops:
                            dist[v] = new_dist
                            heapq.heappush(pq, (new_dist, v))

        witnesses = []
        for i in range(graph.max_vertex + 1):
            if final[i] and (i in successors):
                node_dist = dist[i]
                if node_dist <= (start_to_forbidden_dist + graph.edges[(forbidden_node, i)]):
                    witnesses.append(i)

        return witnesses

    def dist(self, start, end):
        dist_fw = [self._inf for _ in range(self.graph_aug.num_vertices)]
        dist_bw = [self._inf for _ in range(self.graph_aug.num_vertices)]

        dist_fw[start] = 0
        dist_bw[end] = 0

        pq_fw = [(0, start)]
        pq_bw = [(0, end)]

        final_fw = [False for _ in range(self.graph_aug.num_vertices)]
        final_bw = [False for _ in range(self.graph_aug_r.num_vertices)]

        workset = set()

        while pq_fw or pq_bw:
            if pq_fw:
                cur_dist, cur_vertex = heapq.heappop(pq_fw)
                workset.add(cur_vertex)

                if not final_fw[cur_vertex]:
                    final_fw[cur_vertex] = True

                    # stop when the extracted node is farther thane the target
                    if cur_dist > dist_fw[end]:
                        continue

                    # process children
                    for v in self.graph_aug.adj_list[cur_vertex]:
                        if not final_fw[v]:
                            new_dist = cur_dist + self.graph_aug.edges[(cur_vertex, v)]
                            if new_dist < dist_fw[v]:
                                dist_fw[v] = new_dist
                                heapq.heappush(pq_fw, (new_dist, v))

            if pq_bw:
                cur_dist, cur_vertex = heapq.heappop(pq_bw)
                workset.add(cur_vertex)

                if not final_bw[cur_vertex]:
                    final_bw[cur_vertex] = True

                    # stop when the extracted node is farther thane the target
                    if cur_dist > dist_bw[end]:
                        continue

                    # process children
                    for v in self.graph_aug_r.adj_list[cur_vertex]:
                        if not final_bw[v]:
                            new_dist = cur_dist + self.graph_aug_r.edges[(cur_vertex, v)]
                            if new_dist < dist_bw[v]:
                                dist_bw[v] = new_dist
                                heapq.heappush(pq_bw, (new_dist, v))

        res = self._calculate_mid_dist(workset, dist_fw, dist_bw)
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
        edges=(
            Edge(0, 1, 1),
            Edge(3, 0, 2),
            Edge(1, 2, 2),
            Edge(0, 2, 5),
        ),
        queries=(
            (0, 2, 3),
        )
    )

    test = Test(
        n=2,
        m=1,
        edges=(
            Edge(0, 1, 1),
        ),
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

    graph = Graph(list(range(test.n)), list(test.edges))
    ch = ContractionHierarchies(graph)

    print(f"Node order: {ch.node_order}")
    print(f"Augmented graph: {ch.graph_aug.adj_list}")
    print()

    for i in range(len(test.queries)):
        start, end, ans = test.queries[i]
        print(f"True: {ans}, ans: {ch.dist(start, end)}")


def run_algo():
    num_vertices, num_edges = map(int, sys.stdin.readline().split())

    edges = []
    for _ in range(num_edges):
        start, end, weight = map(int, sys.stdin.readline().split())
        start, end = start - 1, end - 1
        edges.append(Edge(start, end, weight))

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
