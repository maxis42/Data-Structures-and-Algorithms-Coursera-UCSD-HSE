# python3
import random


class ImplicationGraph:
    def __init__(self, n_vars, clauses):
        self.n_vars = n_vars
        self.clauses = clauses

        self._n = self.n_vars * 2
        self.to_inner_id, self.to_orig_id = self._get_id_mappings(self.n_vars)
        self._adj_list, self._adj_list_r = self._construct_adj_lists()

    @staticmethod
    def _get_id_mappings(n_vars):
        """
        For every variable x, introduce two vertices labeled
        by x and not-x. Original IDs transformed to consecutive
        array starting from zero:
            -4, -3, -2, -1,  1,  2,  3,  4
         ->  0,  1,  2,  3,  4,  5,  6,  7
        """
        to_inner_id = dict()
        to_orig_id = [0 for _ in range(n_vars*2)]
        for i in range(1, n_vars + 1):
            inner_i_pos = n_vars + i - 1
            inner_i_neg = n_vars - i

            to_inner_id[i] = inner_i_pos
            to_inner_id[-i] = inner_i_neg

            to_orig_id[inner_i_pos] = i
            to_orig_id[inner_i_neg] = -i
        return to_inner_id, to_orig_id

    def _construct_adj_lists(self):
        adj_list = [set() for _ in range(self._n)]
        adj_list_r = [set() for _ in range(self._n)]

        for x, y in self.clauses:
            x_i = self.to_inner_id[x]
            not_x_i = self.to_inner_id[-x]

            y_i = self.to_inner_id[y]
            not_y_i = self.to_inner_id[-y]

            adj_list[not_x_i].add(y_i)
            adj_list[not_y_i].add(x_i)

            adj_list_r[y_i].add(not_x_i)
            adj_list_r[x_i].add(not_y_i)
        return adj_list, adj_list_r

    def explore_vertex_recursive(self, v, visited, adj_list, postorder):
        visited[v] = True

        for child in adj_list[v]:
            if not visited[child]:
                self.explore_vertex_recursive(child, visited, adj_list, postorder)

        postorder.append(v)

    def dfs_recursive(self, adj_list):
        visited = [False] * len(adj_list)
        postorder = []

        for v in adj_list:
            if not visited[v]:
                # explore every possible vertex reachable from v
                self.explore_vertex_recursive(v, visited, adj_list, postorder)

        return postorder

    @staticmethod
    def explore_vertex(v, visited, adj_list):
        explored = set()
        stack = [v]
        while stack:
            cur = stack.pop()
            if not visited[cur]:
                visited[cur] = True
                explored.add(cur)
                for child in adj_list[cur]:
                    if not visited[child]:
                        stack.append(child)
        return explored

    @staticmethod
    def dfs(adj_list):
        visited = [False] * len(adj_list)
        postorder = []

        for v in range(len(adj_list)):
            if not visited[v]:
                visited[v] = True

                stack = [v]
                while stack:
                    last = stack[-1]

                    no_children = True
                    for child in adj_list[last]:
                        if not visited[child]:
                            stack.append(child)
                            visited[child] = True
                            no_children = False
                            break

                    if no_children:
                        stack.pop()
                        postorder.append(last)
        return postorder

    def find_sccs(self):
        """
        Find strongly connected components.
        """
        postorder_r = self.dfs(self._adj_list_r)

        visited = [False] * self._n
        sccs = []
        sccs_id = [-1 for _ in range(self._n)]
        sccs_id_i = 0
        for v in reversed(postorder_r):
            if not visited[v]:
                explored = self.explore_vertex(v, visited, self._adj_list)
                sccs.append(explored)

                for e in explored:
                    sccs_id[e] = sccs_id_i
                sccs_id_i += 1
        return sccs, sccs_id

    def get_sccs_in_topological_order(self, sccs, sccs_id):
        """
        sort SCCs in topological order
        graph of SCCs is directed acyclic graph
        """
        if len(sccs) <= 1:
            return sccs

        # construct graph of SCCs
        adj_list_sccs = [set() for _ in range(len(sccs))]
        for parent, children in enumerate(self._adj_list):
            parent_scc_id = sccs_id[parent]
            for child in children:
                child_scc_id = sccs_id[child]
                if parent_scc_id != child_scc_id:
                    adj_list_sccs[parent_scc_id].add(child_scc_id)

        postorder = self.dfs(adj_list_sccs)
        sccs = [sccs[i] for i in reversed(postorder)]
        return sccs

    def is_unsatisfiable(self, sccs_id):
        """
        Check if x and not-x lie in the same SCC
        if so, then the formula is unsatisfiable.
        """
        unsatisfiable = False
        for x in range(1, self.n_vars + 1):
            x_scc_i = sccs_id[self.to_inner_id[x]]
            not_x_scc_i = sccs_id[self.to_inner_id[-x]]
            if x_scc_i == not_x_scc_i:
                unsatisfiable = True
                break
        return unsatisfiable


