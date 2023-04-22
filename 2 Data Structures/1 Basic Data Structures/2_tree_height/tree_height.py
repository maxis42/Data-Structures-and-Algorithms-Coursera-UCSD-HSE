# python3
from collections import deque


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_index):
        self.children.append(child_index)

    def __str__(self):
        children_names = [child.name for child in self.children]
        return f"Node #{self.name} children: {children_names}"

    def __repr__(self):
        children_names = [child.name for child in self.children]
        return f"Node #{self.name} children: {children_names}"


class TreeHeight:
    def __init__(self, parent):
        self.parent = parent
        self.n = len(self.parent)

        if -1 not in self.parent:
            raise ValueError("No root node!")

        self.nodes = [Node(i) for i in range(self.n)]

        # add children to the nodes
        for child_index in range(self.n):
            parent_index = self.parent[child_index]
            if parent_index == -1:
                self.root = child_index
            else:
                self.nodes[parent_index].add_child(self.nodes[child_index])

    #         print(self.nodes)

    def compute_height_naive(self):
        """
        For every node get its height. Then take the max height
        between all nodes.
        """
        max_height = 0

        for vertex in range(self.n):
            height = 0
            i = vertex
            while i != -1:
                height += 1
                i = self.parent[i]
            max_height = max(max_height, height)

        return max_height

    def compute_height(self):
        """
        Compute tree height with breadth-first search. Use deque to store
        current level nodes.
        """
        d = deque()

        d.append(self.nodes[self.root])
        height = 0

        while len(d):
            height += 1
            for i in range(len(d)):
                node = d.popleft()

                for child in node.children:
                    d.append(child)

        return height


if __name__ == '__main__':
    n = int(input())
    parents = list(map(int, input().split()))
    tree = TreeHeight(parents)
    print(tree.compute_height())
