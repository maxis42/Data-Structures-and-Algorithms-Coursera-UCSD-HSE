# uses python3


class Vertex:
    num_vertices = 0

    def __init__(self, weight):
        self.weight = weight
        self.children = []
        self.v_id = Vertex.num_vertices
        Vertex.num_vertices += 1


class MaxWeightTreeIndependentSet:
    def __init__(self, tree):
        self.tree = tree
        self.n = len(self.tree)

    def max_weight(self):
        max_weight = [0] * self.n
        visited = [False] * self.n
        visit_order = [-1] * self.n
        root_id = 0
        root = self.tree[root_id]

        stack = [root]
        visited[root_id] = True
        visit_order[root_id] = 0
        cur_order = 1
        while stack:
            last = stack[-1]

            no_unvisited_children = True
            for child in last.children:
                if not visited[child.v_id]:
                    visited[child.v_id] = True
                    visit_order[child.v_id] = cur_order
                    cur_order += 1
                    stack.append(child)
                    no_unvisited_children = False
                    break

            if no_unvisited_children:
                stack.pop()

                children_total_weight = 0
                for child in last.children:
                    if visit_order[last.v_id] < visit_order[child.v_id]:
                        children_total_weight += max_weight[child.v_id]

                grand_children_total_weight = 0
                for child in last.children:
                    for grand_child in child.children:
                        if visit_order[last.v_id] < visit_order[grand_child.v_id]:
                            grand_children_total_weight += max_weight[grand_child.v_id]

                max_weight[last.v_id] = max(
                    last.weight + grand_children_total_weight,
                    children_total_weight
                )
        return max_weight[root_id]


def run_test():
    n = 11
    weights = [3, 5, 1, 6, 2, 3, 7, 2, 1, 2, 1]
    edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 4),
        (2, 5),
        (3, 6),
        (3, 7),
        (6, 8),
        (6, 9),
        (6, 10),
    )
    tree = [Vertex(w) for w in weights]
    for a, b in edges:
        tree[a].children.append(tree[b])
        tree[b].children.append(tree[a])

    mwtis = MaxWeightTreeIndependentSet(tree)
    print(mwtis.max_weight())


def run_algo():
    n = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for _ in range(n - 1):
        a_, b_ = list(map(int, input().split()))
        a, b = a_ - 1, b_ - 1
        tree[a].children.append(tree[b])
        tree[b].children.append(tree[a])

    mwtis = MaxWeightTreeIndependentSet(tree)
    print(mwtis.max_weight())


if __name__ == "__main__":
    # run_test()
    run_algo()
