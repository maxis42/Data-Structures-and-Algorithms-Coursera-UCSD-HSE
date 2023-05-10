# Uses python3
import sys
from collections import deque


class TreeNode:
    def __init__(self, parent, start_pos, length, initial_start_pos):
        self.parent = parent
        self.start_pos = start_pos
        self.length = length
        self.initial_start_pos = initial_start_pos

        self.children = []

        self.text_type = None

    def add_child(self, start_pos, length, initial_start_pos):
        self.children.append(TreeNode(self, start_pos, length, initial_start_pos))

    def __repr__(self):
        if self.start_pos is None:
            # root
            parent_text = "None"
            node_text = "Root {}".format(self.children)
        else:
            if self.parent.start_pos is None:
                # parent is root
                parent_text = "Root"
            else:
                # parent is not root
                s, e = self.parent.start_pos, self.parent.start_pos+self.parent.length
                parent_text = "{}".format(self.text[s:e])
            s, e = self.start_pos, self.start_pos + self.length
            node_text = "{} {}".format(self.text[s:e], self.children)

        return "{}->{}".format(parent_text, node_text)


class SuffixTree:
    def __init__(self, text):
        self.text = text
        self.tree = self._construct_tree(self.text)

    @staticmethod
    def _construct_tree(text):
        last_pos = len(text) - 1

        root = TreeNode(None, None, None, None)

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
                            split_node = TreeNode(cur_node, child.start_pos, j, None)
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
                    cur_node.add_child(pos_inner, last_pos - pos_inner + 1, pos)
                    pos_inner = last_pos + 1

            pos += 1

        return root

    def print(self):
        q = deque([])
        for child in self.tree.children:
            q.append(child)

        while q:
            cur = q.popleft()
            # print(self.text[cur.start_pos:(cur.start_pos + cur.length)])
            for child in cur.children:
                q.append(child)

    def shortest_substring_in_first_not_in_second(self, n, s1):
        min_ss = None

        s1_end_pos = n

        q_list = []
        q = deque([self.tree])
        while q:
            cur = q.popleft()
            q_list.append(cur)
            for child in cur.children:
                q.append(child)

        for node in reversed(q_list):
            if node.children:
                first_type = False
                second_type = False
                for child in node.children:
                    if (child.text_type == "12") or (first_type and second_type):
                        node.text_type = "12"
                        break
                    if child.text_type == "1":
                        first_type = True
                    else:
                        second_type = True

                if node.text_type is None:
                    if first_type and second_type:
                        node.text_type = "12"
                    elif first_type:
                        node.text_type = "1"
                    else:
                        # only second type
                        node.text_type = "2"
            else:
                if node.start_pos > s1_end_pos:
                    node.text_type = "2"
                else:
                    node.text_type = "1"

        q = deque([])
        for child in self.tree.children:
            q.append(child)

        while q:
            cur = q.popleft()

            if cur.text_type == "12":
                for child in cur.children:
                    q.append(child)
            elif cur.text_type == "1":
                end_pos = min(cur.start_pos + 1, s1_end_pos)
                candidate = s1[cur.start_pos:end_pos]
                if candidate != "":
                    while cur.parent.parent is not None:
                        cur = cur.parent
                        end_pos = cur.start_pos + cur.length
                        candidate = s1[cur.start_pos:end_pos] + candidate

                    if (min_ss is None) or (len(candidate) < len(min_ss)):
                        min_ss = candidate
            else:
                # node.text_type == "2" -> skip such nodes
                continue

        return min_ss


def print_tree(tree):
    q = deque([tree])
    while q:
        cur = q.popleft()
        print(cur)
        for child in cur.children:
            q.append(child)


def run_test():
    text1 = "AAA"
    text2 = "TTT"

    text1 = "CCAAGCTGCTAGAGG"
    text2 = "CATGCTGGGCTGGCT"
    n = len(text1)
    s = "{}#{}$".format(text1, text2)
    TreeNode.text = s
    tree = SuffixTree(s)
    print_tree(tree.tree)
    res = tree.shortest_substring_in_first_not_in_second(n, text1)
    print(res)


def run_algo():
    text1 = sys.stdin.readline().strip()
    text2 = sys.stdin.readline().strip()
    n = len(text1)
    s = "{}#{}$".format(text1, text2)
    tree = SuffixTree(s)
    res = tree.shortest_substring_in_first_not_in_second(n, text1)
    print(res)


if __name__ == "__main__":
    # run_test()
    run_algo()
