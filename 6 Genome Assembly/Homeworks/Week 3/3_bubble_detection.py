# python 3
from collections import defaultdict


class BubbleDetection:
    def __init__(self, k, threshold, reads):
        self.k = k
        self.threshold = threshold
        self.reads = reads

        self._adj_list_cnt = None
        self._in_stack = None

    def num_bubbles(self):
        k_mers = self.k_mers()
        k_min_1_mers = self.k_min_1_mers(k_mers)

        n = len(k_min_1_mers)
        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)
        adj_list = self.edges_to_adj_list(n, edges)

        n_bubbles = 0
        for v_start in range(n):
            paths_raw = self.dfs_threshold_paths(v_start, adj_list, self.threshold)

            paths = defaultdict(list)
            for path in paths_raw:
                paths[path[-1]].append(path)

            for v_end, paths_cur in paths.items():
                if len(paths_cur) <= 1:
                    continue

                for i in range(len(paths_cur) - 1):
                    path_i_inner = set(paths_cur[i][1:-1])
                    for j in range(i, len(paths_cur)):
                        path_j_inner = set(paths_cur[j][1:-1])
                        if len(path_i_inner.intersection(path_j_inner)) == 0:
                            n_bubbles += 1
        return n_bubbles

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

    def k_mers(self):
        k_mers = set()
        for read in self.reads:
            for i in range(len(read) - self.k + 1):
                k_mers.add("".join(read)[i:(i + self.k)])
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
    def edges_to_adj_list(n, edges):
        adj_list = [[] for _ in range(n)]
        for v1, v2 in edges:
            adj_list[v1].append(v2)
        return adj_list

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


def run_test():
    k, threshold = 3, 3
    reads = ("AACG", "AAGG", "ACGT", "AGGT", "CGTT",
             "GCAA", "GGTT", "GTTG", "TGCA", "TTGC")
    bd = BubbleDetection(k, threshold, reads)
    print(bd.num_bubbles())


def run_algo():
    k, threshold = map(int, input().split())
    reads = []
    for _ in range(1618):
        reads.append(input().strip())

    bd = BubbleDetection(k, threshold, reads)
    print(bd.num_bubbles())


if __name__ == "__main__":
    # run_test()
    run_algo()
