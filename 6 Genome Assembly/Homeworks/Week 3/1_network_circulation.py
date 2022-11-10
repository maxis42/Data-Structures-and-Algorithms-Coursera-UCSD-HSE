# python 3
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


class EdgeNC:
    def __init__(self, start, end, low_bound, capacity):
        self.start = start
        self.end = end
        self.low_bound = low_bound
        self.capacity = capacity

        self.flow = 0

    def __str__(self):
        s = "Edge(start={}, end={}, low_bound={}, capacity={})"\
            .format(self.start, self.end, self.low_bound, self.capacity)
        return s

    def __repr__(self):
        s = "Edge(start={}, end={}, low_bound={}, capacity={})" \
            .format(self.start, self.end, self.low_bound, self.capacity)
        return s


class NetworkCirculation:
    def __init__(self, n_vertices, edges):
        self.n = n_vertices
        self.edges = edges
        self.m = len(self.edges)

    def solve(self):
        if self.check_naive_solution():
            circulation = [edge.low_bound for edge in self.edges]
            return circulation

        adj_list_prev = [[] for _ in range(self.n)]
        adj_list_next = [[] for _ in range(self.n)]
        for i, edge in enumerate(self.edges):
            adj_list_prev[edge.end].append(i)
            adj_list_next[edge.start].append(i)

        fg = FlowGraph(self.n + 2)
        for edge in self.edges:
            # print(f"Add edge {edge.start}->{edge.end} capacity={edge.capacity - edge.low_bound}")
            fg.add_edge(edge.start, edge.end, edge.capacity - edge.low_bound)

        # add super-source and super-sink
        for v in range(self.n):
            source_capacity = sum([self.edges[i].low_bound for i in adj_list_prev[v]])
            if source_capacity != 0:
                fg.add_edge(self.n, v, source_capacity)
                # print(f"Add edge source->{v} capacity={source_capacity}")

            sink_capacity = sum([self.edges[i].low_bound for i in adj_list_next[v]])
            if sink_capacity != 0:
                fg.add_edge(v, self.n + 1, sink_capacity)
                # print(f"Add edge {v}->sink capacity={sink_capacity}")

        fg.max_flow(start=self.n, end=self.n + 1)

        # check super-source and super-sink edges are saturated
        for edge_id in fg.graph[self.n]:
            edge = fg.edges[edge_id]
            if edge.flow != edge.capacity:
                return None
        for edge_id in fg.graph[self.n + 1]:
            edge = fg.edges[edge_id]
            if edge.flow != edge.capacity:
                return None

        # construct solution
        circulation = []
        for i, edge in enumerate(self.edges):
            print(f"Res flow through {i}: {fg.edges[i * 2].flow}")
            circulation.append(edge.low_bound + fg.edges[i * 2].flow)
        return circulation

    def check_naive_solution(self):
        old_flow = []
        for edge in self.edges:
            old_flow.append(edge.flow)
            edge.flow = edge.low_bound

        ans = self.check_solution(self.n, self.edges)

        for i, edge in enumerate(self.edges):
            edge.flow = old_flow[i]
        return ans

    @staticmethod
    def check_solution(n, edges):
        for edge in edges:
            if edge.low_bound <= edge.flow <= edge.capacity:
                continue
            else:
                return False

        adj_list_prev = [[] for _ in range(n)]
        adj_list_next = [[] for _ in range(n)]
        for i, edge in enumerate(edges):
            adj_list_prev[edge.end].append(i)
            adj_list_next[edge.start].append(i)

        for v in range(n):
            inflow = sum([edges[i].flow for i in adj_list_prev[v]])
            outflow = sum([edges[i].flow for i in adj_list_next[v]])
            if inflow != outflow:
                return False
        return True


def run_test():
    n_vertices = 3
    edges_raw = [
        (1, 2, 0, 3),
        (2, 3, 0, 3),
    ]
    edges_raw = [
        (1, 2, 1, 3),
        (2, 3, 2, 4),
        (3, 1, 1, 2),
    ]
    # edges_raw = [
    #     (1, 2, 1, 3),
    #     (2, 3, 2, 4),
    #     (1, 3, 1, 2),
    # ]
    edges = []
    for v1, v2, low, cap in edges_raw:
        edges.append(EdgeNC(v1 - 1, v2 - 1, low, cap))
    edges = tuple(edges)

    circulation = NetworkCirculation(n_vertices, edges).solve()

    if circulation is not None:
        print("YES")
        for flow in circulation:
            print(flow)
    else:
        print("NO")


def run_algo():
    n_vertices, n_edges = map(int, input().split())
    edges = []
    for _ in range(n_edges):
        v1, v2, low, cap = map(int, input().split())
        edges.append(EdgeNC(v1 - 1, v2 - 1, low, cap))
    edges = tuple(edges)

    circulation = NetworkCirculation(n_vertices, edges).solve()

    if circulation is not None:
        print("YES")
        for flow in circulation:
            print(flow)
    else:
        print("NO")


if __name__ == "__main__":
    run_test()
    # run_algo()
