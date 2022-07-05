# python3

from sys import stdin

MODULO = 1000000001


class Node:
    def __init__(self, key, subtree_sum=0, left=None, right=None, parent=None):
        self.key = key
        self.subtree_sum = subtree_sum
        self.left = left
        self.right = right
        self.parent = parent


class SplayTree:
    LAST_SUM_RESULT = 0

    def __init__(self, root=None):
        self.root = None
        if root is not None:
            self.root = root

    @staticmethod
    def update(node):
        if node is None:
            return

        node.subtree_sum = node.key
        if node.left is not None:
            node.subtree_sum += node.left.subtree_sum
            node.left.parent = node
        if node.right is not None:
            node.subtree_sum += node.right.subtree_sum
            node.right.parent = node

    def small_rotation(self, node):
        """
        This simple rotation is applied at the root of the splay
        tree, moving the splayed node x up to become the new tree
        root. Here we have A < x < B < y < C, and the splayed node
        is either x or y depending on which direction the rotation
        is.
            y             x
           / \           / \
          x   C   <->   A   y
         / \               / \
        A   B             B   C
        """
        parent = node.parent

        if parent is None:
            return

        grandparent = node.parent.parent

        if parent.left == node:
            m = node.right
            node.right = parent
            parent.left = m
        else:
            m = node.left
            node.left = parent
            parent.right = m

        self.update(parent)
        self.update(node)

        node.parent = grandparent

        if grandparent is not None:
            if grandparent.left == parent:
                grandparent.left = node
            else:
                grandparent.right = node

    def big_rotation(self, node):
        """
        1. Zig-Zig and Zag-Zag
        Lower down in the tree rotations are performed in pairs
        so that nodes on the path from the splayed node to the
        root move closer to the root on average. In the "zig-zig"
        case, the splayed node x is the left child of a left child
        or the splayed node z is the right child of a right child
        ("zag-zag").
        A < x < B < y < C < z < D
              z             x
             / \           / \
            y   D         A   y
           / \      <->      / \
          x   C             B   z
         / \                   / \
        A   B                 C   D

        2. Zig-Zag
        In the "zig-zag" case, the splayed node is the left
        child of a right child or vice-versa. The rotations
        produce a subtree whose height is less than that of
        the original tree. Thus, this rotation improves the
        balance of the tree. In each of the two cases shown,
        y is the splayed node.
        A < y < B < x < z < D
               z                x                y
              / \              / \              / \
             y   D            /   \            A   z
            / \         ->   y     z    <-        / \
           A   x            / \   / \            x   D
              / \          A   B C   D          / \
             B   C                             B   C
        """
        if (node.parent.left == node) and (node.parent.parent.left == node.parent):
            # Zig-Zig
            self.small_rotation(node.parent)
            self.small_rotation(node)
        elif (node.parent.right == node) and (node.parent.parent.right == node.parent):
            # Zag-Zag
            self.small_rotation(node.parent)
            self.small_rotation(node)
        else:
            # Zig-Zag
            self.small_rotation(node)
            self.small_rotation(node)

    def splay(self, node):
        """
        Makes splay of the given vertex and makes it the new root.
        """
        if node is None:
            return

        while node.parent is not None:
            if node.parent.parent is None:
                # the splayed node become the new tree root
                self.small_rotation(node)
                break
            self.big_rotation(node)

        self.root = node
        self.root.parent = None

    def insert(self, key):
        """
        To insert a value x into a splay tree:
        - Insert x as with a normal binary search tree.
        - When an item is inserted, a splay is performed.
        - As a result, the newly inserted node x becomes the root of the tree.
        """
        new_node = Node(key, key)

        # empty tree
        if self.root is None:
            self.root = new_node
            return

        # the node is already in the tree
        last_visited_node, _ = self.find(key)
        if last_visited_node.key == key:
            return

        # add new node
        node = self.root
        while node is not None:
            if key < node.key:
                if node.left is None:
                    node.left = new_node
                    new_node.parent = node
                    break
                else:
                    node = node.left
            else:
                if node.right is None:
                    node.right = new_node
                    new_node.parent = node
                    break
                else:
                    node = node.right

        self.splay(new_node)

    def find(self, key):
        """
        Searches for the given key in the tree with the given root
        and calls splay for the deepest visited node after that.

        Returns a pair of the result and the new root.
        If found, result is a pointer to the node with the given key.
        Otherwise, result is a pointer to the node with the biggest
        smaller key (previous value in the order).
        """
        # empty tree
        if self.root is None:
            return None

        node = self.root
        last_visited_node = node
        biggest_smaller_node = None

        while node is not None:
            last_visited_node = node

            if (node.key <= key) and\
                    ((biggest_smaller_node is None) or (node.key > biggest_smaller_node.key)):
                biggest_smaller_node = node

            if node.key == key:
                break
            if node.key > key:
                node = node.left
            else:
                node = node.right

        if biggest_smaller_node is not None:
            self.splay(biggest_smaller_node)
        else:
            self.splay(last_visited_node)

        return last_visited_node, biggest_smaller_node

    def split(self, key):
        """
        Given a tree and an element x, return two new trees:
        one containing all elements less than or equal to x
        and the other containing all elements greater than x.
        This can be done in the following way:
        - Splay x. Now it is in the root so the tree to its
        left contains all elements smaller than x and the tree
        to its right contains all element larger than x.
        - Split the right subtree from the rest of the tree.
        """
        last_visited_node, biggest_smaller_node = self.find(key)
        if biggest_smaller_node is not None:
            right_child = biggest_smaller_node.right

            left = SplayTree(root=biggest_smaller_node)
            if left.root is not None:
                left.root.right = None
                self.update(left.root)

            right = SplayTree(root=right_child)
            if right.root is not None:
                right.root.parent = None
        else:
            left = SplayTree(root=None)
            right = SplayTree(root=last_visited_node)
            if right.root is not None:
                right.root.parent = None

        return left, right

    def merge(self, left, right):
        """
        Given two trees S and T such that all elements of S
        are smaller than the elements of T, the following
        steps can be used to join them to a single tree:
        - Splay the largest item in S. Now this item is in
        the root of S and has a null right child.
        - Set the right child of the new root to T.
        """
        if (left.root is None) and (right.root is None):
            self.root = None
        elif left.root is None:
            self.root = right.root
        elif right.root is None:
            self.root = left.root
        else:
            max_left_node = left.root
            while max_left_node.right is not None:
                max_left_node = max_left_node.right

            left.splay(max_left_node)

            left.root.right = right.root

            left.update(left.root)
            left.update(left.root.right)
            self.root = left.root

    def search(self, key):
        # empty tree
        if self.root is None:
            return False

        last_visited_node, _ = self.find(key)
        if last_visited_node.key == key:
            return True
        return False

    def erase(self, key):
        """
        To delete a node x, use the same method as with a
        binary search tree:
            - If x has two children:
                - Swap its value with that of either the
                rightmost node of its left sub tree (its
                in-order predecessor) or the leftmost node
                of its right subtree (its in-order
                successor).
                - Remove that node instead.

        In this way, deletion is reduced to the problem of
        removing a node with 0 or 1 children. Unlike a binary
        search tree, in a splay tree after deletion, we splay
        the parent of the removed node to the top of the tree.

        Alternatively (this one implemented):

            - The node to be deleted is first splayed, i.e.
            brought to the root of the tree and then deleted.
            Leaves the tree with two sub trees.
            - The two sub-trees are then joined using a "join"
            operation.
        """
        # empty tree
        if self.root is None:
            return

        last_visited_node, _ = self.find(key)
        if last_visited_node.key == key:
            left = SplayTree(last_visited_node.left)
            if left.root is not None:
                left.root.parent = None

            right = SplayTree(last_visited_node.right)
            if right.root is not None:
                right.root.parent = None

            self.merge(left, right)

    def sum_(self, min_value, max_value):
        ans = 0

        if self.root is not None:
            ans = self.root.subtree_sum

            left, middle = self.split(min_value)
            if left.root is not None:
                ans -= left.root.subtree_sum
                if left.root.key == min_value:
                    ans += left.root.key
            self.merge(left, middle)

            middle, right = self.split(max_value)
            if right.root is not None:
                ans -= right.root.subtree_sum
            self.merge(middle, right)

        return ans

    def parse_operation(self, line):
        line = line.split()

        if line[0] == "+":
            x = int(line[1])
            self.insert((x + self.LAST_SUM_RESULT) % MODULO)
        elif line[0] == "-":
            x = int(line[1])
            self.erase((x + self.LAST_SUM_RESULT) % MODULO)
        elif line[0] == "?":
            x = int(line[1])
            print(
                "Found" if self.search((x + self.LAST_SUM_RESULT) % MODULO)
                else "Not found"
            )
        elif line[0] == "s":
            min_value = int(line[1])
            max_value = int(line[2])
            res = self.sum_(
                (min_value + self.LAST_SUM_RESULT) % MODULO,
                (max_value + self.LAST_SUM_RESULT) % MODULO
            )
            print(res)
            self.LAST_SUM_RESULT = res % MODULO

    def traverse_tree(self):
        if self.root is None:
            return

        print("start traversing")
        self.traverse_tree_(self.root)
        print("end traversing")

    def traverse_tree_(self, node):
        if node is None:
            return

        self.traverse_tree_(node.left)
        print(f"Node: key={node.key}, subtree_sum={node.subtree_sum}")
        self.traverse_tree_(node.right)


def run_tests():
    tree = SplayTree()
    ops = (
        "? 1",
        "+ 1",
        "? 1",
        "+ 2",
        "s 1 2",
        "+ 1000000000",
        "? 1000000000",
        "- 1000000000",
        "? 1000000000",
        "s 999999999 1000000000",
        "- 2",
        "? 2",
        "- 0",
        "+ 9",
        "s 0 9",
    )

    for op in ops:
        print(f"Operation: {op}")
        tree.parse_operation(op)
        tree.traverse_tree()
        print()


def run_algo():
    tree = SplayTree()

    n = int(stdin.readline())

    for _ in range(n):
        line = stdin.readline()
        tree.parse_operation(line)


if __name__ == "__main__":
    run_algo()
    # run_tests()
