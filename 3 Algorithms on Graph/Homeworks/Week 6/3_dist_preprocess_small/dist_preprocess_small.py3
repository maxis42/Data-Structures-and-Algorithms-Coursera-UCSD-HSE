#!/usr/bin/python3
import sys
from typing import List, Dict
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
    def __init__(self, vertices: List[int], num_edges: int, edges: List[Edge]):
        self.vertices = vertices
        self.num_edges = num_edges
        self.edges = edges

        self.adj_list, self.adj_list_r = self._get_adj_list(self.vertices, self.edges)
        self.weights = {(edge.start, edge.end): edge.weight for edge in self.edges}
        self.num_vertices = len(self.vertices)

        self.max_vertex = max(self.vertices)

    @staticmethod
    def _get_adj_list(vertices: List[int], edges: List[Edge])\
            -> (Dict[int, List[Edge]], Dict[int, List[Edge]]):
        adj_list = {i: [] for i in vertices}
        adj_list_r = {i: [] for i in vertices}
        for edge in edges:
            adj_list[edge.start].append(edge)
            adj_list_r[edge.end].append(Edge(edge.end, edge.start, edge.weight))
        return adj_list, adj_list_r

    def reverse_graph(self):
        edges_r = [Edge(edge.end, edge.start, edge.weight) for edge in self.edges]
        graph_r = Graph(self.vertices, self.num_edges, edges_r)
        return graph_r

    def add_edge(self, edge: Edge):
        # print(f"Add edge inside: {edge.start, edge.end, edge.weight}")
        if (edge.start, edge.end) not in self.weights:
            self.edges.append(edge)
            self.weights[(edge.start, edge.end)] = edge.weight
            self.adj_list[edge.start].append(edge)
            self.adj_list_r[edge.end].append(Edge(edge.end, edge.start, edge.weight))
            self.num_edges += 1
        else:
            cur_weight = self.weights[(edge.start, edge.end)]
            if edge.weight < cur_weight:
                self.weights[(edge.start, edge.end)] = edge.weight
                self.edges = [e for e in self.edges if not e.same_edge(edge)]
                self.edges.append(edge)
                self.adj_list, self.adj_list_r = self._get_adj_list(self.vertices, self.edges)

    def contract_node(self, node: int):
        self.edges = [edge for edge in self.edges
                      if (edge.start != node) and (edge.end != node)]
        self.weights = {(edge.start, edge.end): edge.weight for edge in self.edges}
        self.num_edges = len(self.edges)

        self.vertices.remove(node)
        self.num_vertices -= 1

        self.adj_list, self.adj_list_r = self._get_adj_list(self.vertices, self.edges)

    def get_predecessors(self, node: int) -> List[int]:
        predecessors = []
        for edge in self.adj_list_r[node]:
            predecessors.append(edge.end)
        return predecessors

    def get_successors(self, node: int) -> List[int]:
        successors = []
        for edge in self.adj_list[node]:
            successors.append(edge.end)
        return successors


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
            # print()
            # print(f"Graph aug: {graph_aug.adj_list}")
            # extract the least important node
            _, node = heapq.heappop(node_order_pq)

            # print(f"Chosen node: {node}")

            predecessors = graph_pre.get_predecessors(node)
            successors = graph_pre.get_successors(node)

            # print(f"Predecessors: {predecessors}")
            # print(f"Successors: {successors}")

            shortcuts = self.get_shortcuts(graph_pre, predecessors, successors, node)

            # print(f"Shortcuts: {shortcuts}")

            new_imp = self._recompute_importance(node, predecessors, successors,
                                                 shortcuts, node_order, node_level)

            # print(f"New importance: {new_imp}")

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

            # break

        # print()
        # print("Out of node order PQ")
        # print(f"New edges: {new_edges}")

        graph_aug = self.graph
        for edge in new_edges:
            graph_aug.add_edge(edge)

        return graph_aug, node_order

    def _recompute_importance(
            self,
            node: int,
            predecessors: List[int],
            successors: List[int],
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
        contracted_nodes = set(node_order)
        cn = len(contracted_nodes.intersection(predecessors)) \
             + len(contracted_nodes.intersection(successors))

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
            predecessors: List[int],
            successors: List[int],
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
                    weight = graph.weights[(predecessor, node)] + graph.weights[(node, successor)]
                    shortcuts.append(Edge(predecessor, successor, weight))

        return shortcuts

    @staticmethod
    def _contract_node(graph: Graph, node: int, shortcuts: List[Edge]):
        # print(f"Contract node: {node}")
        graph.contract_node(node)

        for edge in shortcuts:
            # print(f"Add edge: {edge.start, edge.end, edge.weight}")
            graph.add_edge(edge)

    def _witness_search(
            self,
            graph: Graph,
            node: int,
            forbidden_node: int,
            successors: List[int],
            max_hops: int = 1
    ) -> List[int]:
        # print(f"Start witness search for node: {node}")
        # print(f"Forbidden node: {forbidden_node}")

        dist = [self._inf for _ in range(graph.max_vertex + 1)]
        dist[node] = 0
        final = [False for _ in range(graph.max_vertex + 1)]
        pq = [(0, node)]
        hops = [0 for _ in range(graph.max_vertex + 1)]

        # max distance is the distance from the "node" to the farthest successor
        # of "forbidden node" via "forbidden node"
        start_to_forbidden_dist = graph.weights[(node, forbidden_node)]
        forbidden_to_successor_dist = 0
        for edge in graph.adj_list[forbidden_node]:
            forbidden_to_successor_dist = max(forbidden_to_successor_dist, edge.weight)
        max_dist = start_to_forbidden_dist + forbidden_to_successor_dist
        # print(f"Max dist: {max_dist}")

        while pq:
            cur_dist, cur = heapq.heappop(pq)
            final[cur] = True

            if cur_dist > max_dist:
                break

            for edge in graph.adj_list[cur]:
                # print(edge)
                # we do not want the path through the "forbidden node"
                if (not final[edge.end]) and (edge.end != forbidden_node):
                    # print("Inside 1")
                    new_hops = hops[cur] + 1
                    new_dist = dist[cur] + edge.weight
                    if new_dist < dist[edge.end]:
                        hops[cur] = new_hops
                        if new_hops <= max_hops:
                            dist[edge.end] = new_dist
                            heapq.heappush(pq, (new_dist, edge.end))

        # print(f"Final: {final}")
        # print(f"Dist: {dist}")
        witnesses = []
        for i in range(graph.max_vertex + 1):
            if final[i] and (i in successors):
                node_dist = dist[i]
                if node_dist <= (start_to_forbidden_dist + graph.weights[(forbidden_node, i)]):
                    witnesses.append(i)

        # print(f"Found witnesses: {witnesses}")

        return witnesses

    def dist(self, start, end):
        res = -1

        dist_fw = [self._inf for _ in range(self.graph_aug.num_vertices)]
        dist_bw = [self._inf for _ in range(self.graph_aug.num_vertices)]

        dist_fw[start] = 0
        dist_bw[end] = 0

        pq_fw = [(0, start)]
        pq_bw = [(0, end)]

        final_fw = [False for _ in range(self.graph_aug.num_vertices)]
        final_bw = [False for _ in range(self.graph_aug_r.num_vertices)]

        node_order = {v: order for (order, v) in enumerate(self.node_order)}

        start_order = node_order[start]
        end_order = node_order[end]

        workset = set()

        while pq_fw or pq_bw:
            if pq_fw:
                cur_dist, cur_vertex = heapq.heappop(pq_fw)
                # print(f"Forward pass / node {cur_vertex} / dist {cur_dist}")
                workset.add(cur_vertex)

                if not final_fw[cur_vertex]:
                    final_fw[cur_vertex] = True

                    # stop when the extracted node is farther thane the target
                    if cur_dist > dist_fw[end]:
                        continue

                    # process children
                    for edge in self.graph_aug.adj_list[cur_vertex]:
                        if not final_fw[edge.end]:
                            new_dist = cur_dist + edge.weight
                            if new_dist < dist_fw[edge.end]:
                                dist_fw[edge.end] = new_dist
                                heapq.heappush(pq_fw, (new_dist, edge.end))

            if pq_bw:
                cur_dist, cur_vertex = heapq.heappop(pq_bw)
                # print(f"Backward pass / node {cur_vertex} / dist {cur_dist}")
                workset.add(cur_vertex)

                if not final_bw[cur_vertex]:
                    final_bw[cur_vertex] = True

                    # stop when the extracted node is farther thane the target
                    if cur_dist > dist_bw[end]:
                        continue

                    # process children
                    for edge in self.graph_aug_r.adj_list[cur_vertex]:
                        if not final_bw[edge.end]:
                            new_dist = cur_dist + edge.weight
                            if new_dist < dist_bw[edge.end]:
                                dist_bw[edge.end] = new_dist
                                heapq.heappush(pq_bw, (new_dist, edge.end))

        # print(dist_fw, dist_bw, workset)
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

    # test = Test(
    #     n=5,
    #     m=20,
    #     edges=[
    #         Edge(0, 1, 667),
    #         Edge(0, 2, 677),
    #         Edge(0, 3, 700),
    #         Edge(0, 4, 622),
    #         Edge(1, 0, 118),
    #         Edge(1, 2, 325),
    #         Edge(1, 3, 784),
    #         Edge(1, 4, 11),
    #         Edge(2, 0, 585),
    #         Edge(2, 1, 956),
    #         Edge(2, 3, 551),
    #         Edge(2, 4, 559),
    #         Edge(3, 0, 503),
    #         Edge(3, 1, 722),
    #         Edge(3, 2, 331),
    #         Edge(3, 4, 366),
    #         Edge(4, 0, 880),
    #         Edge(4, 1, 883),
    #         Edge(4, 2, 461),
    #         Edge(4, 3, 228),
    #     ],
    #     queries=(
    #         (0, 0, 0),
    #         (0, 1, 667),
    #         (0, 2, 677),
    #         (0, 3, 700),
    #         (0, 4, 622),
    #         (1, 0, 118),
    #         (1, 1, 0),
    #         (1, 2, 325),
    #         (1, 3, 239),
    #         (1, 4, 11),
    #     )
    # )

    graph = Graph(list(range(test.n)), test.m, list(test.edges))
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

    graph = Graph(list(range(num_vertices)), num_edges, edges)
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
