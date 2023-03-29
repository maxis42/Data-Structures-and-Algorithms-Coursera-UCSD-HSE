

def lcs3(a, b, c):
    m = len(a)
    n = len(b)
    o = len(c)
    L = [[[0 for k in range(o+1)] for j in range(n+1)] for i in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            for k in range(1, o+1):
                if a[i-1] == b[j-1] and a[i-1] == c[k-1]:
                    L[i][j][k] = L[i-1][j-1][k-1] + 1
                else:
                    L[i][j][k] = max(L[i-1][j][k], L[i][j-1][k], L[i][j][k-1])
    return L[m][n][o]


if __name__ == "__main__":
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    b = list(map(int, input().split()))
    l = int(input())
    c = list(map(int, input().split()))
    print(lcs3(a, b, c))
