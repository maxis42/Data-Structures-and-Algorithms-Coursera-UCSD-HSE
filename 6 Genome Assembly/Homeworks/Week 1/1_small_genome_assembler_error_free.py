# python 3


class GenomeAssembler:
    """
    Error free genome assembler for small genome.
    """
    STR_LEN = 100

    def __init__(self, dataset):
        self.dataset = dataset
        self.n = len(self.dataset)

    def solve(self):
        # [(overlap_size, next string ID)]
        next_s = [(0, None) for _ in range(self.n)]

        for i in range(self.n - 1):
            s1 = self.dataset[i]
            for j in range(i + 1, self.n):
                s2 = self.dataset[j]

                prev_overlap_size_i, _ = next_s[i]
                prev_overlap_size_j, _ = next_s[j]

                overlap_size_i = self.find_bigger_overlap_size(s1, s2, prev_overlap_size_i)
                overlap_size_j = self.find_bigger_overlap_size(s2, s1, prev_overlap_size_j)

                if overlap_size_i is not None:
                    next_s[i] = (overlap_size_i, j)
                if overlap_size_j is not None:
                    next_s[j] = (overlap_size_j, i)

        str_parts = [self.dataset[0]]
        overlap_size, cur = next_s[0]
        while cur != 0:
            str_parts.append(self.dataset[cur][overlap_size:])
            overlap_size, cur = next_s[cur]

        s = "".join(str_parts)

        # truncate circularly identical symbols
        s = s[:-overlap_size]
        return s

    @staticmethod
    def find_bigger_overlap_size(s1, s2, prev_overlap_size):
        res = None
        for overlap_size in range(GenomeAssembler.STR_LEN - 1, prev_overlap_size, -1):
            if s2.startswith(s1[(GenomeAssembler.STR_LEN - overlap_size):]):
                res = overlap_size
                break
        return res


def run_test():
    s = "gagttttatcgcttcca"
    dataset = [
        "gagtt",  # 0
        "gtttt",  # 1
        "tttat",  # 2
        "tatcg",  # 3
        "tcgct",  # 4
        "gcttc",  # 5
        "ttcca",  # 6
        "agttt",  # 7
        "cagag",  # 8
    ]
    t = GenomeAssembler(dataset)
    ans = t.solve()
    print(ans)


def run_algo():
    n_rows = 1618
    dataset = [input().strip()]
    for _ in range(n_rows - 1):
        s = input().strip()
        if s != dataset[-1]:
            dataset.append(s)

    t = GenomeAssembler(dataset)
    ans = t.solve()
    print(ans)


if __name__ == "__main__":
    run_algo()
    # run_test()
