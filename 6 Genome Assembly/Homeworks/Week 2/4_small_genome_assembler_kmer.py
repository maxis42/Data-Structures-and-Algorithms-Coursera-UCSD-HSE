# python 3
from collections import deque


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
            cycle = [v_start]
            while v_next != v_start:
                cycle.append(v_next)
                edge_id = adj_list[v_next].pop()
                explored_edge[edge_id] = True
                m_explored += 1
                v_next = self.edges[edge_id][1]
            cycles.append(cycle)

        # construct the only cycle from found cycles
        cycles_sets = []
        for i, cycle in enumerate(cycles):
            cycles_sets.append(set(cycle))
            cycles[i] = deque(cycle)

        visited_cycles = [False] * len(cycles)

        path = []
        path_stack = deque(list(cycles[0]))
        visited_cycles[0] = True

        while path_stack:
            cur_v = path_stack.popleft()
            for i, cycle_set in enumerate(cycles_sets):
                if visited_cycles[i]:
                    continue

                if cur_v in cycle_set:
                    while cycles[i][-1] != cur_v:
                        cycles[i].rotate(1)

                    for v in reversed(cycles[i]):
                        path_stack.appendleft(v)

                    visited_cycles[i] = True
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


class UniversalString:
    """
    Find a universal circular string.
    """
    def __init__(self, patterns):
        self.patterns = patterns
        self.k = len(self.patterns[0])

    def solve(self):
        k_mers = self.patterns

        k_min_1_mers = set()
        for k_mer in k_mers:
            k_min_1_mers.add(k_mer[:-1])
            k_min_1_mers.add(k_mer[1:])
        k_min_1_mers = tuple(k_min_1_mers)

        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)

        ec = EulerianCycle(len(k_min_1_mers), edges)
        path = ec.find_path()

        ss = []
        for i in path:
            ss.append(k_min_1_mers[i][-1:])
        s = "".join(ss)
        return s

    @staticmethod
    def de_bruijn_graph(k_mers, k_min_1_mers):
        k_min_1_mer_to_id = dict()
        for i, k_mer in enumerate(k_min_1_mers):
            k_min_1_mer_to_id[k_mer] = i

        edges = []
        for k_mer in k_mers:
            v1 = k_min_1_mer_to_id[k_mer[:-1]]
            v2 = k_min_1_mer_to_id[k_mer[1:]]
            edges.append((v1, v2))
        edges = tuple(edges)
        return edges


class GenomeAssemblerKmer:
    def __init__(self, k_mers):
        self.k_mers = k_mers

    def solve(self):
        s = UniversalString(self.k_mers).solve()
        return s


def run_test():
    k_mers = []
    n_kmers = 5386
    with open("phix174_10mers.txt", "r") as f:
        for _ in range(n_kmers):
            k_mers.append(f.readline().strip())
    k_mers = tuple(k_mers)
    res = GenomeAssemblerKmer(k_mers).solve()
    print(res)


def run_algo():
    n_kmers = 5396
    k_mers = []
    for _ in range(n_kmers):
        k_mer = input().strip()
        k_mers.append(k_mer)
    k_mers = tuple(k_mers)

    res = GenomeAssemblerKmer(k_mers).solve()
    print(res)


if __name__ == "__main__":
    # run_test()
    run_algo()
