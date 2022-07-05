# python3

import sys
import threading
from time import sleep

sys.setrecursionlimit(10 ** 6)  # max depth of recursion
threading.stack_size(2 ** 27)  # new thread will get stack of such size


class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left if left != -1 else None
        self.right = right if right != -1 else None


class TreeOrders:
    def __init__(self):
        self.nodes = []
        self.root = None
        self.result_inorder = []
        self.result_preorder = []
        self.result_postorder = []

    def read(self):
        n = int(sys.stdin.readline())

        for i in range(n):
            key, left, right = map(int, sys.stdin.readline().split())
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def read_test1(self):
        n = 5
        data = (
            (4, 1, 2),
            (2, 3, 4),
            (5, -1, -1),
            (1, -1, -1),
            (3, -1, -1),
        )

        for i in range(n):
            key, left, right = data[i]
            node = Node(key, left, right)
            self.nodes.append(node)

        self.root = self.nodes[0]

    def run_traversals(self):
        self.inorder(self.root)
        self.preorder(self.root)
        self.postorder(self.root)

    def inorder(self, node):
        if not node:
            return

        if node.left:
            self.inorder(self.nodes[node.left])

        self.result_inorder.append(node.key)

        if node.right:
            self.inorder(self.nodes[node.right])

    def preorder(self, node):
        if not node:
            return

        self.result_preorder.append(node.key)

        if node.left:
            self.preorder(self.nodes[node.left])

        if node.right:
            self.preorder(self.nodes[node.right])

    def postorder(self, node):
        if not node:
            return

        if node.left:
            self.postorder(self.nodes[node.left])

        if node.right:
            self.postorder(self.nodes[node.right])

        self.result_postorder.append(node.key)


def main():
    tree = TreeOrders()
    tree.read()
    # tree.read_test1()
    tree.run_traversals()
    print(" ".join(str(x) for x in tree.result_inorder))
    print(" ".join(str(x) for x in tree.result_preorder))
    print(" ".join(str(x) for x in tree.result_postorder))


def run_algo():
    threading.Thread(target=main).start()


if __name__ == "__main__":
    run_algo()
