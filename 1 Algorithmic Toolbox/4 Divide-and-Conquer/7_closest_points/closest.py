# Uses python3
import sys
from math import sqrt


def min_dist_sort(x, y):
    points = list(zip(x, y))
    points = sorted(points, key=lambda p: p[0])
    return sqrt(minimum_distance(points))


def minimum_distance(points):
    N = len(points)
    if N <= 3:
        x, y = [list(t) for t in zip(*points)]
        return minimum_distance_bruteforce_wo_sqrt(x, y)

    mid = N // 2

    d1 = minimum_distance(points[:mid])
    d2 = minimum_distance(points[mid:])
    d12 = min(d1, d2)

    points_mid = [p for p in points if abs(points[mid][0] - p[0]) < d12]
    d = check_middle_line(points_mid, d12)

    return d


def check_middle_line(points, d):
    min_dist = d
    N = len(points)
    points = sorted(points, key=lambda x: x[1])
    for i in range(N-1):
        p1 = points[i]
        for j in range(i+1, min(i+9, N)):
            p2 = points[j]
            dist = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

            if dist < min_dist:
                min_dist = dist
    return min_dist


def minimum_distance_bruteforce_wo_sqrt(x, y):
    points = list(zip(x, y))

    min_dist = 10**18

    for i in range(len(points)-1):
        p1 = points[i]
        for j in range(i+1, len(points)):
            p2 = points[j]
            dist = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

            if dist < min_dist:
                min_dist = dist
    return min_dist


if __name__ == '__main__':
    n = int(input())
    x, y = [], []
    for _ in range(n):
        x_i, y_i = map(int, input().split())
        x.append(x_i)
        y.append(y_i)
    print("{0:.9f}".format(min_dist_sort(x, y)))
