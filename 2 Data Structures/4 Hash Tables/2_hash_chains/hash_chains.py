# python3
from collections import namedtuple

Test = namedtuple("Test", ["m", "n", "queries", "output"])


class Query:
    def __init__(self, query):
        self.type = query[0]
        if self.type == "check":
            self.ind = int(query[1])
        else:
            self.s = query[1]


class QueryProcessor:
    _multiplier = 263
    _prime = 1000000007

    def __init__(self, bucket_count):
        self.bucket_count = bucket_count
        # store all strings in one list
        self.elems = [[] for _ in range(self.bucket_count)]

    def _hash_func(self, s):
        ans = 0
        for c in reversed(s):
            ans = (ans * self._multiplier + ord(c)) % self._prime
        return ans % self.bucket_count

    def add_string(self, string, ind):
        if string not in self.elems[ind]:
            self.elems[ind].append(string)

    def del_string(self, string, ind):
        if string in self.elems[ind]:
            self.elems[ind].remove(string)

    def find_string(self, string, ind):
        if self.elems[ind] and (string in self.elems[ind]):
            print("yes")
        else:
            print("no")

    @staticmethod
    def write_chain(chain):
        print(" ".join(chain))

    @staticmethod
    def read_query():
        return Query(input().split())

    def process_query(self, query):
        if query.type == "check":
            # use reverse order, because we append strings to the end
            self.write_chain(cur for cur in reversed(self.elems[query.ind]))
        else:
            ind = self._hash_func(query.s)

            if query.type == "find":
                self.find_string(query.s, ind)
            elif query.type == "add":
                self.add_string(query.s, ind)
            else:
                # "del"
                self.del_string(query.s, ind)

    def process_queries(self):
        n = int(input())
        for i in range(n):
            self.process_query(self.read_query())


def run_tests():
    test1 = Test(
        m=5,
        n=12,
        queries=(
            "add world",
            "add HellO",
            "check 4",
            "find World",
            "find world",
            "del world",
            "check 4",
            "del HellO",
            "add luck",
            "add GooD",
            "check 2",
            "del good",
        ),
        output=(
            "HellO world",
            "no",
            "yes",
            "HellO",
            "GooD luck",
        ),
    )

    test2 = Test(
        m=4,
        n=8,
        queries=(
            "add test",
            "add test",
            "find test",
            "del test",
            "find test",
            "find Test",
            "add Test",
            "find Test",
        ),
        output=(
            "yes",
            "no",
            "no",
            "yes",
        ),
    )

    test3 = Test(
        m=3,
        n=12,
        queries=(
            "check 0",
            "find help",
            "add help",
            "add del",
            "add add",
            "find add",
            "find del",
            "del del",
            "find del",
            "check 0",
            "check 1",
            "check 2",
        ),
        output=(
            "",
            "no",
            "",
            "yes",
            "yes",
            "no",
            "",
            "",
            "add help",
            "",
        ),
    )

    tests = (test1, test2, test3)

    for test in tests:
        bucket_count = test.m
        proc = QueryProcessor(bucket_count)
        n = test.n
        for i in range(n):
            proc.process_query(Query(test.queries[i].split()))
        print("Test ended!\n")


if __name__ == "__main__":
    # run_tests()
    bucket_count = int(input())
    proc = QueryProcessor(bucket_count)
    proc.process_queries()
