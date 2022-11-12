# python 3


class TipRemoval:
    def __init__(self, reads, k):
        self.reads = reads
        self.k = k

    def remove_tips(self):
        k_mers = self.k_mers()
        k_min_1_mers = self.k_min_1_mers(k_mers)

        n = len(k_min_1_mers)
        edges = self.de_bruijn_graph(k_mers, k_min_1_mers)
        adj_list, adj_list_r = self.edges_to_adj_lists(n, edges)

        n_tips = 0
        while True:
            edges_to_del = set()
            for i, edge in enumerate(edges):
                v1, v2 = edge
                if (len(adj_list[v2]) == 0) or (len(adj_list_r[v1]) == 0):
                    edges_to_del.add(i)

            if len(edges_to_del) == 0:
                # all edges are good
                break
            else:
                n_tips += len(edges_to_del)
                edges = [edge for i, edge in enumerate(edges) if i not in edges_to_del]
                adj_list, adj_list_r = self.edges_to_adj_lists(n, edges)
        return n_tips

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


def run_test():
    reads = ("AACG", "AAGG", "ACGT", "CAAC", "CGTT",
             "GCAA", "GTTG", "TCCA", "TGCA", "TTGC")
    k = 3
    tr = TipRemoval(reads, k)
    n_tips = tr.remove_tips()
    print(n_tips)


def run_algo():
    reads = []
    for _ in range(1618):
        reads.append(input().strip())
    reads = tuple(reads)
    k = 15
    tr = TipRemoval(reads, k)
    n_tips = tr.remove_tips()
    print(n_tips)


if __name__ == "__main__":
    # run_test()
    run_algo()
