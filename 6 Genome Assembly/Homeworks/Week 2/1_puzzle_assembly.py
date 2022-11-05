# python 3
from math import sqrt
from itertools import permutations


class PuzzleAssembly:
    def __init__(self, squares):
        # tuple (up, left, down, right)
        self.squares = squares

        self._color_to_id, self._id_to_color = self._get_color_maps(self.squares)
        self._squares = self._get_inner_squares(self.squares, self._color_to_id)

    @staticmethod
    def _get_color_maps(squares):
        color_to_id = dict()
        id_to_color = []

        # border color is black
        color_to_id["black"] = 0
        id_to_color.append("black")

        i = 1
        for square in squares:
            for color in square:
                if color not in color_to_id:
                    color_to_id[color] = i
                    id_to_color.append(color)
                    i += 1
        return color_to_id, id_to_color

    @staticmethod
    def _get_inner_squares(squares, color_to_id):
        squares_inner = []
        for square in squares:
            square_inner = tuple(color_to_id[color] for color in square)
            squares_inner.append(square_inner)
        squares_inner = tuple(squares_inner)
        return squares_inner

    @classmethod
    def read_input(cls, n_squares):
        squares = []
        for _ in range(n_squares):
            # ex. "(red,green,blue,black)"
            square = input().strip()
            square = square[1:-1]
            square = tuple(square.split(","))
            squares.append(square)
        squares = tuple(squares)
        return cls(squares)

    @staticmethod
    def print_result(squares):
        for row in squares:
            row_ss = []
            for square in row:
                row_ss.append("(" + ",".join(square) + ")")
            row_s = ";".join(row_ss)
            print(row_s)

    def solve(self):
        n = int(sqrt(len(self._squares)))
        pos = [[-1] * n for _ in range(n)]
        up_inner_border = []
        left_inner_border = []
        down_inner_border = []
        right_inner_border = []
        inner_squares = []
        for i, (c_u, c_l, c_d, c_r) in enumerate(self._squares):
            # find corner squares positions
            if c_u == c_l == 0:
                pos[0][0] = i
                continue
            elif c_u == c_r == 0:
                pos[0][n - 1] = i
                continue
            elif c_l == c_d == 0:
                pos[n - 1][0] = i
                continue
            elif c_d == c_r == 0:
                pos[n - 1][n - 1] = i
                continue

            # find inner border candidates
            if (c_u == 0) and (c_l != 0) and (c_r != 0):
                up_inner_border.append(i)
                continue
            elif (c_l == 0) and (c_u != 0) and (c_d != 0):
                left_inner_border.append(i)
                continue
            elif (c_d == 0) and (c_l != 0) and (c_r != 0):
                down_inner_border.append(i)
                continue
            elif (c_r == 0) and (c_d != 0) and (c_u != 0):
                right_inner_border.append(i)
                continue

            # inner squares
            inner_squares.append(i)

        pos = self._find_permutation(
            pos,
            up_inner_border,
            left_inner_border,
            down_inner_border,
            right_inner_border,
            inner_squares
        )

        # convert inner IDs back to colors
        pos_col = [[""] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                square_id = pos[i][j]
                pos_col[i][j] = self.squares[square_id]
        return pos_col

    def _find_permutation(self, pos, up_inner_border, left_inner_border,
                         down_inner_border, right_inner_border, inner_squares):
        n = len(up_inner_border) + 2
        n_inn = len(up_inner_border)

        # iterate over all border positions
        # n = 25 -> 6 possible placing * 4 borders = 24 positions
        # if violate corners -> skip to next=
        for u_b in permutations(up_inner_border):
            for i, square in enumerate(u_b):
                pos[0][i + 1] = square

            correct = True
            for i in range(1, n):
                prev_right_col = self._squares[pos[0][i - 1]][3]
                cur_left_col = self._squares[pos[0][i]][1]
                if prev_right_col != cur_left_col:
                    correct = False
                    break
            if not correct:
                continue

            for l_b in permutations(left_inner_border):
                for i, square in enumerate(l_b):
                    pos[i + 1][0] = square

                correct = True
                for i in range(1, n):
                    prev_down_col = self._squares[pos[i - 1][0]][2]
                    cur_up_col = self._squares[pos[i][0]][0]
                    if prev_down_col != cur_up_col:
                        correct = False
                        break
                if not correct:
                    continue

                for d_b in permutations(down_inner_border):
                    for i, square in enumerate(d_b):
                        pos[n - 1][i + 1] = square

                    correct = True
                    for i in range(1, n):
                        prev_right_col = self._squares[pos[n - 1][i - 1]][3]
                        cur_left_col = self._squares[pos[n - 1][i]][1]
                        if prev_right_col != cur_left_col:
                            correct = False
                            break
                    if not correct:
                        continue

                    for r_b in permutations(right_inner_border):
                        for i, square in enumerate(r_b):
                            pos[i + 1][n - 1] = square

                        correct = True
                        for i in range(1, n):
                            prev_down_col = self._squares[pos[i - 1][n - 1]][2]
                            cur_up_col = self._squares[pos[i][n - 1]][0]
                            if prev_down_col != cur_up_col:
                                correct = False
                                break
                        if not correct:
                            continue

                        # iterate over all inner squares positions
                        # n = 25 -> 9 inner squares -> 9! = 362,880 positions
                        for inner in permutations(inner_squares):
                            for k, square in enumerate(inner):
                                i = k // n_inn
                                j = k % n_inn
                                pos[i + 1][j + 1] = square

                            correct = True
                            for i in range(1, n):
                                for j in range(1, n):
                                    prev_right_col = self._squares[pos[i][j - 1]][3]
                                    cur_left_col = self._squares[pos[i][j]][1]

                                    if prev_right_col != cur_left_col:
                                        correct = False
                                        break

                                    prev_bot_col = self._squares[pos[i - 1][j]][2]
                                    cur_up_col = self._squares[pos[i][j]][0]

                                    if prev_bot_col != cur_up_col:
                                        correct = False
                                        break

                                if not correct:
                                    break

                            if correct:
                                return pos
        return None


def run_test():
    n_squares = 9
    squares = (
        ("yellow", "black", "black", "blue"),
        ("blue", "blue", "black", "yellow"),
        ("orange", "yellow", "black", "black"),
        ("red", "black", "yellow", "green"),
        ("orange", "green", "blue", "blue"),
        ("green", "blue", "orange", "black"),
        ("black", "black", "red", "red"),
        ("black", "red", "orange", "purple"),
        ("black", "purple", "green", "black"),
    )
    pa = PuzzleAssembly(squares)
    res = pa.solve()
    pa.print_result(res)


def run_algo():
    n_squares = 25
    pa = PuzzleAssembly.read_input(n_squares)
    res = pa.solve()
    pa.print_result(res)


if __name__ == "__main__":
    # run_test()
    run_algo()
