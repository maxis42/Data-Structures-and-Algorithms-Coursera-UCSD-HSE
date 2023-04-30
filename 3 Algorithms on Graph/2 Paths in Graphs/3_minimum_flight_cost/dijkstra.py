# Uses python3
import sys
from collections import namedtuple
from typing import List


Test = namedtuple("Test", "n m edges start end ans")


class DijkstraPQElem:
    """
    Element in priority queue for Dijkstra algorithm.
    """
    def __init__(self, vertex, dist):
        self.vertex = vertex
        self.dist = dist


class DijkstraPQ:
    """
    Priority queue for Dijkstra algorithm.
    """
    def __init__(self):
        self.q = []
        self.empty = True
        self.num_elems = 0
        self.vertex_indices = dict()

    def insert(self, elem):
        self.q.append(elem)
        self.num_elems += 1
        self.empty = False
        self.vertex_indices[elem.vertex] = self.num_elems - 1
        self.sift_up(self.num_elems - 1)

    def pop_min(self):
        min_elem = None

        if self.num_elems > 0:
            if self.num_elems == 1:
                min_elem = self.q.pop()
            else:
                min_elem = self.q[0]
                last_elem = self.q.pop()
                self.q[0] = last_elem
                self.vertex_indices[last_elem.vertex] = 0

            self.num_elems -= 1
            if self.num_elems == 0:
                self.empty = True
            del self.vertex_indices[min_elem.vertex]

            self.sift_down(0)

        return min_elem

    def change_dist(self, vertex, new_dist):
        i = self.vertex_indices[vertex]

        cur_dist = self.q[i].dist
        self.q[i].dist = new_dist
        if new_dist >= cur_dist:
            self.sift_down(i)
        else:
            self.sift_up(i)

    def left_child_i(self, i):
        j = 2*i + 1
        if j >= self.num_elems:
            j = None
        return j

    def right_child_i(self, i):
        j = 2 * i + 2
        if j >= self.num_elems:
            j = None
        return j

    def left_child(self, i):
        j = self.left_child_i(i)
        if j is not None:
            return self.q[j]

    def right_child(self, i):
        j = self.right_child_i(i)
        if j is not None:
            return self.q[j]

    @staticmethod
    def parent_i(i):
        j = (i-1)//2
        if i == 0:
            j = None
        return j

    def sift_down(self, i):
        while True:
            lci = self.left_child_i(i)
            rci = self.right_child_i(i)

            if (lci is not None) and (rci is not None):
                # both children
                if self.q[lci].dist == self.q[i].dist == self.q[rci].dist:
                    # same dist elements
                    break
                elif (self.q[lci].dist <= self.q[i].dist) \
                        and (self.q[lci].dist <= self.q[rci].dist):
                    # q[lci] = min(q[lci], q[i], q[rci])
                    self.q[i], self.q[lci] = self.q[lci], self.q[i]
                    self.vertex_indices[self.q[i].vertex] = i
                    self.vertex_indices[self.q[lci].vertex] = lci
                    i = lci
                elif (self.q[rci].dist <= self.q[i].dist) \
                        and (self.q[rci].dist <= self.q[lci].dist):
                    # q[lci] = min(q[lci], q[i], q[rci])
                    self.q[i], self.q[rci] = self.q[rci], self.q[i]
                    self.vertex_indices[self.q[i].vertex] = i
                    self.vertex_indices[self.q[rci].vertex] = rci
                    i = rci
                else:
                    # q[lci] <= q[i] <= q[rci]
                    break
            elif lci is not None:
                # only left child
                if self.q[lci].dist < self.q[i].dist:
                    self.q[i], self.q[lci] = self.q[lci], self.q[i]
                    self.vertex_indices[self.q[i].vertex] = i
                    self.vertex_indices[self.q[lci].vertex] = lci
                    i = lci
                else:
                    break
            else:
                # no children
                break

    def sift_up(self, i):
        while True:
            if i == 0:
                # root element
                break

            pi = self.parent_i(i)
            if self.q[i].dist < self.q[pi].dist:
                self.q[i], self.q[pi] = self.q[pi], self.q[i]
                self.vertex_indices[self.q[i].vertex] = i
                self.vertex_indices[self.q[pi].vertex] = pi
                i = pi
            else:
                break


