# python3
from collections import namedtuple

TestCase = namedtuple("TestCase", ["n_tables", "n_merges", "n_rows", "merges",
                                   "output"])


class Database:
    def __init__(self, row_counts):
        self.row_counts = row_counts
        self.max_row_count = max(row_counts)
        n_tables = len(row_counts)
        self.ranks = [1] * n_tables
        self.parents = list(range(n_tables))

    def merge(self, src, dst):
        src_parent = self.get_parent(src)
        dst_parent = self.get_parent(dst)

        if src_parent == dst_parent:
            return
        else:
            if self.ranks[src_parent] > self.ranks[dst_parent]:
                self.parents[dst_parent] = src_parent
                self.row_counts[src_parent] += self.row_counts[dst_parent]
                self.max_row_count = max(self.max_row_count, self.row_counts[src_parent])
            elif self.ranks[src_parent] < self.ranks[dst_parent]:
                self.parents[src_parent] = dst_parent
                self.row_counts[dst_parent] += self.row_counts[src_parent]
                self.max_row_count = max(self.max_row_count, self.row_counts[dst_parent])
            else:
                self.parents[src_parent] = dst_parent
                self.ranks[src_parent] += 1
                self.row_counts[dst_parent] += self.row_counts[src_parent]
                self.max_row_count = max(self.max_row_count, self.row_counts[dst_parent])

    def get_parent(self, table):
        tables_to_compress_path = []

        parent = self.parents[table]
        while table != parent:
            tables_to_compress_path.append(table)
            table = parent
            parent = self.parents[table]

        for table in tables_to_compress_path:
            self.parents[table] = parent

        if tables_to_compress_path:
            self.ranks[parent] = 2
        else:
            self.ranks[parent] = 1
        return parent


def run_tests():
    tests = []

    t1 = TestCase(
        n_tables=5,
        n_merges=5,
        n_rows=[1, 1, 1, 1, 1],
        merges=(
            (3, 5),
            (2, 4),
            (1, 4),
            (5, 4),
            (5, 3),
        ),
        output=(2, 2, 3, 5, 5)
    )
    tests.append(t1)

    t2 = TestCase(
        n_tables=6,
        n_merges=4,
        n_rows=[10, 0, 5, 0, 3, 3],
        merges=(
            (6, 6),
            (6, 5),
            (5, 4),
            (4, 3),
        ),
        output=(10, 10, 10, 11)
    )
    tests.append(t2)

    for test in tests:
        max_size = []
        db = Database(test.n_rows)
        for i in range(test.n_merges):
            dst, src = test.merges[i]
            db.merge(dst - 1, src - 1)
            max_size.append(db.max_row_count)

            print(f"dst: {dst-1}, src: {src-1}")
            print(f"Parents: {db.parents}")
            print(f"Ranks: {db.ranks}")
            print(f"Row cnt: {db.row_counts}")
            print()

        assert test.output == tuple(max_size), f"\nExpected: {test.output}\nResult: {tuple(max_size)}"


def main():
    n_tables, n_queries = map(int, input().split())
    counts = list(map(int, input().split()))
    assert len(counts) == n_tables
    db = Database(counts)
    for i in range(n_queries):
        dst, src = map(int, input().split())
        db.merge(dst - 1, src - 1)
        print(db.max_row_count)


if __name__ == "__main__":
    main()
    # run_tests()
