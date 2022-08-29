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
        parent[start] = -1

        q = deque([start])
        while q:
            cur = q.popleft()

            if cur == end:
                break

            for edge_id in self.graph[cur]:
                edge = self.edges[edge_id]
                if (parent[edge.end] is None) and (edge.flow > 0):
                    q.append(edge.end)
                    parent[edge.end] = (edge_id, edge)

        path = []
        if parent[end] is not None:
            next_node = end
            while next_node != start:
                edge_id, edge = parent[next_node]
                path.append(edge_id)
                next_node = edge.start
        return path

    def maximize_flow(self, start, end):
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
            min_flow = graph_r.edges[path[0]].flow
            for edge_id in path[1:]:
                min_flow = min(min_flow, graph_r.edges[edge_id].flow)

            # update graphs
            for edge_id in path:
                if edge_id % 2 == 0:
                    self.edges[edge_id].flow += min_flow

                    graph_r.edges[edge_id].flow -= min_flow
                    graph_r.edges[edge_id + 1].flow += min_flow
                else:
                    self.edges[edge_id - 1].flow -= min_flow

                    graph_r.edges[edge_id - 1].flow += min_flow
                    graph_r.edges[edge_id].flow -= min_flow

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

        self._source_id = 0
        self._stock_id = self.n + self.m + 1

        self.graph = FlowGraph(self.n + self.m + 2)
        # add edges between source '0' and left nodes with unit capacity
        for i in range(self.n):
            self.graph.add_edge(start=self._source_id,
                                end=i + 1,
                                capacity=1)
        # add edges between right nodes and stock 'n + m + 1' with unit capacity
        for i in range(self.m):
            self.graph.add_edge(start=self.n + 1 + i,
                                end=self._stock_id,
                                capacity=1)

    def maximize_matching(self):
        self.graph.maximize_flow(self._source_id, self._stock_id)

        matches = []
        for i in range(len(self.graph.edges) // 2):
            edge = self.graph.edges[i * 2]
            if (
                    (edge.start != self._source_id)
                    and (edge.end != self._stock_id)
                    and (edge.flow == 1)
            ):
                node_first = edge.start - 1
                node_second = edge.end - 1
                matches.append((node_first, node_second))
        return matches


class StockCharts:
    def __init__(self, prices):
        self.prices = prices

        self.num_stocks = len(self.prices)
        self.num_points = len(self.prices[0])

    def solve(self):
        bgm = BipartiteGraphMatching(self.num_stocks, self.num_stocks)

        for i in range(self.num_stocks):
            stock_1 = self.prices[i]
            for j in range(i + 1, self.num_stocks):
                stock_2 = self.prices[j]

                edge = True  # stock 1 everywhere less than stock 2
                edge_rev = True  # stock 2 everywhere less than stock 1
                for k in range(self.num_points):
                    if edge and (stock_1[k] >= stock_2[k]):
                        edge = False
                    if edge_rev and (stock_2[k] >= stock_1[k]):
                        edge_rev = False

                    if not edge and not edge_rev:
                        break

                if edge:
                    bgm.graph.add_edge(i + 1, self.num_stocks + 1 + j, 1)
                if edge_rev:
                    bgm.graph.add_edge(j + 1, self.num_stocks + 1 + i, 1)

        matches = bgm.maximize_matching()
        num_charts = self.num_stocks - len(matches)
        return num_charts


def run_test():
    prices = (
        (1, 2, 3, 4),
        (2, 3, 4, 6),
        (6, 5, 4, 3),
    )

    prices = (
        (0, 0, 0, 0),
        (1013, 13, 1013, 1013),
        (10, 1010, 10, 1010),
        (1009, 9, 9, 1009),
        (4, 4, 1004, 4),
        (2, 1002, 2, 2),
        (1007, 1007, 1007, 7),
        (1001, 1, 1, 1),
        (1003, 1003, 3, 3),
        (12, 12, 1012, 1012),
        (1005, 5, 1005, 5),
        (6, 1006, 1006, 6),
        (1015, 1015, 1015, 1015),
        (1011, 1011, 11, 1011),
        (14, 1014, 1014, 1014),
        (8, 8, 8, 1008),
    )

    stock_charts = StockCharts(prices)
    num_charts = stock_charts.solve()
    print(num_charts)


def run_algo():
    num_stocks, num_points = map(int, input().split())

    prices = []
    for _ in range(num_stocks):
        prices.append(list(map(int, input().split())))

    stock_charts = StockCharts(prices)
    num_charts = stock_charts.solve()
    print(num_charts)


if __name__ == "__main__":
    # run_test()
    run_algo()
