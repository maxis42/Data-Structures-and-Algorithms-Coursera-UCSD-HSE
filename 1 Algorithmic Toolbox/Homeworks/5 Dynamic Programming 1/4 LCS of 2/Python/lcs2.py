# Uses python3

import sys


def distance_matrix(A, B):
    n = len(A)
    m = len(B)

    # array of distances (n+1 x m+1)
    D = [[0] * (m+1) for i in range(n+1)]

    # initialize zero row and column
    for i in range(n+1):
        D[i][0] = i
    for j in range(m+1):
        D[0][j] = j

    for j in range(1, m+1):
        for i in range(1, n+1):
            # space to the 1st word
            insertion = D[i][j-1] + 1
            # space to the 2nd word
            deletion = D[i-1][j] + 1
            # letters match
            match = D[i-1][j-1]
            # letters mismatch
            mismatch = D[i-1][j-1] + 1

            # check whether there is a match
            if A[i-1] == B[j-1]:
                D[i][j] = min(insertion, deletion, match)
            else:
                D[i][j] = min(insertion, deletion, mismatch)

    return D


def lcs2(a, b):
    D = distance_matrix(a, b)
    return output_alignment(len(a), len(b), D)


def output_alignment(i, j, D):
    if i == 0 and j == 0:
        return 0

    # deletion
    if i > 0 and D[i][j] == D[i-1][j] + 1:
        n = output_alignment(i-1, j, D)
    # insertion
    elif j > 0 and D[i][j] == D[i][j-1] + 1:
        n = output_alignment(i, j-1, D)
    # match/mismatch
    else:
        n = output_alignment(i-1, j-1, D)
        if D[i][j] == D[i-1][j-1]:
            n += 1
    return n


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))

    n = data[0]
    data = data[1:]
    a = data[:n]

    data = data[n:]
    m = data[0]
    data = data[1:]
    b = data[:m]

    print(lcs2(a, b))
