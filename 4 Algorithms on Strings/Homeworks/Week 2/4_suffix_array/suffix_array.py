# python3
import sys


def build_suffix_array(text):
    """
    Build suffix array of the string text and
    return a list result of the same length as the text
    such that the value result[i] is the index (0-based)
    in text where the i-th lexicographically smallest
    suffix of text starts.
    """
    data = []
    for i in range(len(text)):
        data.append((text[i:], i))

    data.sort(key=lambda x: x[0])
    result = [i for s, i in data]

    return result


def run_test():
    text = "PANAMABANANAS$"
    print(" ".join(map(str, build_suffix_array(text))))


def run_algo():
    text = sys.stdin.readline().strip()
    print(" ".join(map(str, build_suffix_array(text))))


if __name__ == "__main__":
    # run_test()
    run_algo()
