# Uses python3

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


def compare_by_position(str_num1, str_num2):
    """
    Circularly fill numbers to the combined length.
    Compare by first non-equal number on same position.

    Input: str_num1, str_num2 - str
    Output: 1 if str_num1 is greater when combined with str_num2 than str_num2 else -1
    """
    total_len = len(str_num1) + len(str_num2)

    # circularly extend numbers
    str_num1 = circum_fill_str(str_num1, total_len)
    str_num2 = circum_fill_str(str_num2, total_len)

    cmp_flag = -1

    for i in range(total_len):
        c1, c2 = int(str_num1[i]), int(str_num2[i])
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
    n = input()
    nums = input().split()

    print(largest_number_fast(nums))
