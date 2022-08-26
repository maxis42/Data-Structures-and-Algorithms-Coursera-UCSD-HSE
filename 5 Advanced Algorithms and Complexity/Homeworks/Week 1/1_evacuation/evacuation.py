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

    def max_flow(self, start, end):
        graph_r = deepcopy(self)
        for i in range(len(graph_r.edges) // 2):
            graph_r.edges[i * 2].flow = graph_r.edges[i * 2].capacity

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

        return flow


def run_algo():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)

    print(graph.max_flow(0, vertex_count - 1))


def run_test():
    n = 5
    edges = (
        (1, 2, 2),
        (2, 5, 5),
        (1, 3, 6),
        (3, 4, 2),
        (4, 5, 1),
        (3, 2, 3),
        (2, 4, 1),
    )
    graph = FlowGraph(n)
    for edge in edges:
        start = edge[0] - 1
        end = edge[1] - 1
        capacity = edge[2]
        graph.add_edge(start, end, capacity)

    print(graph.max_flow(0, n - 1))


if __name__ == "__main__":
    # run_test()
    run_algo()
