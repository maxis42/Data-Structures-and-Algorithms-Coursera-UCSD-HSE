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

    def inorder(self, node):
        if not node:
            return

        if node.left:
            self.inorder(self.nodes[node.left])

        self.result_inorder.append(node.key)

        if node.right:
            self.inorder(self.nodes[node.right])

    def is_bst(self):
        if len(self.nodes) <= 1:
            return True

        self.inorder(self.root)

        for i in range(len(self.result_inorder)-1):
            if self.result_inorder[i] >= self.result_inorder[i+1]:
                return False

        return True


def main():
    tree = TreeIsBST()
    tree.read()
    # tree.read_test1()
    # tree.read_test2()
    if tree.is_bst():
        print("CORRECT")
    else:
        print("INCORRECT")


if __name__ == "__main__":
    threading.Thread(target=main).start()
