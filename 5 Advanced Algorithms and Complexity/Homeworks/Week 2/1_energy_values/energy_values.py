# python3
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
                return "Multiple solutions!"

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

    def print(self):
        print("Matrix:")
        for row in self.matrix:
            print(row)
        print()


def run_test():
    matrix = [
        [5, -5, -1],
        [-1, -2, -1],
    ]

    gm = GaussMethod(matrix)
    res = gm.solve()
    print(" ".join(map(lambda x: str(round(x, 4)), res)))


def run_algo():
    size = int(input())
    matrix = []
    for _ in range(size):
        row = list(map(float, input().split()))
        matrix.append(row)

    gm = GaussMethod(matrix)
    res = gm.solve()
    print(" ".join(map(lambda x: str(round(x, 4)), res)))


if __name__ == "__main__":
    run_test()
    # run_algo()
