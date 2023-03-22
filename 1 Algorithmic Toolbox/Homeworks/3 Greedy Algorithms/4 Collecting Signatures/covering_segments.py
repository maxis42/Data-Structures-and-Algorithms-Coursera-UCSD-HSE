# Uses python3
from collections import namedtuple

Segment = namedtuple('Segment', ['start', 'end'])


def optimal_points(segments):
    segments_sorted = sorted(segments, key=lambda x: x.start)

    x = segments_sorted[0].end
    points = []

    for s in segments_sorted:
        if s.start > x:
            points.append(x)
            x = s.end
        else:
            x = min(x, s.end)
    points.append(x)
    return points


if __name__ == '__main__':
    n = int(input())
    segments = []
    for _ in range(n):
        a, b = map(int, input().split())
        segments.append(Segment(a, b))

    points = optimal_points(segments)

    print(len(points))
    for p in points:
        print(p, end=' ')
