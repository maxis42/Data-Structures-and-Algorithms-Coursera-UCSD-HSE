# python3
from copy import deepcopy
from collections import deque


class Edge:
    def __init__(self, start, end, capacity):
        self.start = start
        self.end = end
        self.capacity = capacity

        self.flow = 0

    def __str__(self):
        s = "Edge(start={}, end={}, capacity={}, flow={})"\
            .format(self.start + 1, self.end + 1, self.capacity, self.flow)
        return s

    def __repr__(self):
        s = "\nEdge(start={}, end={}, capacity={}, flow={})"\
            .format(self.start + 1, self.end + 1, self.capacity, self.flow)
        return s


class FlowGraph:
    """
    This class implements an unusual scheme for storing
    edges of the graph, in order to retrieve the backward
    edge for a given edge quickly.
    """

    def __init__(self, n):
        self.n = n
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges
        # in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, start, end, capacity):
        # Note that we first append a forward edge and then
        # a backward edge, so all forward edges are stored
        # at even indices (starting from 0), whereas
        # backward edges are stored at odd indices.
        forward_edge = Edge(start, end, capacity)
        backward_edge = Edge(end, start, 0)
        self.graph[start].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[end].append(len(self.edges))
        self.edges.append(backward_edge)

    def find_shortest_path(self, start, end):
        parent = [None] * self.n

        processed = [False] * self.n
        processed[start] = True

        q = deque([start])
        while q:
            cur = q.popleft()

            if cur == end:
                break

            for edge_id in self.graph[cur]:
                edge = self.edges[edge_id]
                if (not processed[edge.end]) and (edge.flow > 0):
                    q.append(edge.end)
                    parent[edge.end] = (edge_id, edge)
                    processed[edge.end] = True

        path = []
        if parent[end] is not None:
            next_node = end
            while next_node != start:
                edge_id, edge = parent[next_node]
                path.append((edge_id, edge))
                next_node = edge.start

            path = path[::-1]
        return path

    def maximize_flow(self, start, end):
        graph_r = deepcopy(self)
        for i in range(len(graph_r.edges) // 2):
            graph_r.edges[i * 2].flow = graph_r.edges[i * 2].capacity

        # edge.flow assumed to represent its capacity
        # (incorrect attributes naming)

        flow = 0
        while True:
            # find the shortest path in residuals graph
            path = graph_r.find_shortest_path(start, end)
            if not path:
                break

            # find min flow through the path
            min_flow = path[0][1].flow
            for _, edge in path[1:]:
                min_flow = min(min_flow, edge.flow)

            # update graphs
            for edge_id, _ in path:
                if edge_id % 2 == 0:
                    self.edges[edge_id].flow += min_flow

                    graph_r.edges[edge_id].flow -= min_flow
                    graph_r.edges[edge_id + 1].flow += min_flow
                else:
                    self.edges[edge_id - 1].flow -= min_flow

                    graph_r.edges[edge_id - 1].flow -= min_flow
                    graph_r.edges[edge_id].flow += min_flow

            # update flow
            flow += min_flow


class BipartiteGraphMatching:
    # 0 - source
    # n + m + 1 - stock
    # [1, n] - left nodes
    # [n + 1, n + m] - right nodes

    def __init__(self, n, m):
        self.n = n  # left part
        self.m = m  # right part

        self.graph = FlowGraph(n + m + 2)
        # add edges between source '0' and left nodes with unit capacity
        for i in range(self.n):
            self.graph.add_edge(start=0,
                                end=i + 1,
                                capacity=1)
        # add edges between right nodes and stock 'n + m + 1' with unit capacity
        for i in range(self.m):
            self.graph.add_edge(start=self.n + 1 + i,
                                end=self.n + self.m + 1,
                                capacity=1)

    def maximize_matching(self):
        self.graph.maximize_flow(0, self.n + self.m + 1)

        matches = [-1] * self.n
        for i in range(len(self.graph.edges) // 2):
            edge = self.graph.edges[i * 2]
            if (edge.start != 0) \
                    and (edge.end != self.n + self.m + 1) \
                    and (edge.flow == 1):
                cur_flight = edge.start - 1
                cur_crew = edge.end - self.n
                matches[cur_flight] = cur_crew
        return matches


def run_test():
    num_flights, num_crews = 3, 4
    timetable = [
        (1, 1, 0, 1),
        (0, 1, 0, 0),
        (0, 0, 0, 0),
    ]
    bgm = BipartiteGraphMatching(num_flights, num_crews)
    for i in range(num_flights):
        for j in range(num_crews):
            if timetable[i][j] == 1:
                bgm.graph.add_edge(start=i + 1,
                                   end=num_flights + 1 + j,
                                   capacity=1)
    print(" ".join(map(str, bgm.maximize_matching())))


def run_algo():
    num_flights, num_crews = map(int, input().split())

    bgm = BipartiteGraphMatching(num_flights, num_crews)
    for i in range(num_flights):
        timetable = tuple(map(int, input().split()))
        for j in range(num_crews):
            if timetable[j] == 1:
                bgm.graph.add_edge(start=i + 1,
                                   end=num_flights + 1 + j,
                                   capacity=1)
    print(" ".join(map(str, bgm.maximize_matching())))


if __name__ == "__main__":
    # run_test()
    run_algo()
