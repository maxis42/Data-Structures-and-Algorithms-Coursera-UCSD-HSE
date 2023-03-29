# Uses python3


def distance_matrix(a, b):
    n = len(a)
    m = len(b)

    # array of distances (n+1 x m+1 x s+1)
    D = []
    for i in range(n+1):
        row = []
        for j in range(m+1):
            row.append(0)
        D.append(row)

    # array of directions
    directions = []
    for i in range(n):
        row = []
        for j in range(m):
            row.append('')
        directions.append(row)

    # initialize zero row and column
    for i in range(n+1):
        D[i][0] = i
    for j in range(m+1):
        D[0][j] = j

    for i in range(1, n+1):
        for j in range(1, m+1):
            # check whether there is a match
            if a[i-1] == b[j-1]:
                directions[i-1][j-1] = 'ADDXY'
                D[i][j] = D[i-1][j-1]
            else:
                # space to the 1st word
                ins1 = D[i][j-1] + 1
                # space to the 2nd word
                ins2 = D[i-1][j] + 1

                ind_arr = range(1, 3)
                ins_arr = [ins1, ins2]
                sorted_arr = sorted(zip(ind_arr, ins_arr), key=lambda x: x[1])
                min_ind, min_ins = sorted_arr[0]
                D[i][j] = min_ins
                directions[i-1][j-1] = ''.join(['INS', str(min_ind)])

            print(i, j)
            for row in D:
                print(row)
            print()

    for row in directions:
        print(row)

    return directions


def output_alignment(directions):
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


def lcs2(a, b):
    directions = distance_matrix(a, b)
    return output_alignment(directions)


if __name__ == '__main__':
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))

    print(lcs2(a, b))
