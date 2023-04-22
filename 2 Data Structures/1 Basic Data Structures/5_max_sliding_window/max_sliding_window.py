# python3
from collections import deque


def max_sliding_window_naive(arr, window):
    maximums = []
    for i in range(len(arr) - window + 1):
        maximums.append(max(arr[i:i + window]))

    return maximums


def max_sliding_window_deque_naive(arr, window):
    d = deque(arr[:window], maxlen=window)
    maximums = []
    for i in range(len(arr) - window):
        maximums.append(max(d))
        d.append(arr[i + window])
    maximums.append(max(d))

    return maximums


def max_sliding_window_deque(arr, window):
    d = deque(arr[:window], maxlen=window)

    max_val = max(d)
    maximums = [max_val]

    for i in range(len(arr) - window):
        next_elem = arr[i + window]
        if next_elem >= max_val:
            # main idea:
            # clear deque if the new element no less than the previous
            # maximum element
            max_val = next_elem
            d.clear()
            d.append(next_elem)
        else:
            d.append(next_elem)
            max_val = max(d)
        maximums.append(max_val)

    return maximums


def max_sliding_window_deque_idx(arr, window):
    # main idea:
    # store in deque indices of maximum elements (not elements)
    # example: arr = [2, 7, 3, 1, 5, 2, 6, 2], w = 4
    # deque with indices:
    # create the first window
    # [0] -> [1] -> [1, 2] -> [1, 2, 3]
    # iterate by elements
    # [1, 2, 3] -> [1, 4] -> [4, 5] -> [6] -> [6, 7]
    # maximums are the first deque elements on every step:
    # indices [1, 1, 4, 6, 6]
    # values  [7, 7, 5, 6, 6]

    d = deque()

    maximums = []

    for i in range(window):
        new_elem = arr[i]
        while (len(d) > 0) and (arr[d[-1]] < new_elem):
            d.pop()
        d.append(i)

    for i in range(window, len(arr)):
        maximums.append(arr[d[0]])

        new_elem = arr[i]

        # drop indices out of current window
        while (len(d) > 0) and (d[0] <= (i - window)):
            d.popleft()

        # drop indices which elements are lower than the new element
        while (len(d) > 0) and (arr[d[-1]] < new_elem):
            d.pop()

        d.append(i)

    maximums.append(arr[d[0]])

    return maximums


if __name__ == '__main__':
    n = int(input())
    input_sequence = [int(i) for i in input().split()]
    assert len(input_sequence) == n
    window_size = int(input())

    print(*max_sliding_window_deque_idx(input_sequence, window_size))
