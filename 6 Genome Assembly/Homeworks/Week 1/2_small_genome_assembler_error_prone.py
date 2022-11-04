# python 3
from collections import defaultdict


class GenomeAssembler:
    """
    Error prone genome assembler for small genome.
    """
    # all strings of this length
    STR_LEN = 100

    # each string has exactly one mistake
    STR_ERR_NUM = 2

    def __init__(self, dataset):
        self.dataset = self.drop_duplicates(dataset)
        self.n = len(self.dataset)

    def drop_duplicates(self, dataset):
        n = len(dataset)
        duplicate = [False] * n

        for i in range(n - 1):
            if duplicate[i]:
                continue

            s1 = dataset[i]
            for j in range(i + 1, n):
                if duplicate[j]:
                    continue

                s2 = dataset[j]

                if self.has_less_mistakes(s1, s2, max_num_mistakes=GenomeAssembler.STR_ERR_NUM):
                    duplicate[j] = True

        filtered_dataset = []
        for i in range(n):
            if not duplicate[i]:
                filtered_dataset.append(dataset[i])
        return filtered_dataset

    @staticmethod
    def has_less_mistakes(s1, s2, max_num_mistakes=2):
        num_mistakes = 0
        res = True
        for i in range(GenomeAssembler.STR_LEN):
            if s1[i] != s2[i]:
                num_mistakes += 1

            if num_mistakes > max_num_mistakes:
                res = False
                break
        return res

    def solve(self):
        processed = [False] * self.n
        overlap = [0] * self.n
        next_id = [0] * self.n

        i = 0
        for _ in range(self.n - 1):
            s1 = self.dataset[i]
            processed[i] = True
            for j in range(1, self.n):
                if processed[j]:
                    continue

                s2 = self.dataset[j]

                new_overlap = self.find_bigger_overlap_size(s1, s2, overlap[i])

                if new_overlap is not None:
                    next_id[i] = j
                    overlap[i] = new_overlap

            i = next_id[i]

        # genome is circular
        next_id[i] = 0
        overlap[i] = self.find_bigger_overlap_size(self.dataset[i], self.dataset[0])
        last_overlap = overlap[i]

        # [(string ID, start position in final string)]
        start_pos = 0
        str_with_errors = [(0, start_pos)]
        cur = 0
        for _ in range(self.n - 1):
            start_pos += GenomeAssembler.STR_LEN - overlap[cur]
            str_with_errors.append((next_id[cur], start_pos))
            cur = next_id[cur]
        str_len = start_pos + GenomeAssembler.STR_LEN
        for _ in range(self.n - 1, self.n * 2):
            start_pos += GenomeAssembler.STR_LEN - overlap[cur]
            str_with_errors.append((next_id[cur], start_pos))
            cur = next_id[cur]

        # clean strings from errors
        # take the most frequent element for each position
        chars = []
        for i in range(str_len):
            # get all candidate chars for this position with its frequencies
            counter = defaultdict(int)
            for str_id, start_pos in str_with_errors:
                if start_pos <= i < (start_pos + GenomeAssembler.STR_LEN):
                    counter[self.dataset[str_id][i - start_pos]] += 1

            # find the most frequent char
            max_n = 0
            char = ""
            for c, n in counter.items():
                if n > max_n:
                    char = c
                    max_n = n
            chars.append(char)

        s = "".join(chars)

        # truncate circularly identical symbols
        s = s[last_overlap:]
        return s

    @staticmethod
    def find_bigger_overlap_size(s1, s2, prev_overlap_size=0):
        res = None
        for overlap_size in range(GenomeAssembler.STR_LEN - 1, prev_overlap_size, -1):
            num_errors = 0
            s1_start_pos = GenomeAssembler.STR_LEN - overlap_size
            for i in range(overlap_size):
                if s1[s1_start_pos + i] != s2[i]:
                    num_errors += 1
                    if num_errors > GenomeAssembler.STR_ERR_NUM:
                        break
            else:
                res = overlap_size
                break
        return res


def run_test():
    # gagttttatcgcttcca
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
    GenomeAssembler.STR_LEN = 5
    t = GenomeAssembler(dataset)
    ans = t.solve()
    print(ans)


def run_algo():
    n_rows = 1618
    dataset = [input().strip()]
    for _ in range(n_rows - 1):
        dataset.append(input().strip())

    t = GenomeAssembler(dataset)
    ans = t.solve()
    print(ans)


if __name__ == "__main__":
    run_algo()
    # run_test()
