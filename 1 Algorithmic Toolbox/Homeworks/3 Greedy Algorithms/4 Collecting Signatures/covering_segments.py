# Uses python3
import sys
from collections import namedtuple

Segment = namedtuple('Segment', ['start', 'end'])


def optimal_points(segments):
    segments_sorted = sorted(segments, key=lambda x: x.start)

    start = segments_sorted[0].start
    end = segments_sorted[0].end

    points = []

    for s in segments_sorted:
        if s.start <= end:
            start = s.start
        else:
            points.append(start)
            end = s.end
    points.append(start)
    return points


if __name__ == '__main__':
    input = sys.stdin.read()

    n, *data = map(int, input.split())
    segments = list(map(lambda x: Segment(x[0], x[1]), zip(data[::2], data[1::2])))

    points = optimal_points(segments)

    print(len(points))
    for p in points:
        print(p, end=' ')
