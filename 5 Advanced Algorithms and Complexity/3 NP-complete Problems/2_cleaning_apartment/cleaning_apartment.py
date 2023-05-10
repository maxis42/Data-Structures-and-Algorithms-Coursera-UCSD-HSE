# python3
from collections import defaultdict


class HamiltonianPathToSAT:
    def __init__(self, num_vertices, edges):
        self.num_vertices = num_vertices
        self.edges = edges

    def _belongs_to_a_path(self):
        sat = []
        for v in range(1, self.num_vertices + 1):
            clause = tuple(range(
                (v - 1) * self.num_vertices + 1,
                (v - 1) * self.num_vertices + self.num_vertices + 1
            ))
            sat.append(clause)
        return sat

    def _once_in_a_path(self):
        sat = []
        for v in range(1, self.num_vertices + 1):
            for pos1 in range(1, self.num_vertices):
                for pos2 in range(pos1 + 1, self.num_vertices + 1):
                    x1 = -(self.num_vertices*(v - 1) + pos1)
                    x2 = -(self.num_vertices*(v - 1) + pos2)
                    sat.append((x1, x2))
        return sat

    def _each_pos_by_some_vertex(self):
        sat = []
        for pos in range(1, self.num_vertices + 1):
            clause = tuple(range(pos, self.num_vertices**2 + 1, self.num_vertices))
            sat.append(clause)
        return sat

    def _no_two_vertices_same_pos(self):
        sat = []
        for pos in range(1, self.num_vertices + 1):
            for v1 in range(1, self.num_vertices):
                for v2 in range(v1 + 1, self.num_vertices + 1):
                    x1 = -(self.num_vertices*(v1 - 1) + pos)
                    x2 = -(self.num_vertices*(v2 - 1) + pos)
                    sat.append((x1, x2))
        return sat

    def _connected_by_an_edge(self):
        adj_list = defaultdict(set)
        for v1, v2 in self.edges:
            adj_list[v1].add(v2)
            adj_list[v2].add(v1)

        sat = []
        for v1 in range(1, self.num_vertices):
            for v2 in range(v1 + 1, self.num_vertices + 1):
                if v2 not in adj_list[v1]:
                    for pos in range(1, self.num_vertices):
                        # v1 to v2
                        x1 = -((v1 - 1)*self.num_vertices + pos)
                        x2 = -((v2 - 1)*self.num_vertices + (pos + 1) % (self.num_vertices + 1))
                        sat.append((x1, x2))

                        # v2 to v1
                        x1 = -((v2 - 1) * self.num_vertices + pos)
                        x2 = -((v1 - 1) * self.num_vertices + (pos + 1) % (self.num_vertices + 1))
                        sat.append((x1, x2))
        return sat

    def convert(self):
        sat = []
        sat.extend(self._belongs_to_a_path())
        sat.extend(self._once_in_a_path())
        sat.extend(self._each_pos_by_some_vertex())
        sat.extend(self._no_two_vertices_same_pos())
        sat.extend(self._connected_by_an_edge())
        return sat


def run_test():
    num_vertices, num_edges = 5, 4
    edges = [
        (1, 2),
        (2, 3),
        (5, 4),
        (3, 5),
    ]
    hp_to_sat = HamiltonianPathToSAT(num_vertices, edges)
    sat = hp_to_sat.convert()
    print(len(sat), num_vertices**2)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


def run_algo():
    num_vertices, num_edges = map(int, input().split())
    edges = [list(map(int, input().split())) for _ in range(num_edges)]
    hp_to_sat = HamiltonianPathToSAT(num_vertices, edges)
    sat = hp_to_sat.convert()
    print(len(sat), num_vertices**2)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


if __name__ == "__main__":
    # run_test()
    run_algo()
