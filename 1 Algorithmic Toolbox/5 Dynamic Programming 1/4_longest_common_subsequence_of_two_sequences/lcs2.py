# Uses python3


def distance_matrix(A, B):
    n = len(A)
    m = len(B)

    # array of distances (n+1 x m+1)
    D = [[0] * (m+1) for i in range(n+1)]

    # array of directions
    directions = [[''] * m for i in range(n)]

    # initialize zero row and column
    for i in range(n+1):
        D[i][0] = i
    for j in range(m+1):
        D[0][j] = j

    for j in range(1, m+1):
        for i in range(1, n+1):
            # check whether there is a match
            if A[i-1] == B[j-1]:
                directions[i-1][j-1] = 'ADDXY'
                D[i][j] = D[i-1][j-1]
            else:
                # space to the 1st word
                insertion = D[i][j-1] + 1
                # space to the 2nd word
                deletion = D[i-1][j] + 1

                if insertion < deletion:
                    D[i][j] = insertion
                    directions[i-1][j-1] = 'INS'
                else:
                    D[i][j] = deletion
                    directions[i-1][j-1] = 'DEL'
    return directions


def lcs2(a, b):
    directions = distance_matrix(a, b)
    return output_alignment(directions)


def output_alignment(directions):
    i = len(directions)
    j = len(directions[0])
    cnt = 0
    while i != 0 and j != 0:
        if directions[i-1][j-1] == 'ADDXY':
            i -= 1
            j -= 1
            cnt += 1
        elif directions[i-1][j-1] == 'INS':
            j -= 1
        elif directions[i-1][j-1] == 'DEL':
            i -= 1
    return cnt


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))

    print(lcs2(a, b))
