# python 3
from collections import deque, defaultdict
from random import randint, choice


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


class GenomeAssembler:
    def __init__(self, reads):
        self.reads = reads

        self._adj_list_cnt = None
        self._in_stack = None

    def solve(self, k):
        k_mers = self.k_mers(self.reads, k)
        k_min_1_mers = self.k_min_1_mers(k_mers)

        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)
        edges = self.remove_bubbles(len(k_min_1_mers), edges, k_mers, k_min_1_mers)
        edges = self.remove_tips(len(k_min_1_mers), edges)
        k_min_1_mers, edges = self.shrink_graph(k_min_1_mers, edges)

        ec = EulerianCycle(len(k_min_1_mers), edges)
        path = ec.find_path()

        genome = None
        if path is not None:
            genome = self.construct_genome(k_min_1_mers, path)
        return genome

    @staticmethod
    def construct_genome(k_min_1_mers, path):
        ss = []
        for i in path:
            ss.append(k_min_1_mers[i][-1:])
        s = "".join(ss)
        return s

    @staticmethod
    def k_mers(reads, k):
        k_mers = set()
        for read in reads:
            for i in range(len(read) - k + 1):
                k_mers.add(read[i:(i + k)])
        k_mers = tuple(k_mers)
        return k_mers

    @staticmethod
    def k_min_1_mers(k_mers):
        k_min_1_mers = set()
        for k_mer in k_mers:
            k_min_1_mers.add(k_mer[:-1])
            k_min_1_mers.add(k_mer[1:])
        k_min_1_mers = tuple(k_min_1_mers)
        return k_min_1_mers

    @staticmethod
    def k_mers_coverage(reads, k_mers):
        k = len(k_mers[0])
        coverage_raw = defaultdict(int)
        for read in reads:
            for i in range(len(read) - k + 1):
                coverage_raw[read[i:(i + k)]] += 1
        coverage = [0] * len(k_mers)
        for i, k_mer in enumerate(k_mers):
            coverage[i] = coverage_raw[k_mer]
        return coverage

    def remove_bubbles(self, n, edges, k_mers, k_min_1_mers):
        k_mers_coverage = self.k_mers_coverage(self.reads, k_mers)
        adj_list = self.edges_to_adj_list(n, edges)

        for v_start in range(n):
            paths_raw = self.dfs_threshold_paths(v_start, adj_list, len(k_mers[0]))

            paths = defaultdict(list)
            for path in paths_raw:
                v_end = path[-1]
                paths[v_end].append(path)

            for v_end, paths_cur in paths.items():
                if len(paths_cur) <= 1:
                    continue

                bubble_pairs = []
                for i in range(len(paths_cur) - 1):
                    path_i_inner = set(paths_cur[i][1:-1])
                    for j in range(i + 1, len(paths_cur)):
                        path_j_inner = set(paths_cur[j][1:-1])
                        if len(path_i_inner.intersection(path_j_inner)) == 0:
                            bubble_pairs.append((i, j))

                    path_removed = [False] * len(paths_cur)
                    for p1, p2 in bubble_pairs:
                        if not path_removed[p1] and not path_removed[p2]:
                            path_1 = paths_cur[p1]
                            coverage_p1 = self.path_coverage(path_1, k_mers, k_min_1_mers, k_mers_coverage)
                            path_2 = paths_cur[p2]
                            coverage_p2 = self.path_coverage(path_2, k_mers, k_min_1_mers, k_mers_coverage)

                            if coverage_p1 < coverage_p2:
                                edges_to_del = {(path_1[i], path_1[i + 1]) for i in range(len(path_1) - 1)}
                                edges = [edge for edge in edges if edge not in edges_to_del]
                                path_removed[p1] = True
                            else:
                                edges_to_del = {(path_2[i], path_2[i + 1]) for i in range(len(path_2) - 1)}
                                edges = [edge for edge in edges if edge not in edges_to_del]
                                path_removed[p2] = True

                            adj_list = self.edges_to_adj_list(n, edges)
        return edges

    @staticmethod
    def path_coverage(path, k_mers, k_min_1_mers, k_mers_coverage):
        coverage = 0
        for i in range(len(path) - 1):
            k_mer = k_min_1_mers[path[i]] + k_min_1_mers[path[i + 1]][-1]
            coverage += k_mers_coverage[k_mers.index(k_mer)]
        coverage = coverage / (len(path) - 1)
        return coverage

    @staticmethod
    def shrink_graph(k_min_1_mers, edges):
        k_min_1_mers_new_set = set()
        for v1, v2 in edges:
            k_min_1_mers_new_set.add(k_min_1_mers[v1])
            k_min_1_mers_new_set.add(k_min_1_mers[v2])

        k_min_1_mers_new = []
        k_min_1_mers_old_to_new = [0] * len(k_min_1_mers)
        j = 0
        for i, k_min_1_mer in enumerate(k_min_1_mers):
            if k_min_1_mer in k_min_1_mers_new_set:
                k_min_1_mers_new.append(k_min_1_mer)
                k_min_1_mers_old_to_new[i] = j
                j += 1
        k_min_1_mers = tuple(k_min_1_mers_new)

        edges_new = []
        for v1, v2 in edges:
            edges_new.append((k_min_1_mers_old_to_new[v1], k_min_1_mers_old_to_new[v2]))
        edges = tuple(edges_new)
        return k_min_1_mers, edges

    def remove_tips(self, n, edges):
        while True:
            adj_list, adj_list_r = self.edges_to_adj_lists(n, edges)

            edges_to_del = set()
            for i, edge in enumerate(edges):
                v1, v2 = edge
                if (len(adj_list[v2]) == 0) or (len(adj_list_r[v1]) == 0):
                    edges_to_del.add(i)

            if len(edges_to_del) == 0:
                # all edges are good
                break

            edges = [edge for i, edge in enumerate(edges)
                     if i not in edges_to_del]
        return edges

    @staticmethod
    def edges_to_adj_list(n, edges):
        adj_list = [[] for _ in range(n)]
        for v1, v2 in edges:
            adj_list[v1].append(v2)
        return adj_list

    @staticmethod
    def edges_to_adj_lists(n, edges):
        adj_list = [[] for _ in range(n)]
        adj_list_r = [[] for _ in range(n)]
        for v1, v2 in edges:
            adj_list[v1].append(v2)
            adj_list_r[v2].append(v1)
        return adj_list, adj_list_r

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

    def dfs_threshold_paths(self, v_start, adj_list, threshold):
        if self._adj_list_cnt is None:
            self._adj_list_cnt = [0] * len(adj_list)
        if self._in_stack is None:
            self._in_stack = [False] * len(adj_list)

        paths = set()
        stack = [v_start]
        self._in_stack[v_start] = True

        while stack:
            if len(stack) > 1:
                paths.add(tuple(stack))

            v_last = stack[-1]
            adj_list_i = self._adj_list_cnt[v_last]
            while adj_list_i < len(adj_list[v_last]):
                v_next = adj_list[v_last][adj_list_i]
                adj_list_i += 1
                if not self._in_stack[v_next]:
                    self._adj_list_cnt[v_last] = adj_list_i
                    stack.append(v_next)
                    self._in_stack[v_next] = True
                    break
            else:
                stack.pop()
                self._in_stack[v_last] = False
                self._adj_list_cnt[v_last] = 0

            if len(stack) == (threshold + 1):
                paths.add(tuple(stack))
                v_last = stack.pop()
                self._in_stack[v_last] = False
                self._adj_list_cnt[v_last] = 0
        return paths


