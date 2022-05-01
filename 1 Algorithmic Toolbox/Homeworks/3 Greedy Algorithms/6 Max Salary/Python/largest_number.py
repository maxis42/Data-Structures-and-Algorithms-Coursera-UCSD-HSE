# Uses python3

import sys
from functools import cmp_to_key


def largest_number(digits):
    res = ""

    digits = list(map(int, digits))

    while digits:
        max_digit = -1
        for d in digits:
            if d >= max_digit:
                max_digit = d
        res += str(max_digit)
        digits.remove(max_digit)

    return res


def circum_fill_str(s, length):
    i = 0
    while len(s) != length:
        s += s[i]
        i += 1
    return s


def compare_by_position(item1, item2):
    """
    If items lengths are not equal, circularly fill smaller item
    Compare by first non-equal number on same position

    Input: item1, item2 - str
    Output: 1 if item1 > item2 else -1
    """
    items = [item1, item2]

    item_len0 = len(items[0])
    item_len1 = len(items[1])
    item_len = max(item_len0, item_len1)

    # circularly extend the smaller item
    if item_len0 != item_len1:
        if item_len0 < item_len:
            items[0] = circum_fill_str(items[0], item_len)
        else:
            items[1] = circum_fill_str(items[1], item_len)

    cmp_flag = -1

    for i in range(item_len):
        c1, c2 = int(items[0][i]), int(items[1][i])
        if c1 != c2:
            if c1 > c2:
                cmp_flag = +1
                break
            else:
                break

    return cmp_flag


def largest_number_fast(digits):
    res = ''.join(sorted(digits, key=cmp_to_key(compare_by_position), reverse=True))

    return res


if __name__ == '__main__':
    input = sys.stdin.read()

    data = input.split()
    a = data[1:]

    print(largest_number_fast(a))
