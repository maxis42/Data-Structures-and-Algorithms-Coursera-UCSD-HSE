#!/usr/bin/python3

import sys
import threading

sys.setrecursionlimit(10 ** 8)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left if left != -1 else None
        self.right = right if right != -1 else None


class TreeIsBST:
    def __init__(self):
        self.nodes = []
        self.root = None
        self.keys_inorder = []
        self.result_inorder = []

    def read(self):
        n = int(sys.stdin.readline())

        for i in range(n):
            key, left, right = map(int, sys.stdin.readline().split())
            node = Node(key, left, right)
            self.nodes.append(node)

        if n > 0:
            self.root = self.nodes[0]

    def read_test1(self):
        # CORRECT
        n = 3
        data = (
            (2, 1, 2),
            (1, -1, -1),
            (3, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test2(self):
        # INCORRECT
        n = 3
        data = (
            (1, 1, 2),
            (2, -1, -1),
            (3, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test3(self):
        # CORRECT
        n = 3
        data = (
            (2, 1, 2),
            (1, -1, -1),
            (2, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test4(self):
        # INCORRECT
        n = 3
        data = (
            (2, 1, 2),
            (2, -1, -1),
            (3, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test5(self):
        # CORRECT
        n = 0
        data = ()

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        if n > 0:
            self.root = self.nodes[0]

    def read_test6(self):
        # CORRECT
        n = 1
        data = (
            (2147483647, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        if n > 0:
            self.root = self.nodes[0]

    def read_test7(self):
        # CORRECT
        n = 5
        data = (
            (1, -1, 1),
            (2, -1, 2),
            (3, -1, 3),
            (4, -1, 4),
            (5, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test8(self):
        # CORRECT
        n = 7
        data = (
            (4, 1, 2),
            (2, 3, 4),
            (6, 5, 6),
            (1, -1, -1),
            (3, -1, -1),
            (5, -1, -1),
            (7, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_testN(self):
        # # CORRECT
        # n = 3
        # data = (
        #     (9, -1, 1),
        #     (10, 2, -1),
        #     (9, -1, -1),
        # )

        # # INCORRECT
        # n = 5
        # data = (
        #     (9, -1, 1),
        #     (10, 2, 3),
        #     (9, -1, -1),
        #     (10, 4, -1),
        #     (10, -1, -1)
        # )

        # # INCORRECT
        # n = 4
        # data = (
        #     (9, -1, 1),
        #     (8, -1, 2),
        #     (8, 3, -1),
        #     (8, -1, -1)
        # )

        # # CORRECT
        # n = 4
        # data = (
        #     (9, -1, 1),
        #     (30, 2, -1),
        #     (19, 3, -1),
        #     (9, -1, -1)
        # )

        # INCORRECT
        n = 3
        data = (
            (9, -1, 1),
            (30, 2, -1),
            (8, -1, -1)
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def inorder(self, node):
        if not node:
            return

        if node.left:
            self.inorder(self.nodes[node.left])

        self.keys_inorder.append(node.key)

        if node.left and node.right:
            if self.nodes[node.left].key < node.key <= self.nodes[node.right].key:
                self.result_inorder.append(True)
            else:
                self.result_inorder.append(False)
        elif node.left:
            if self.nodes[node.left].key < node.key:
                self.result_inorder.append(True)
            else:
                self.result_inorder.append(False)
        elif node.right:
            if node.key <= self.nodes[node.right].key:
                self.result_inorder.append(True)
            else:
                self.result_inorder.append(False)
        else:
            self.result_inorder.append(True)

        if node.right:
            self.inorder(self.nodes[node.right])

    def is_bst(self):
        if len(self.nodes) <= 1:
            return True

        self.inorder(self.root)

        keys_sorted = self.is_keys_sorted()

        if all(self.result_inorder) and keys_sorted:
            return True

        return False

    def is_keys_sorted(self):
        for i in range(len(self.keys_inorder)-1):
            if self.keys_inorder[i] > self.keys_inorder[i+1]:
                return False
        return True


def main():
    tree = TreeIsBST()
    tree.read()
    # tree.read_test1()
    # tree.read_test2()
    # tree.read_test3()
    # tree.read_test4()
    # tree.read_test5()
    # tree.read_test6()
    # tree.read_test7()
    # tree.read_test8()
    # tree.read_testN()
    if tree.is_bst():
        print("CORRECT")
    else:
        print("INCORRECT")


if __name__ == "__main__":
    threading.Thread(target=main).start()
