# python 3
from collections import deque, defaultdict


class EulerianCycle:
    def __init__(self, n, edges):
        # num vertices
        self.n = n
        self.edges = edges
        # num edges
        self.m = len(self.edges)

    def find_path(self):
        path = None

        if not self.cycle_exists():
            return path

        # construct adjacency list of adjacent edges
        adj_list = [[] for _ in range(self.n)]
        for i, edge in enumerate(self.edges):
            v_start = edge[0]
            adj_list[v_start].append(i)

        # find all cycles
        m_explored = 0  # num explored edges
        explored_edge = [False] * self.m
        prev_not_explored_v = 0
        cycles = []

        while m_explored < self.m:
            for i in range(prev_not_explored_v, self.n):
                if adj_list[i]:
                    edge_id = adj_list[i].pop()
                    explored_edge[edge_id] = True
                    m_explored += 1
                    prev_not_explored_v = i
                    break

            v_start, v_next = self.edges[edge_id]
            cycle = [v_start, v_next]
            while v_next != v_start:
                edge_id = adj_list[v_next].pop()
                explored_edge[edge_id] = True
                m_explored += 1
                v_next = self.edges[edge_id][1]
                cycle.append(v_next)
            cycles.append(cycle)

        # construct the only cycle from found cycles
        cycle_starts = defaultdict(list)
        for i, cycle in enumerate(cycles):
            cycle_starts[cycle[0]].append(i)

        path = []
        path_stack = deque([cycles[0][0]])

        while path_stack:
            cur_v = path_stack.popleft()
            if (cur_v in cycle_starts) and cycle_starts[cur_v]:
                cycle_id = cycle_starts[cur_v].pop()
                for v in cycles[cycle_id][1:][::-1]:
                    path_stack.appendleft(v)
            path.append(cur_v)
        return path

    def cycle_exists(self):
        in_degree = [0] * self.n
        out_degree = [0] * self.n

        for v1, v2 in self.edges:
            out_degree[v1] += 1
            in_degree[v2] += 1

        cycle = True
        for d1, d2 in zip(in_degree, out_degree):
            if d1 != d2:
                cycle = False
                break
        return cycle


def run_test():
    num_vertices = 4
    edges_ = (
        (1, 2),
        (2, 1),
        (1, 4),
        (4, 1),
        (2, 4),
        (3, 2),
        (4, 3),
    )

    edges = []
    for edge in edges_:
        v1, v2 = edge
        v1, v2 = v1 - 1, v2 - 1
        edges.append((v1, v2))

    ec = EulerianCycle(num_vertices, edges)
    path = ec.find_path()

    if path is None:
        print(0)
    else:
        print(1)
        print(" ".join(map(lambda x: str(x + 1), path[:-1])))


def run_algo():
    num_vertices, num_edges = map(int, input().split())

    edges = []
    for _ in range(num_edges):
        v1, v2 = map(int, input().split())
        v1, v2 = v1 - 1, v2 - 1
        edges.append((v1, v2))

    ec = EulerianCycle(num_vertices, edges)
    path = ec.find_path()

    if path is None:
        print(0)
    else:
        print(1)
        print(" ".join(map(lambda x: str(x + 1), path[:-1])))


if __name__ == "__main__":
    # run_test()
    run_algo()