class TwoSAT:
    def __init__(self, n_vars, clauses):
        self.n_vars = n_vars
        self.clauses = clauses

    def is_satisfiable(self):
        ig = ImplicationGraph(self.n_vars, self.clauses)
        sccs, sccs_id = ig.find_sccs()
        if ig.is_unsatisfiable(sccs_id):
            return None
        sccs = ig.get_sccs_in_topological_order(sccs, sccs_id)

        # construct satisfying assignment
        ans = [None for _ in range(self.n_vars)]
        num_assigned = 0
        for scc in reversed(sccs):
            for x in scc:
                var = ig.to_orig_id[x]
                i = abs(var) - 1
                if ans[i] is None:
                    if var > 0:
                        ans[i] = True
                    else:
                        ans[i] = False
                    num_assigned += 1
            if num_assigned == self.n_vars:
                break
        return ans


class ThreeRecoloring:
    def __init__(self, n_vertices, edges, colors, vertex_loop):
        self.n = n_vertices
        self.edges = edges
        self.colors = colors
        self.vertex_loop = vertex_loop

    def solve(self):
        if self.vertex_loop:
            return "Impossible"

        clauses = self._construct_clauses()
        # print(clauses)
        ts = TwoSAT(self.n*2, clauses)
        res = ts.is_satisfiable()
        # print(res)
        if res is None:
            return "Impossible"

        # construct solution
        solution = []
        for i in range(self.n):
            cur_color = self.colors[i]
            new_color_num = 0 if res[2 * i] else 1
            if cur_color == "R":
                new_color = "GB"[new_color_num]
            elif cur_color == "G":
                new_color = "RB"[new_color_num]
            else:  # cur_color == "B"
                new_color = "RG"[new_color_num]
            solution.append(new_color)
        solution = "".join(solution)
        return solution

    def _construct_clauses(self):
        clauses = []

        # exactly one of two other possible colors of vertex
        for i in range(self.n):
            v_col1 = 2 * i + 1
            v_col2 = v_col1 + 1
            clause = [
                [v_col1, v_col2],
                [-v_col1, -v_col2],
            ]
            clauses.extend(clause)

        # different colors on edge ends
        for v1, v2 in self.edges:
            col_v1 = self.colors[v1 - 1]
            col_v2 = self.colors[v2 - 1]

            v1_col1 = 2 * (v1 - 1) + 1
            v1_col2 = v1_col1 + 1
            v2_col1 = 2 * (v2 - 1) + 1
            v2_col2 = v2_col1 + 1
            if col_v1 == col_v2:
                clause = [
                    [-v1_col1, -v2_col1],
                    [-v1_col2, -v2_col2],
                ]
            else:
                if col_v1 == "R":
                    if col_v2 == "G":
                        clause = [[-v1_col2, -v2_col2]]
                    else:  # col_v2 == "B"
                        clause = [[-v1_col1, -v2_col2]]
                elif col_v1 == "G":
                    if col_v2 == "R":
                        clause = [[-v1_col2, -v2_col2]]
                    else:  # col_v2 == "B"
                        clause = [[-v1_col1, -v2_col1]]
                else:  # col_v1 == "B"
                    if col_v2 == "R":
                        clause = [[-v1_col2, -v2_col1]]
                    else:  # col_v2 == "G"
                        clause = [[-v1_col1, -v2_col1]]
            clauses.extend(clause)
        return clauses


def run_test():
    n_vertices = 5
    colors = "RRRGB"
    edges = [
        [1, 3],
        [1, 4],
        [3, 4],
        [2, 4],
        [2, 3],
    ]

    # n_vertices = 4
    # colors = "RGRR"
    # edges = [
    #     [1, 3],
    #     [1, 4],
    #     [3, 4],
    #     [2, 4],
    #     [2, 3],
    # ]

    n_vertices = 3
    colors = "RBG"
    edges = [
        [1, 3],
        [2, 1],
    ]

    tr = ThreeRecoloring(n_vertices, edges, colors)
    res = tr.solve()
    print(res)


def run_algo():
    n_vertices, n_edges = map(int, input().split())
    colors = input()
    edges = []
    vertex_loop = False
    for i in range(n_edges):
        u, v = map(int, input().split())
        if u == v:
            vertex_loop = True
        edges.append((u, v))
    tr = ThreeRecoloring(n_vertices, edges, colors, vertex_loop)
    res = tr.solve()
    print(res)


def stress_test():
    n_vertices = 11
    max_num_edges = int(n_vertices * (n_vertices - 1) / 2)

    false_res = False
    cnt = 0
    while True:
        print(cnt)
        colors = "".join([random.choice("RGB") for _ in range(n_vertices)])
        n_edges = random.randint(0, max_num_edges)

        edges = []
        while len(edges) < n_edges:
            v1 = random.randint(1, n_vertices)
            v2 = random.randint(1, n_vertices)
            if (v1 != v2) and ((v1, v2) not in edges) and ((v2, v1) not in edges):
                edges.append((v1, v2))

        tr = ThreeRecoloring(n_vertices, edges, colors, False)
        res = tr.solve()

        if res == "Impossible":
            continue

        # check that color has changed
        for i in range(n_vertices):
            if colors[i] == res[i]:
                false_res = True
                break

        # check that colors on edge ends are different
        for v1, v2 in edges:
            if res[v1 - 1] == res[v2 - 1]:
                false_res = True
                break

        if false_res:
            # print(f"n_vertices = {n_vertices}")
            # print(f"n_edges = {n_edges}")
            # print(f"colors {colors}")
            for edge in edges:
                print(edge)
            # print(f"res    {res}")
            break

        cnt += 1


if __name__ == "__main__":
    # run_test()
    # stress_test()
    run_algo()
