# python3
import sys


class StackWithMax:
    def __init__(self):
        self.__stack = []
        self.__stack_max = []
        self.__len_stack = 0

    def push(self, a):
        # add stack max element
        if self.__len_stack > 0:
            prev_max = self.__stack_max[-1]
            new_max = a if a > prev_max else prev_max
            self.__stack_max.append(new_max)
        else:
            self.__stack_max.append(a)

        self.__stack.append(a)
        self.__len_stack += 1

    def pop(self):
        assert self.__len_stack

        self.__stack.pop()
        self.__stack_max.pop()
        self.__len_stack -= 1

    def max(self):
        assert self.__len_stack
        return self.__stack_max[-1]


if __name__ == '__main__':
    stack = StackWithMax()

    num_queries = int(sys.stdin.readline())
    for _ in range(num_queries):
        query = sys.stdin.readline().split()

        if query[0] == "push":
            stack.push(int(query[1]))
        elif query[0] == "pop":
            stack.pop()
        elif query[0] == "max":
            print(stack.max())
        else:
            raise NotImplementedError()
