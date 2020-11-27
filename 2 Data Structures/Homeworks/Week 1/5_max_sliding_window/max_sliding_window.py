# python3
from collections import deque


def max_sliding_window_naive(sequence, m):
    maximums = []
    for i in range(len(sequence) - m + 1):
        maximums.append(max(sequence[i:i + m]))

    return maximums


def max_sliding_window_deque_naive(sequence, m):
    d = deque(sequence[:m], maxlen=m)
    maximums = []
    for i in range(len(sequence) - m):
        maximums.append(max(d))
        d.append(sequence[i + m])
    maximums.append(max(d))

    return maximums


def max_sliding_window_deque(sequence, m):
    d = deque(sequence[:m], maxlen=m)

    max_val = max(d)
    maximums = [max_val]

    for i in range(len(sequence) - m):
        next_elem = sequence[i + m]
        if next_elem >= max_val:
            max_val = next_elem
            d.clear()
            d.append(next_elem)
        else:
            d.append(next_elem)
            max_val = max(d)
        maximums.append(max_val)

    return maximums


def max_sliding_window_deque_idx(sequence, m):
    d = deque()

    maximums = []

    for i in range(m):
        new_elem = sequence[i]
        while (len(d) > 0) and (sequence[d[-1]] < new_elem):
            d.pop()
        d.append(i)

    for i in range(m, len(sequence)):
        maximums.append(sequence[d[0]])

        new_elem = sequence[i]

        while (len(d) > 0) and (d[0] <= (i - m)):
            d.popleft()

        while (len(d) > 0) and (sequence[d[-1]] < new_elem):
            d.pop()

        d.append(i)

    maximums.append(sequence[d[0]])

    return maximums


if __name__ == '__main__':
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window_deque_idx(input_sequence, window_size))