def run_test():
    reads = (
        "AAGGCGGTAATATGGCAG",
        "AATATGGCAGCGCGGTCG",
        "ATCATCTGGCCATGACTT",
        "ATCTGGCCATCACTTAAG",
        "CACTTAAGACGGTAATAT",
        "CATCACTTAAGACGGTAA",
        "CGAGCTTAATCATCTGGC",
        "CGGTAATATGGCAGCGCG",
        "CTTAAGACGGTAATATGG",
        "CTTAATCATCTGGCCATC",
        "GAGCTTAATCATCTGGCC",
        "GCAGCGCGGTCGAGCTTA",
        "GCCATCACTTAAGACGGT",
        "GCGCGGTCGAGCTGAATC",
        "GCGGTCGAGCTTAATCAT",
        "GCTTAATCATCTGGCCAT",
        "GGTCGAGCTTAATCATCT",
        "GTAATATGGCAGCGCGGT",
        "GTCGAGCTTAATCTTCTG",
        "TAATATGGCAGCGCGGTC",
        "TAATCATCTGGCCATCAC",
        "TATGGCAGCGCGGTCGAG",
        "TCATCTGGCCATCGCTTA",
        "TGGCAGCGCGGTCGAGCT",
        "TGGCCATCACTTAAGACG",
        # CATCACTTAAGACGGTAATATGGCAGCGCGGTCGAGCTTAATCATCTGGC
    )
    k = 10

    # bubble test
    reads = ("AACG", "AAGG", "ACGT", "AGGT", "CGTT",
             "GCAA", "GGTT", "GTTG", "TGCA", "TTGC")
    k = 3

    # # tip test
    # reads = ("AACG", "AAGG", "ACGT", "CAAC", "CGTT",
    #          "GCAA", "GTTG", "TCCA", "TGCA", "TTGC")
    # k = 3

    genome = GenomeAssembler(reads).solve(k)
    print(genome)


def run_algo():
    reads = []
    for _ in range(1618):
        reads.append(input().strip())
    reads = tuple(reads)

    k = 20
    genome = GenomeAssembler(reads).solve(k)
    print(genome)


def generate_reads_with_errors():
    with open("phix174_genome.txt", "r") as f:
        genome = f.read().strip()

    genome = deque(genome)
    alphabet = ("a", "c", "g", "t")
    with open("phix174_genome_reads_with_errors.txt", "w") as f:
        for _ in range(2000):
            genome.rotate(randint(0, len(genome) - 1))
            read = "".join(list(genome)[:100])
            error_pos = randint(0, len(read) - 1)
            new_letter = choice([c for c in alphabet if c != read[error_pos]])
            read = read[:error_pos] + new_letter + read[(error_pos + 1):] + "\n"
            f.write(read)


def run_error_prone_test():
    n_reads = 1000
    reads = []
    with open("phix174_genome_reads_with_errors.txt", "r") as f:
        for _ in range(n_reads):
            reads.append(f.readline().strip())
    reads = tuple(reads)

    k = 15
    genome = GenomeAssembler(reads).solve(k)
    print(genome)
    if genome is not None:
        print(len(genome))


if __name__ == "__main__":
    # generate_reads_with_errors()
    # run_error_prone_test()
    # run_test()
    run_algo()
