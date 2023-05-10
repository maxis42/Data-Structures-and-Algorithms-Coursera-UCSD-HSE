# python3
from itertools import combinations


class GaussMethod:
    def __init__(self, matrix):
        self.matrix = matrix
        self.n = len(self.matrix)

    def solve(self):
        # forward pass
        for i in range(self.n):
            # find row with the first nonzero column in i-th position
            for k in range(i, self.n):
                if self.matrix[k][i] != 0:
                    cur = k
                    break
            else:
                return []

            # swap rows
            if cur != i:
                self.matrix[i], self.matrix[cur] = self.matrix[cur], self.matrix[i]

            # make the first coefficient equals to 1
            coeff = self.matrix[i][i]
            for j in range(i, self.n + 1):
                self.matrix[i][j] /= coeff

            # subtract current row from the next rows in order to
            # eliminate dependence from current variable
            for k in range(i + 1, self.n):
                coeff = self.matrix[k][i]
                for j in range(i, self.n + 1):
                    self.matrix[k][j] -= coeff * self.matrix[i][j]

        # backward pass
        for i in range(self.n - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                coeff = self.matrix[j][i]
                self.matrix[j][i] -= coeff * self.matrix[i][i]
                self.matrix[j][self.n] -= coeff * self.matrix[i][self.n]

        res = [self.matrix[i][-1] for i in range(self.n)]
        return res


class DietProblem:
    """
    Maximize pleasure from diet bounded by the specified restrictions.
    """

    INF = 10**9

    def __init__(self, n, m, A, b, c):
        # the number of restrictions on your diet
        self.n = n
        self._n = self.n + 1  # add equation to tackle infinity problem (see the assignment)
        # the number of all available dishes and drinks
        self.m = m
        # coefficients of linear inequalities
        # Ax <= b, where A (nxm), x (m), b (n)
        self.A = A
        self._A = self.A.copy()
        self._A.append([1 for _ in range(self.m)])
        self.b = b
        self._b = self.b.copy()
        self._b.append(self.INF)
        # the pleasure for consuming one item of each dish and drink
        # c (m)
        self.c = c

    def solve(self):
        eq_combs = combinations(range(self._n + self.m), self.m)

        results = []
        for equations in eq_combs:
            matrix = []
            inf_equation = False
            for i in equations:
                if i < self._n:
                    row = list(self._A[i])
                    row.append(self._b[i])
                else:
                    row = [0 for _ in range(self.m + 1)]
                    row[i - self._n] = 1
                matrix.append(row)

                if i == self.n:
                    inf_equation = True

            gm = GaussMethod(matrix)
            solution = gm.solve()
            if not solution:
                continue

            # check if at least one of the inequalities is violated
            violated = False
            i = 0
            while not violated and (i < self.n):
                res = sum(map(lambda x: x[0] * x[1], zip(self._A[i], solution)))
                if round(res, 2) > self._b[i]:
                    violated = True
                i += 1
            i = 0
            while not violated and (i < self.m):
                if round(solution[i], 2) < 0:
                    violated = True
                i += 1

            if not violated:
                results.append((solution, inf_equation))

        if not results:
            ans = "No solution"
        else:
            max_result = None
            max_amount = -self.INF
            inf_max_res = False
            for res, inf_equation in results:
                amount = sum(map(lambda x: x[0] * x[1], zip(res, self.c)))
                amount = round(amount, 2)
                if amount > max_amount:
                    max_amount = amount
                    max_result = res
                    if inf_equation:
                        inf_max_res = True
                    else:
                        inf_max_res = False

                if (amount == max_amount) and not inf_equation:
                    max_result = res
                    inf_max_res = False

            if inf_max_res:
                ans = "Infinity"
            else:
                ans = "Bounded solution\n"
                ans += " ".join(list(map(lambda x: "%.18f" % x, max_result)))
        return ans


def run_test():
    n, m = 3, 2
    A = [
        [-1, -1],
        [1, 0],
        [0, 1],
    ]
    b = [-1, 2, 2]
    c = [-1, 2]

    n, m = 2, 2
    A = [
        [1, 1],
        [-1, -1],
    ]
    b = [1, -2]
    c = [1, 1]

    n, m = 1, 3
    A = [
        [0, 0, 1],
    ]
    b = [3]
    c = [1, 1, 1]

    n, m = 1, 1
    A = [
        [30],
    ]
    b = [1680]
    c = [-87]

    n, m = 1, 2
    A = [
        [-29, -93],
    ]
    b = [15149]
    c = [-50, 0]

    n, m = 3, 2
    A = [
        [-66, 37],
        [-77, -87],
        [-73, 1],
    ]
    b = [18658, -15935, 3750]
    c = [-35, 61]

    n, m = 3, 4
    A = [
        [95, 40, 93, 79],
        [-65, 92, 43, 19],
        [-34, 74, 32, -50],
    ]
    b = [6681, 2755, 1974]
    c = [-63, 20, -32, -42]

    n, m = 3, 3
    A = [
        [-46, -46, 14],
        [38, -14, -30],
        [23, 100, -86],
    ]
    b = [-14867, -7071, -10179]
    c = [100, -30, -80]
    dp = DietProblem(n, m, A, b, c)
    ans = dp.solve()
    print(ans)


def run_algo():
    n, m = list(map(int, input().split()))
    A = []
    for i in range(n):
        A += [list(map(int, input().split()))]
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    dp = DietProblem(n, m, A, b, c)
    ans = dp.solve()
    print(ans)


if __name__ == "__main__":
    # run_test()
    run_algo()
