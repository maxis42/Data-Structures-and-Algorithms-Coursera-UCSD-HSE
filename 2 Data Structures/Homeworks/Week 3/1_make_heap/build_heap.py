# python3
from collections import namedtuple


def build_heap_naive(data):
    """Build a heap from ``data`` inplace.

    Returns a sequence of swaps performed by the algorithm.
    """
    # The following naive implementation just sorts the given sequence
    # using selection sort algorithm and saves the resulting sequence
    # of swaps. This turns the given array into a heap, but in the worst
    # case gives a quadratic number of swaps.
    #
    # TODO: replace by a more efficient implementation
    swaps = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            if data[i] > data[j]:
                swaps.append((i, j))
                data[i], data[j] = data[j], data[i]
    # return swaps
    return data


def build_heap(data):
    size = len(data)
    swaps = []

    for i in range(len(data)//2, -1, -1):
        data, swaps_ = sift_down(data, i, size)
        swaps.extend(swaps_)

    return data, swaps


def sift_down(data, i, size):
    swaps = []

    while True:
        min_i = i

        left_i = i*2 + 1
        if left_i < size and data[left_i] < data[min_i]:
            min_i = left_i

        right_i = i*2 + 2
        if right_i < size and data[right_i] < data[min_i]:
            min_i = right_i

        if min_i != i:
            data[i], data[min_i] = data[min_i], data[i]
            swaps.append((i, min_i))
            i = min_i
        else:
            break

    return data, swaps


def run_tests():
    test = namedtuple("Test", ("input", "output"))

    tests = [
        test([5, 4, 3, 2, 1], [1, 2, 3, 5, 4]),
        test([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
    ]

    for test in tests:
        output = build_heap(test.input)
        print()
        assert output[0] == test.output, f"{test}, output: {output}"

    print("Success!")


def main():
    n = int(input())
    data = list(map(int, input().split()))
    assert len(data) == n

    heap, swaps = build_heap(data)

    print(len(swaps))
    for i, j in swaps:
        print(i, j)


if __name__ == "__main__":
    # run_tests()
    main()
