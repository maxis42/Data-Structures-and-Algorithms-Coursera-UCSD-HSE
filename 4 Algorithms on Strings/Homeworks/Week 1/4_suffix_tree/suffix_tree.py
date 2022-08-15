# Uses python3
import sys
from collections import deque


# Return the trie built from patterns
# in the form of a dictionary of dictionaries,
# e.g. {0:{'A':1,'T':2},1:{'C':3}}
# where the key of the external dictionary is
# the node ID (integer), and the internal dictionary
# contains all the trie edges outgoing from the corresponding
# node, and the keys are the letters on those edges, and the
# values are the node IDs to which these edges lead.


class TreeNode:
    def __init__(self, parent, start_pos, length):
        self.parent = parent
        self.start_pos = start_pos
        self.length = length

        self.children = []

    def add_child(self, start_pos, length):
        self.children.append(TreeNode(self, start_pos, length))

    def __repr__(self):
        return "Node(pos={}, length={}, children={})".format(self.start_pos, self.length, self.children)


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.tree = self._construct_tree(self.text)

    @staticmethod
    def _construct_tree(text):
        def print_tree(tree):
            print("Start printing tree...")
            q = deque([tree])
            while q:
                cur = q.popleft()
                print(cur)
                for child in cur.children:
                    q.append(child)
            print("Tree printed!\n")

        last_pos = len(text) - 1

        root = TreeNode(
            parent=None,
            start_pos=None,
            length=None,
        )

        pos = 0
        while pos <= last_pos:
            print_tree(root)
            cur_node = root

            pos_inner = pos
            while pos_inner <= last_pos:
                next_node = None
                for i, child in enumerate(cur_node.children):
                    if text[pos_inner] == text[child.start_pos]:
                        # child has the same start letter
                        next_node = child

                        # search for the split node if child and current text are not the same
                        for j in range(child.length):
                            if text[pos_inner + j] != text[child.start_pos + j]:
                                print(pos_inner, j)

                                split_node = TreeNode(cur_node, pos_inner, j)
                                split_node.children = [child]
                                split_node.add_child(pos_inner, last_pos - pos_inner)

                                cur_node.children = cur_node.children[:i] + cur_node.children[i+1:]
                                cur_node.children.append(split_node)

                                child.start_pos += j
                                child.length -= j

                                next_node = split_node
                                pos_inner += j
                                break
                        continue

                if next_node is None:
                    cur_node.add_child(pos_inner, last_pos - pos_inner)
                    pos_inner = last_pos + 1

            pos += 1

        return root

    def print(self):
        q = deque([self.tree])
        while q:
            cur = q.popleft()
            print("Start pos: {}; length: {}; children: {}".format(cur.start_pos, cur.length, cur.children))
            for child in cur.children:
                q.append(child)


def run_test():
    text = "panamabananas"
    tree = SuffixTree(text)
    tree.print()


def run_algo():
    text = sys.stdin.readline().strip()
    tree = SuffixTree(text)
    tree.print()


if __name__ == "__main__":
    run_test()
    # run_algo()
