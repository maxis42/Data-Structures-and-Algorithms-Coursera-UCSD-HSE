# python3
import sys
from collections import deque


class SuffixTreeNode:
    def __init__(self, parent, string_depth, edge_start, edge_end):
        self.parent = parent
        self.string_depth = string_depth
        self.edge_start = edge_start
        self.edge_end = edge_end

        self.children = dict()
        self.node_id = None


class SuffixTree:
    """
    Build suffix tree of the string text given its
    suffix array and  longest common prefix (LCP) array.

    Return the tree as a mapping from a node ID to
    the list of all outgoing edges of the corresponding
    node. The edges in the list must be sorted in the
    ascending order by the first character of the edge
    label. Root must have node ID = 0, and all other
    node IDs must be different non-negative integers.
    Each edge must be represented by a tuple
    (node, start, end), where
        * node is the node ID of the ending node of the
        edge
        * start is the starting position (0-based) of
        the substring of text corresponding to the edge
        label
        * end is the first position (0-based) after the
        end of the substring corresponding to the edge
        label

    For example, if text = "ACACAA$", an edge with label
    "$" from root to a node with ID 1 must be
    represented by a tuple (1, 6, 7). This edge must be
    present in the list tree[0] (corresponding to the
    root node), and it should be the first edge in the
    list (because it has the smallest first character of
    all edges outgoing from the root).
    """

    def __init__(self, text, suffix_arr, lcp, alphabet):
        self.text = text
        self.suffix_arr = suffix_arr
        # longest common prefix
        self.lcp = lcp
        self.alphabet = sorted(alphabet)

        self.root = self._construct_tree(self.text, self.suffix_arr, self.lcp)
        self.edges = self._construct_edges(self.root)

    def _construct_edges(self, root):
        edges = dict()
        root.node_id = 0
        cur_id = 1
        q = deque([root])
        while q:
            cur = q.popleft()

            if cur.children:
                edges[cur.node_id] = []
                for char in self.alphabet:
                    if char in cur.children:
                        child = cur.children[char]
                        child.node_id = cur_id
                        cur_id += 1
                        edges[cur.node_id].append((child.node_id, child.edge_start, child.edge_end))
                        q.append(child)

        return edges

    def print_edges(self, edges):
        for node in edges:
            s = "Node {} / edges ".format(node)
            edges_s = ""
            for edge in edges[node]:
                edges_s += "#{}-{} ".format(edge[0], self.text[edge[1]:(edge[2] + 1)])
            s += edges_s
            print(s)

    def _construct_tree(self, text, suffix_arr, lcp):
        root = SuffixTreeNode(
            parent=None,
            string_depth=0,
            edge_start=-1,
            edge_end=-1,
        )

        lcp_prev = 0
        cur_node = root

        for i in range(len(text)):
            suffix = suffix_arr[i]

            while cur_node.string_depth > lcp_prev:
                cur_node = cur_node.parent

            if cur_node.string_depth == lcp_prev:
                cur_node = self._create_new_leaf(cur_node, text, suffix)
            else:
                edge_start = suffix_arr[i - 1] + cur_node.string_depth
                offset = lcp_prev - cur_node.string_depth
                mid_node = self._break_edge(cur_node, text, edge_start, offset)
                cur_node = self._create_new_leaf(mid_node, text, suffix)

            if i < len(text) - 1:
                lcp_prev = lcp[i]

        return root

    @staticmethod
    def _create_new_leaf(node, text, suffix):
        leaf = SuffixTreeNode(
            parent=node,
            string_depth=len(text) - suffix,
            edge_start=node.string_depth + suffix,
            edge_end=len(text) - 1,
        )
        node.children[text[leaf.edge_start]] = leaf
        return leaf

    @staticmethod
    def _break_edge(node, text, start, offset):
        start_char = text[start]
        mid_char = text[start + offset]
        mid_node = SuffixTreeNode(
            parent=node,
            string_depth=node.string_depth + offset,
            edge_start=start,
            edge_end=start + offset - 1,
        )
        mid_node.children[mid_char] = node.children[start_char]
        node.children[start_char].parent = mid_node
        node.children[start_char].edge_start += offset
        node.children[start_char] = mid_node
        return mid_node

    def output_tree(self):
        """
        Output the edges of the suffix tree in the
        required order.

        Note that we use here the contract that the root
        of the tree will have node ID = 0 and that each
        vector of outgoing edges will be sorted by the
        first character of the corresponding edge label.

        The following code avoids recursion to avoid
        stack overflow issues. It uses two stacks to
        convert recursive function to a while loop. This
        code is an equivalent of

            OutputEdges(tree, 0)

        for the following _recursive_ function OutputEdges:

        def OutputEdges(tree, node_id):
            edges = tree[node_id]
            for edge in edges:
                print("%d %d" % (edge[1], edge[2]))
                OutputEdges(tree, edge[0])
        """
        stack = [(0, 0)]
        while stack:
            node, edge_index = stack.pop()
            if node not in self.edges:
                continue
            edges = self.edges[node]
            if edge_index + 1 < len(edges):
                stack.append((node, edge_index + 1))
            print("%d %d" % (edges[edge_index][1], edges[edge_index][2] + 1))
            stack.append((edges[edge_index][0], 0))


def run_test():
    alphabet = "ACGT$"
    text = "GTAGT$"
    suffix_array = [5, 2, 3, 0, 4, 1]
    lcp = [0, 0, 2, 0, 1]

    text = "ATAAATG$"
    suffix_array = [7, 2, 3, 0, 4, 6, 1, 5]
    lcp = [0, 2, 1, 2, 0, 0, 1]

    print(text)
    tree = SuffixTree(text, suffix_array, lcp, alphabet)
    tree.output_tree()


def run_algo():
    alphabet = "ACGT$"
    text = sys.stdin.readline().strip()
    suffix_array = list(map(int, sys.stdin.readline().strip().split()))
    lcp = list(map(int, sys.stdin.readline().strip().split()))
    print(text)
    tree = SuffixTree(text, suffix_array, lcp, alphabet)
    tree.output_tree()


if __name__ == "__main__":
    # run_test()
    run_algo()
