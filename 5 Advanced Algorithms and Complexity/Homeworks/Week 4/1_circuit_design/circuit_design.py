# python3


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

    def is_satisfiable_naive(self):
        """
        This solution tries all possible 2^n variable assignments.
        It is too slow to pass the problem.
        Implement a more efficient algorithm.
        """
        for mask in range(1 << self.n_vars):
            result = [(mask >> i) & 1 for i in range(self.n_vars)]
            formula_is_satisfied = True
            for clause in self.clauses:
                clause_is_satisfied = False
                if result[abs(clause[0]) - 1] == (clause[0] < 0):
                    clause_is_satisfied = True
                if result[abs(clause[1]) - 1] == (clause[1] < 0):
                    clause_is_satisfied = True
                if not clause_is_satisfied:
                    formula_is_satisfied = False
                    break
            if formula_is_satisfied:
                return result
        return None


def run_test():
    n_vars = 3
    clauses = [
        (1, -3),
        (-1, 2),
        (-2, -3),
    ]

    # n_vars = 1
    # clauses = [
    #     (1, 1),
    #     (-1, -1),
    # ]

    # n_vars = 5
    # clauses = [
    #     (-1, -2),
    #     (-2, -3),
    #     (-3, -4),
    #     (4, -5),
    #     (-1, -5),
    # ]

    sat = TwoSAT(n_vars, clauses)
    result = sat.is_satisfiable()
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(i + 1 if result[i] else -i - 1) for i in range(n_vars)))


def run_algo():
    n_vars, n_clauses = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(n_clauses)]

    sat = TwoSAT(n_vars, clauses)
    result = sat.is_satisfiable()
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(i + 1 if result[i] else -i - 1) for i in range(n_vars)))


if __name__ == "__main__":
    # run_test()
    run_algo()
