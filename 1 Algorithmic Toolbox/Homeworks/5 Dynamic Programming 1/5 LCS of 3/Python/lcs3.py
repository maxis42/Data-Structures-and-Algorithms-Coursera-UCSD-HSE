# Uses python3

import sys


def distance_matrix(a, b, c):
    n = len(a)
    m = len(b)
    s = len(c)

    # array of distances (n+1 x m+1 x s+1)
    D = []
    for i in range(n+1):
        matrix = []
        for j in range(m+1):
            row = []
            for k in range(s+1):
                row.append(0)
            matrix.append(row)
        D.append(matrix)

    # array of directions
    directions = []
    for i in range(n):
        matrix = []
        for j in range(m):
            row = []
            for k in range(s):
                row.append('')
            matrix.append(row)
        directions.append(matrix)

    # initialize zero row and column
    for i in range(n+1):
        D[i][0][0] = i
    for j in range(m+1):
        D[0][j][0] = j
    for k in range(s+1):
        D[0][0][k] = k

    # i - matrix
    # j - row
    # k - column
    # print("D start")
    # for matrix in D:
    #     for row in matrix:
    #         print(row)
    #     print()
    # print("D end")

    for i in range(1, n+1):
        for j in range(1, m+1):
            for k in range(1, s+1):
                # check whether there is a match
                if a[i-1] == b[j-1] == c[k-1]:
                    directions[i-1][j-1][k-1] = 'ADDXYZ'
                    D[i][j][k] = D[i-1][j-1][k-1]
                else:
                    # space to the 1st word
                    ins1 = D[i-1][j][k] + 1
                    # space to the 2nd word
                    ins2 = D[i][j-1][k] + 1
                    # space to the 3rd word
                    ins3 = D[i][j][k-1] + 1

                    ind_arr = range(1, 4)
                    ins_arr = [ins1, ins2, ins3]
                    sorted_arr = sorted(zip(ind_arr, ins_arr),
                                        key=lambda x: x[1])
                    min_ind, min_ins = sorted_arr[0]
                    D[i][j][k] = min_ins
                    directions[i-1][j-1][k-1] = ''.join(['INS', str(min_ind)])

                print(i, j, k)
                # print(D[i])
                # print(D[i][j])
                # print(D[i][j][k])
                print("D start")
                for matrix in D:
                    for row in matrix:
                        print(row)
                    print()
                print("D end")

    print("Directions start")
    for matrix in directions:
        for row in matrix:
            print(row)
        print()
    print("Directions end")

    return directions


def output_alignment(directions):
    i = len(directions)
    j = len(directions[0])
    k = len(directions[0][0])
    cnt = 0
    print("start output")
    print(i, j, k)
    print(directions)
    while i != 0 and j != 0 and k != 0:
        if directions[i-1][j-1][k-1] == 'ADDXYZ':
            print('ADDXYZ', i, j, k)
            i -= 1
            j -= 1
            k -= 1
            cnt += 1
        elif directions[i-1][j-1][k-1] == 'INS1':
            print('INS1', i, j, k)
            # i -= 1
            j -= 1
            k -= 1
        elif directions[i-1][j-1][k-1] == 'INS2':
            print('INS2', i, j, k)
            i -= 1
            # j -= 1
            k -= 1
        elif directions[i-1][j-1][k-1] == 'INS3':
            print('INS3', i, j, k)
            i -= 1
            j -= 1
            # k -= 1
    return cnt


def lcs3(a, b, c):
    directions = distance_matrix(a, b, c)
    return output_alignment(directions)


if __name__ == '__main__':
    # input = sys.stdin.read()
    # data = list(map(int, input.split()))
    # an = data[0]
    # data = data[1:]
    # a = data[:an]
    # data = data[an:]
    # bn = data[0]
    # data = data[1:]
    # b = data[:bn]
    # data = data[bn:]
    # cn = data[0]
    # data = data[1:]
    # c = data[:cn]

    # a = [1, 2, 3]
    # b = [2, 1, 3]
    # c = [1, 3, 5]

    # a = [8, 3, 2, 1, 7]
    # b = [8, 2, 1, 3, 8, 10, 7]
    # c = [6, 8, 3, 1, 4, 7]
    #
    # a = [1, 2, 3]
    # b = [2, 1, 3]
    # c = [1, 3, 5]

    # a = [2, 7, 5]
    # b = [2, 5]
    #
    # a = [7]
    # b = [1, 2, 3, 4]

    a = [2, 7, 8, 3]
    b = [5, 2, 8, 7]
    # a = [1, 2]
    # b = [1]
    # c = [1]
    c = a.copy()

    print(lcs3(a, b, c))
