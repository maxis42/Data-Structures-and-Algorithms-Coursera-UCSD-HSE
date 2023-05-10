# python3

class GraphColoringToSAT:
    def __init__(self, num_vertices, edges):
        self.num_vertices = num_vertices
        self.edges = edges

    @staticmethod
    def _convert_vertex_to_sat(v):
        v_last_id = v * 3
        v_ids = (v_last_id - 2, v_last_id - 1, v_last_id)

        sat_vertex = [
            # exactly one color for the first vertex
            (v_ids[0], v_ids[1], v_ids[2]),
            (-v_ids[0], -v_ids[1]),
            (-v_ids[0], -v_ids[2]),
            (-v_ids[1], -v_ids[2]),
        ]
        return sat_vertex

    @staticmethod
    def _convert_edge_to_sat(v1, v2):
        v1_last_id = v1 * 3
        v1_ids = (v1_last_id - 2, v1_last_id - 1, v1_last_id)

        v2_last_id = v2 * 3
        v2_ids = (v2_last_id - 2, v2_last_id - 1, v2_last_id)

        sat_edge = [
            # different colors on edge ends
            (-v1_ids[0], -v2_ids[0]),
            (-v1_ids[1], -v2_ids[1]),
            (-v1_ids[2], -v2_ids[2]),
        ]
        return sat_edge

    def convert(self):
        sat = []

        for i in range(self.num_vertices):
            sat.extend(self._convert_vertex_to_sat(i + 1))

        for v1, v2 in self.edges:
            sat.extend(self._convert_edge_to_sat(v1, v2))
        return sat


def run_test():
    num_vertices, num_edges = 3, 3
    edges = [
        (1, 2),
        (2, 3),
        (1, 3),
    ]
    gc_to_sat = GraphColoringToSAT(num_vertices, edges)
    sat = gc_to_sat.convert()
    print(len(sat), num_vertices * 3)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


def run_algo():
    num_vertices, num_edges = map(int, input().split())
    edges = [list(map(int, input().split())) for i in range(num_edges)]
    gc_to_sat = GraphColoringToSAT(num_vertices, edges)
    sat = gc_to_sat.convert()
    print(len(sat), num_vertices*3)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


if __name__ == "__main__":
    # run_test()
    run_algo()
