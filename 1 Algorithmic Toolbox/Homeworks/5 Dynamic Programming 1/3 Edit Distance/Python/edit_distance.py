# Uses python3
def edit_distance(A, B):
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

    return D[n][m]


if __name__ == "__main__":
    print(edit_distance(input(), input()))
