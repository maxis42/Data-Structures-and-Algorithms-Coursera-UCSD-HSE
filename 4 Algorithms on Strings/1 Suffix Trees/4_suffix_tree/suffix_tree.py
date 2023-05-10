# Uses python3
import sys
from collections import deque


class TreeNode:
    def __init__(self, parent, start_pos, length):
        self.parent = parent
        self.start_pos = start_pos
        self.length = length

        self.children = []

    def add_child(self, start_pos, length):
        self.children.append(TreeNode(self, start_pos, length))

    # def __repr__(self):
    #     if self.start_pos is None:
    #         # root
    #         parent_text = "None"
    #         node_text = f"Root {self.children}"
    #     else:
    #         if self.parent.start_pos is None:
    #             # parent is root
    #             parent_text = "Root"
    #         else:
    #             # parent is not root
    #             s, e = self.parent.start_pos, self.parent.start_pos+self.parent.length
    #             parent_text = f"{self.text[s:e]}"
    #         s, e = self.start_pos, self.start_pos + self.length
    #         node_text = f"{self.text[s:e]} {self.children}"
    #
    #     return f"{parent_text}->{node_text}"


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.tree = self._construct_tree(self.text)

    @staticmethod
    def _construct_tree(text):
        last_pos = len(text) - 1

        root = TreeNode(
            parent=None,
            start_pos=None,
            length=None,
        )

        pos = 0
        while pos <= last_pos:
            cur_node = root

            pos_inner = pos
            while pos_inner <= last_pos:
                # look for a compatible child
                child_i = None
                for i, child in enumerate(cur_node.children):
                    if text[pos_inner] == text[child.start_pos]:
                        child_i = i

                # if child found iterate over child and split if necessary
                if child_i is not None:
                    child = cur_node.children[child_i]
                    next_node = child
                    for j in range(child.length):
                        child_pos = child.start_pos + j
                        if text[pos_inner] != text[child_pos]:
                            split_node = TreeNode(cur_node, child.start_pos, j)
                            split_node.children = [child]

                            cur_node.children.pop(child_i)
                            cur_node.children.append(split_node)

                            child.parent = split_node
                            child.start_pos = child_pos
                            child.length -= j

                            next_node = split_node

                            # break at the first different letter
                            break

                        pos_inner += 1

                    cur_node = next_node
                # otherwise add the rest part of the text as the leaf
                else:
                    cur_node.add_child(pos_inner, last_pos - pos_inner + 1)
                    pos_inner = last_pos + 1

            pos += 1

        return root

    def print(self):
        q = deque([])
        for child in self.tree.children:
            q.append(child)

        while q:
            cur = q.popleft()
            print(self.text[cur.start_pos:(cur.start_pos + cur.length)])
            for child in cur.children:
                q.append(child)


def run_test():
    text = "ATAAATG$"
    tree = SuffixTree(text)
    tree.print()


def run_algo():
    text = sys.stdin.readline().strip()
    tree = SuffixTree(text)
    tree.print()


if __name__ == "__main__":
    # run_test()
    run_algo()
