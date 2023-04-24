# python3
from collections import namedtuple

Test = namedtuple("Test", ["n", "query", "output"])


class Query:
    def __init__(self, query):
        self.type = query[0]
        self.number = int(query[1])
        if self.type == "add":
            self.name = query[2]


class PhoneBook:
    def __init__(self):
        self.phone_book = {}

    def add_number(self, number, name):
        self.phone_book[number] = name

    def del_number(self, number):
        if number in self.phone_book:
            del self.phone_book[number]

    def find_number(self, number):
        return self.phone_book.get(number, "not found")


def read_queries():
    n = int(input())
    return [Query(input().split()) for _ in range(n)]


def write_responses(result):
    print("\n".join(result))


def process_queries(queries):
    result = []
    # Keep list of all existing (i.e. not deleted yet) contacts.
    phone_book = PhoneBook()
    for query in queries:
        if query.type == "add":
            phone_book.add_number(query.number, query.name)
        elif query.type == "del":
            phone_book.del_number(query.number)
        else:
            response = phone_book.find_number(query.number)
            result.append(response)
    return result


def run_tests():
    test1 = Test(
        n=12,
        query=(
            "add 911 police",
            "add 76213 Mom",
            "add 17239 Bob",
            "find 76213",
            "find 910",
            "find 911",
            "del 910",
            "del 911",
            "find 911",
            "find 76213",
            "add 76213 daddy",
            "find 76213",
        ),
        output=(
            "Mom",
            "not found",
            "police",
            "not found",
            "Mom",
            "daddy",
        )
    )

    test2 = Test(
        n=8,
        query=(
            "find 3839442",
            "add 123456 me",
            "add 0 granny",
            "find 0",
            "find 123456",
            "del 0",
            "del 0",
            "find 0",
        ),
        output=(
            "not found",
            "granny",
            "me",
            "not found",
        )
    )

    tests = (test1, test2)
    for test in tests:
        queries = [Query(test.query[i].split()) for i in range(test.n)]
        result = process_queries(queries)
        print(result)
        assert result == list(test.output), result


if __name__ == "__main__":
    write_responses(process_queries(read_queries()))
    # run_tests()