class Edge:
    def __init__(self, v_start, v_end, weight):
        self.v_start = v_start
        self.v_end = v_end
        self.weight = weight


class Graph:
    def __init__(self, num_vertices: int, num_edges: int, edges: List[Edge]):
        self.num_vertices = num_vertices
        self.num_edges = num_edges
        self.edges = edges

        self.adj_list = self.get_adj_list(self.num_vertices, self.edges)

    @staticmethod
    def get_adj_list(num_vertices: int, edges: List[Edge]) -> dict:
        adj_list = {i: [] for i in range(num_vertices)}
        for edge in edges:
            adj_list[edge.v_start].append((edge.v_end, edge.weight))
        return adj_list

    def min_dist_dijkstra(self, start, end):
        dist = [float("inf") for _ in range(self.num_vertices)]
        processed = [False for _ in range(self.num_vertices)]
        final = [False for _ in range(self.num_vertices)]

        q = DijkstraPQ()
        q.insert(DijkstraPQElem(start, 0))
        dist[start] = 0
        processed[start] = True

        while not q.empty:
            cur = q.pop_min()
            final[cur.vertex] = True

            if cur.vertex == end:
                break

            children = self.adj_list[cur.vertex]

            for child, weight in children:
                if not final[child]:
                    new_dist = dist[cur.vertex] + weight

                    if not processed[child]:
                        dist[child] = new_dist
                        q.insert(DijkstraPQElem(child, new_dist))
                        processed[child] = True
                    else:
                        cur_dist = dist[child]

                        if new_dist < cur_dist:
                            dist[child] = new_dist
                            q.change_dist(child, new_dist)

        if final[end]:
            min_dist = dist[end]
        else:
            min_dist = -1

        return min_dist


def run_algo():
    data = list(map(int, sys.stdin.read().split()))
    n, m = data[0:2]
    data = data[2:]
    edges_ = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    edges = []
    for ((a, b), w) in edges_:
        edges.append(Edge(a - 1, b - 1, w))
    start, end = data[0] - 1, data[1] - 1

    graph = Graph(n, m, edges)
    print(graph.min_dist_dijkstra(start, end))


def run_test():
    test = Test(
        n=4,
        m=4,
        edges=[
            Edge(1-1, 2-1, 1),
            Edge(4-1, 1-1, 2),
            Edge(2-1, 3-1, 2),
            Edge(1-1, 3-1, 5),
        ],
        start=1-1,
        end=3-1,
        ans=3,
    )
    test = Test(
        n=5,
        m=9,
        edges=[
            Edge(1 - 1, 2 - 1, 4),
            Edge(1 - 1, 3 - 1, 2),
            Edge(2 - 1, 3 - 1, 2),
            Edge(3 - 1, 2 - 1, 1),
            Edge(2 - 1, 4 - 1, 2),
            Edge(3 - 1, 5 - 1, 4),
            Edge(5 - 1, 4 - 1, 1),
            Edge(2 - 1, 5 - 1, 3),
            Edge(3 - 1, 4 - 1, 4),
        ],
        start=1 - 1,
        end=5 - 1,
        ans=6,
    )
    test = Test(
        n=3,
        m=3,
        edges=[
            Edge(1 - 1, 2 - 1, 7),
            Edge(1 - 1, 3 - 1, 5),
            Edge(2 - 1, 3 - 1, 2),
        ],
        start=3 - 1,
        end=2 - 1,
        ans=-1,
    )
    test = Test(
        n=1,
        m=0,
        edges=[
        ],
        start=1 - 1,
        end=1 - 1,
        ans=0,
    )
    test = Test(
        n=2,
        m=0,
        edges=[
        ],
        start=1 - 1,
        end=2 - 1,
        ans=-1,
    )
    graph = Graph(test.n, test.m, test.edges)
    min_dist = graph.min_dist_dijkstra(test.start, test.end)
    print(min_dist)
    assert min_dist == test.ans, f"Min dist: {min_dist}\nExpected: {test.ans}"


if __name__ == "__main__":
    # run_test()
    run_algo()
