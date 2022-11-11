# python 3
from time import sleep


class BubbleDetection:
    def __init__(self, k, threshold, reads):
        self.k = k
        self.threshold = threshold
        self.reads = reads

    def num_bubbles(self):
        k_mers = self.k_mers()
        k_min_1_mers = self.k_min_1_mers(k_mers)

        n = len(k_min_1_mers)
        print("Vertices:")
        for i in range(n):
            print(k_min_1_mers[i], i, " ", end="")
        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)

        n = 8
        edges = (
            (0, 1), (0, 7), (0, 5),
            (1, 2), (1, 7),
            (2, 3), (2, 7),
            (3, 4), (3, 7),
            (5, 7), (5, 6),
            (6, 4), (6, 7),
            (7, 4),
        )
        self.threshold = 4

        # print("Edges:")
        # for v1, v2 in edges:
        #     print(f"{v1}->{v2} {k_min_1_mers[v1]}->{k_min_1_mers[v2]}")
        adj_list = self.edges_to_adj_list(n, edges)
        print(f"\nadj_list: {adj_list}")

        n_bubbles = 0
        for v in range(n):
            paths = self.dfs_threshold_paths(v, adj_list, self.threshold)
            n_bubbles += 0
        return n_bubbles

    @staticmethod
    def dfs_threshold_paths(v, adj_list, threshold):
        paths = []
        visited = [False] * len(adj_list)
        stack = [v]
        while stack:
            if len(stack) == (threshold + 1):
                paths.append(tuple(stack))
                print(tuple(stack))

                visited[stack[-1]] = True
                stack.pop()
                print(visited)

            for v_next in adj_list[stack[-1]]:
                if not visited[v_next]:
                    stack.append(v_next)
                    break
            else:
                visited[stack[-1]] = True
                for v_next in adj_list[stack[-1]]:
                    visited[v_next] = False
                stack.pop()
        print(f"Vector {v} paths: {paths}")
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
    run_test()
    # run_algo()
