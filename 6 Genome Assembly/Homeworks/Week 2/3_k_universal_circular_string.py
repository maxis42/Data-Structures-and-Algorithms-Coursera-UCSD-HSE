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


class KUniCircStr:
    """
    Find a k-universal circular binary string.
    """
    def __init__(self, k):
        self.k = k

    def solve(self):
        k_mers = []
        for i in range(2 ** self.k):
            s = format(i, "0{}b".format(self.k))
            k_mers.append(s)

        k_min_1_mers = []
        for i in range(2 ** (self.k - 1)):
            s = format(i, "0{}b".format(self.k - 1))
            k_min_1_mers.append(s)

        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)

        ec = EulerianCycle(len(k_min_1_mers), edges)
        path = ec.find_path()

        ss = [k_min_1_mers[path[0]][-1:]]
        for i in path[1:-1]:
            ss.append(k_min_1_mers[i][-1:])
        s = "".join(ss)
        return s

    def de_bruijn_graph(self, k_mers, k_min_1_mers):
        k_min_1_mer_to_id = dict()
        for i, k_mer in enumerate(k_min_1_mers):
            k_min_1_mer_to_id[k_mer] = i

        edges = set()
        for k_mer in k_mers:
            v1 = k_min_1_mer_to_id[k_mer[:-1]]
            v2 = k_min_1_mer_to_id[k_mer[1:]]
            edges.add((v1, v2))
        edges = tuple(edges)
        return edges


def run_test():
    # k = 3
    # ans = "0001110100"
    k = 4
    ans = "0000110010111101"
    res = KUniCircStr(k).solve()
    print(res)
    # assert len(res) == len(ans), f"len = {len(res)}, true len = {len(ans)}"
    # assert res == ans


def run_algo():
    k = int(input())
    res = KUniCircStr(k).solve()
    print(res)


if __name__ == "__main__":
    # run_test()
    run_algo()
