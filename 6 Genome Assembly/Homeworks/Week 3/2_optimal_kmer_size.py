# python 3


class OptimalKMerSize:
    def __init__(self, reads):
        self.reads = reads

    def solve(self):
        k_min = 3
        k_max = len(self.reads[0])

        while k_min <= k_max:
            k = (k_min + k_max) // 2

            k_mers = set()
            for read in self.reads:
                for i in range(len(read) - k + 1):
                    k_mers.add("".join(read)[i:(i + k)])
            k_mers = tuple(k_mers)

            k_min_1_mers = set()
            for k_mer in k_mers:
                k_min_1_mers.add(k_mer[:-1])
                k_min_1_mers.add(k_mer[1:])
            k_min_1_mers = tuple(k_min_1_mers)

            edges = self.de_bruijn_graph(k_mers, k_min_1_mers)

            if not self.cycle_exists(len(k_min_1_mers), edges):
                k_max = k - 1
            else:
                k_min = k + 1
        return k_max

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

    @staticmethod
    def cycle_exists(n, edges):
        in_degree = [0] * n
        out_degree = [0] * n

        for v1, v2 in edges:
            out_degree[v1] += 1
            in_degree[v2] += 1

        cycle = True
        for d1, d2 in zip(in_degree, out_degree):
            if d1 != d2:
                cycle = False
                break
        return cycle


def run_test():
    reads = ("AACG", "ACGT", "CAAC", "GTTG", "TGCA")
    k = OptimalKMerSize(reads).solve()
    print(k)


def run_algo():
    n_reads = 400
    reads = []
    for _ in range(n_reads):
        reads.append(input().strip())
    reads = tuple(reads)

    k = OptimalKMerSize(reads).solve()
    print(k)


if __name__ == "__main__":
    # run_test()
    run_algo()
