# Uses python3
import sys


# complexity n*log(n), where n = p + 2*s
def fast_count_segments(starts, ends, points):
    cnt = [0] * len(points)
    points_num = [i for _, i in sorted(zip(points, range(len(points))))]

    # order for points with the same value:
    # starts, points, ends
    # (value, point type)
    # 0 - starts; 1 - points; 2 - ends
    full_points = [(p, 1) for p in points]
    full_points.extend([(s, 0) for s in starts])
    full_points.extend([(e, 2) for e in ends])

    full_points.sort()

    num_open_segments = 0
    i = 0
    for val, p_type in full_points:
        if p_type == 0:
            num_open_segments += 1
        elif p_type == 2:
            num_open_segments -= 1
        else:
            cnt[points_num[i]] = num_open_segments
            i += 1
    return cnt


def naive_count_segments(starts, ends, points):
    cnt = [0] * len(points)
    for i in range(len(points)):
        for j in range(len(starts)):
            if starts[j] <= points[i] <= ends[j]:
                cnt[i] += 1
    return cnt


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]
    m = data[1]
    starts = data[2:2 * n + 2:2]
    ends = data[3:2 * n + 2:2]
    points = data[2 * n + 2:]
    # use fast_count_segments
    cnt = fast_count_segments(starts, ends, points)
    for x in cnt:
        print(x, end=' ')
