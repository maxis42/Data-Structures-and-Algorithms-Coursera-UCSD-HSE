# Uses python3
import sys
from collections import deque


class TrieNode:
    def __init__(self, parent, value, node_id):
        self.parent = parent
        self.value = value
        self.node_id = node_id

        self.children = dict()

    def add_child(self, value, node_id):
        self.children[value] = TrieNode(self, value, node_id)


class Trie:
    def __init__(self, patterns):
        self.patterns = patterns

        self.tree = TrieNode(None, None, 0)
        self._construct_trie(self.patterns)

    def _construct_trie(self, patterns):
        node_id = 1

        for pattern in patterns:
            cur = self.tree
            for c in pattern:
                if c not in cur.children:
                    cur.add_child(c, node_id)
                    node_id += 1

                cur = cur.children[c]

            cur.add_child("$", None)

    def print_adj_list(self):
        q = deque([self.tree])

        while q:
            cur = q.popleft()

            if cur.value is not None:
                print("{}->{}:{}".format(cur.parent.node_id, cur.node_id, cur.value))

            for node in cur.children.values():
                q.append(node)

    def find_occurrences(self, text):
        pos = 0
        found_positions = []

        while pos < len(text):
            node = self.tree

            for c in text[pos:]:
                if c in node.children:
                    node = node.children[c]

                    if "$" in node.children:
                        found_positions.append(pos)
                        break
                else:
                    break

            pos += 1

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
