# python3

from collections import namedtuple

Bracket = namedtuple("Bracket", ["char", "position"])


def are_matching(left, right):
    return (left + right) in ["()", "[]", "{}"]


def is_balanced(text):
    match = False

    opening_brackets_stack = []

    for i, char_next in enumerate(text):
        if char_next in "([{":
            opening_brackets_stack.append(char_next)
        elif char_next in ")]}":
            char_last = opening_brackets_stack.pop()
            if not are_matching(char_last, char_next):
                break
        else:
            raise NotImplementedError()
    else:
        if len(opening_brackets_stack) == 0:
            match = True

    return match


def find_mismatch(text):
    opening_brackets_stack = []

    for i, char_next in enumerate(text):
        # closing bracket
        if char_next in ")]}":
            match_inner = True

            # find opening bracket
            for _ in range(len(opening_brackets_stack)):
                last_char = opening_brackets_stack.pop()
                if last_char in "([{":
                    if not are_matching(last_char, char_next):
                        match_inner = False
                    break
            # no opening bracket
            else:
                match_inner = False

            # no match
            if not match_inner:
                break
        # opening bracket or other char
        else:
            opening_brackets_stack.append(char_next)
    # all closing brackets matched
    # check whether there are any unclosed opening brackets
    else:
        for bracket in "([{":
            if bracket in opening_brackets_stack:
                break
        else:
            return "Success"

    text_processed = list(reversed(text[:(i + 1)]))
    closing_brackets_stack = []
    for j, char_next in enumerate(text_processed):
        # closing bracket
        if char_next in "([{":
            match_inner = True

            # find opening bracket
            for _ in range(len(closing_brackets_stack)):
                last_char, j_prev = closing_brackets_stack.pop()
                if last_char in ")]}":
                    if not are_matching(char_next, last_char):
                        match_inner = False
                        closing_brackets_stack.append((last_char, j_prev))
                    break
            # no opening bracket
            else:
                match_inner = False

            # no match
            if not match_inner:
                break
        # opening bracket or other char
        elif char_next in ")]}":
            closing_brackets_stack.append((char_next, j))
        else:
            pass

    if len(closing_brackets_stack) == 0:
        return len(text_processed) - j
    else:
        return len(text_processed) - closing_brackets_stack.pop()[1]


def main():
    text = input()
    mismatch = find_mismatch(text)
    print(mismatch)


if __name__ == "__main__":
    main()
