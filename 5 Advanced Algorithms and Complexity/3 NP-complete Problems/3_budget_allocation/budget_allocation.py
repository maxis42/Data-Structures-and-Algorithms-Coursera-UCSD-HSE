# python3
from itertools import starmap
from operator import mul


class IntegerLinearProgrammingToSAT:
    """
    It is guaranteed that there will be AT MOST 3
    different variables with non-zero coefficients
    in each inequality of this Integer Linear
    Programming problem.
    """
    sol1 = (
        (0,),
        (1,),
    )
    sol2 = (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    )
    sol3 = (
        (0, 0, 0),
        (0, 0, 1),
        (0, 1, 0),
        (0, 1, 1),
        (1, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (1, 1, 1),
    )

    def __init__(self, A, b):
        # Ax <= b
        self.A = A
        self.b = b

    def _inequality_to_sat(self, row, value):
        nonzero_ids, nonzero_elems = [], []
        for i, a in enumerate(row):
            if a != 0:
                nonzero_ids.append(i + 1)
                nonzero_elems.append(a)
                if len(nonzero_elems) == 3:
                    # at most 3 non-zero coefficients
                    break

        num_nonzero_elems = len(nonzero_elems)

        sat = []
        if num_nonzero_elems == 0:
            return sat

        if num_nonzero_elems == 1:
            sol = self.sol1
        elif num_nonzero_elems == 2:
            sol = self.sol2
        else:
            # at most 3 non-zero coefficients
            sol = self.sol3

        for s in sol:
            res = sum(starmap(mul, zip(nonzero_elems, s)))
            if res > value:
                signs = [1 if x == 0 else -1 for x in s]
                clause = tuple(starmap(mul, zip(signs, nonzero_ids)))
                sat.append(clause)
        return sat

    def convert(self):
        sat = []
        for i in range(len(self.A)):
            row = self.A[i]
            value = self.b[i]
            sat_row = self._inequality_to_sat(row, value)
            if sat_row:
                sat.extend(sat_row)

        if not sat:
            # if no invalidate inequalities than add
            # always satisfiable formula
            sat.append((1, -1))
        return sat


def run_test():
    num_inequalities, num_variables = 2, 3
    A = [
        (5, 2, 3),
        (-1, -1, -1),
    ]
    b = [6, -2]
    ilp_to_sat = IntegerLinearProgrammingToSAT(A, b)
    sat = ilp_to_sat.convert()
    print(len(sat), num_variables)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


def run_algo():
    num_inequalities, num_variables = list(map(int, input().split()))
    # Ax <= b
    A = []  # num_inequalities X num_variables
    for _ in range(num_inequalities):
        A += [list(map(int, input().split()))]
    b = list(map(int, input().split()))  # num_inequalities

    ilp_to_sat = IntegerLinearProgrammingToSAT(A, b)
    sat = ilp_to_sat.convert()

    print(len(sat), num_variables)
    for clause in sat:
        s = " ".join(map(str, clause))
        s += " 0"
        print(s)


if __name__ == "__main__":
    # run_test()
    run_algo()
