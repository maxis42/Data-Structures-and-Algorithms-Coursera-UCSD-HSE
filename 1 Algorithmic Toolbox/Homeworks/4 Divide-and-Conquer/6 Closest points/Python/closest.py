# Uses python3
import sys
from math import sqrt


def min_dist_sort(x, y):
    points = list(zip(x, y))
    points_x = sorted(points, key=lambda x: x)
    points_y = sorted(points, key=lambda y: x[1])
    return sqrt(minimum_distance(points_x, points_y))


def minimum_distance(points_x, points_y):
    if len(points_x) == 1:
        return 10**18

    mid = len(points_x) // 2

    d1 = minimum_distance(points_x[:mid], points_y)
    d2 = minimum_distance(points_x[mid:], points_y)
    d12 = min(d1, d2)

    points_mid_y = [p for p in points_y if p in points_x and abs(points_x[mid][0] - p[0]) < d12]
    dmid = check_middle_line(points_mid_y)

    return min(d12, dmid)


def check_middle_line(points):
    min_dist = 10**18
    N = len(points)
    for i in range(N-1):
        p1 = points[i]
        for j in range(i+1, min(i+9, N)):
            p2 = points[j]
            dist = (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

            if dist < min_dist:
                min_dist = dist
    return min_dist


def minimum_distance_naive(x, y):
    points = list(zip(x, y))

    min_dist = 10**18

    for i in range(len(points)-1):
        p1 = points[i]
        for j in range(i+1, len(points)):
            p2 = points[j]
            dist = sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

            if dist < min_dist:
                min_dist = dist
    return min_dist


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    x = data[1::2]
    y = data[2::2]
    print("{0:.9f}".format(min_dist_sort(x, y)))
