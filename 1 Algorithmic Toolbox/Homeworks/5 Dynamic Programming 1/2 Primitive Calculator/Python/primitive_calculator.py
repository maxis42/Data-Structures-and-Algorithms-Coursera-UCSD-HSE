# Uses python3
import sys


def wrong_optimal_sequence(n):
    sequence = []
    while n >= 1:
        sequence.append(n)
        if n % 3 == 0:
            n = n // 3
        elif n % 2 == 0:
            n = n // 2
        else:
            n = n - 1
    return reversed(sequence)


def optimal_sequence(n):
    '''
    Possible operation types:
    1 - multiply by 2
    2 - multiply by 3
    3 - add 1
    '''

    # n+1 elements as we calculate number of operations starting from zero
    min_num_operations = [n+1] * (n+1)
    min_num_operations[0] = 0

    # dictionary with the least possible number of operations
    # for the current element
    ops_dict = dict()
    ops_dict[0] = [0]

    # types of operations
    op_types = (1, 2, 3)

    # iterate from 1 till n
    # first iteration will always use operation type 3
    for n_i in range(1, n+1):
        # iterate through operations
        for op_type in op_types:
            # multiply by 2
            if op_type == 1:
                if n_i % 2 == 0:
                    n_prev = n_i // 2
                    num_operations = min_num_operations[n_prev] + 1
                else:
                    continue

            # multiply by 3
            elif op_type == 2:
                if n_i % 3 == 0:
                    n_prev = n_i // 3
                    num_operations = min_num_operations[n_prev] + 1
                else:
                    continue

            # add 1
            elif op_type == 3:
                n_prev = n_i - 1
                num_operations = min_num_operations[n_prev] + 1

            # check if number of operations is less then the previous number
            if num_operations < min_num_operations[n_i]:
                min_num_operations[n_i] = num_operations
                min_ops_op_type = op_type
                min_ops_n_prev = n_prev

        # write the least possible sequence of operations
        # for the current element
        ops_dict[n_i] = list(ops_dict[min_ops_n_prev])
        ops_dict[n_i].append(min_ops_op_type)

    # get the sequence from the list of operations
    final_seq = [0]
    for op_type in ops_dict[n]:
        if op_type == 1:
            final_seq.append(final_seq[-1]*2)
        elif op_type == 2:
            final_seq.append(final_seq[-1]*3)
        elif op_type == 3:
            final_seq.append(final_seq[-1] + 1)

    return final_seq[1:]


input = sys.stdin.read()
n = int(input)
sequence = list(optimal_sequence(n))
print(len(sequence) - 1)
for x in sequence:
    print(x, end=' ')
