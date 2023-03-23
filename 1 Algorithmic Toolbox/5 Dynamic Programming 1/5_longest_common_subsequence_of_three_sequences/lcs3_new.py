def edit_distance_3d(A, B, C):
    l = len(A)
    m = len(B)
    n = len(C)
    print(l, m, n)

    # tensor of distances (l+1 x m+1 x n+1)
    D = [[[0] * (n + 1) for i in range(m + 1)] for j in range(l + 1)]
    print(len(D), len(D[0]), len(D[0][0]))

    # initialize zero row and column
    for i in range(l + 1):
        D[i][0][0] = i
    for j in range(m + 1):
        D[0][j][0] = j
    for k in range(n + 1):
        D[0][0][k] = k
    print(D)

    for i in range(1, l + 1):
        for j in range(1, m + 1):
            for k in range(1, n+1):
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

    return D[n][m]


def edit_distance_2d(A, B):
    m = len(A)
    n = len(B)

    # matrix of distances (m+1 x n+1)
    D = [[0] * (n + 1) for i in range(m + 1)]

    # initialize zero row and column
    for i in range(m + 1):
        D[i][0] = i
    for j in range(n + 1):
        D[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n+1):
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
    print(D)
    return D


def count_alignment_matches(directions):
    i = len(directions)
    j = len(directions[0])
    cnt = 0
    while i != 0 and j != 0:
        if directions[i-1][j-1] == 'ADDXY':
            i -= 1
            j -= 1
            cnt += 1
        elif directions[i-1][j-1] == 'INS2':
            i -= 1
        elif directions[i-1][j-1] == 'INS1':
            j -= 1
    return cnt


if __name__ == "__main__":
    # print(edit_distance_tensor(input(), input()))
    # edit_distance_2d("ab", "kad")
    edit_distance_2d([2, 7, 8, 3], [5, 2, 8, 7])
    # edit_distance_3d("ab", "kad", "bums")
