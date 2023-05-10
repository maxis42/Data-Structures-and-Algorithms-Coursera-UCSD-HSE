# Uses python3
import sys
from collections import deque


class TrieNode:
    def __init__(self, is_terminal=False):
        self.children = dict()
        self.is_terminal = is_terminal

    def add_child(self, value, is_terminal=False):
        if value not in self.children:
            self.children[value] = TrieNode(is_terminal)
        elif is_terminal:
            self.children[value].is_terminal = True


class Trie:
    def __init__(self, patterns):
        self.patterns = patterns

        self.tree = TrieNode()
        self._construct_trie(self.patterns)

    def _construct_trie(self, patterns):
        for pattern in patterns:
            cur = self.tree
            for c in pattern:
                cur.add_child(c)
                cur = cur.children[c]
            cur.is_terminal = True

    def find_occurrences(self, text):
        found_positions = []
        for pos in range(len(text)):
            v = self.tree

            for c in text[pos:]:
                if c in v.children:
                    v = v.children[c]
                    if v.is_terminal:
                        found_positions.append(pos)
                        break
                else:
                    break
        return found_positions


def run_test():
    text = "AATCGGGTTCAATCGGGGT"
    patterns = (
        "ATCG",
        "GGGT",
        "GT",
        "T",
        "A",
    )
    tree = Trie(patterns)
    found_positions = tree.find_occurrences(text)
    print(" ".join(map(str, found_positions)))


def run_algo():
    text = sys.stdin.readline().strip()
    num_patterns = int(sys.stdin.readline())
    patterns = [sys.stdin.readline().strip() for _ in range(num_patterns)]

    tree = Trie(patterns)
    found_positions = tree.find_occurrences(text)
    print(" ".join(map(str, found_positions)))


if __name__ == "__main__":
    # run_test()
    run_algo()
