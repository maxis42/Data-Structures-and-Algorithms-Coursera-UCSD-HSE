# Uses python3


def greedy_optimal_sequence(n):
    """
    Actually not optimal
    """
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
    """
    Possible operation types:
    1 - multiply by 2
    2 - multiply by 3
    3 - add 1
    """

    # n elements as we calculate number of operations starting from 1
    # elements [1, n]
    min_num_operations = [n] * n
    min_num_operations[0] = 0

    # operations array - write only last operation
    # sequence would be restored by this operations
    ops = [-1] * n

    # types of operations
    op_types = (1, 2, 3)

    # iterate from 0 till n-1
    for i in range(n-1):
        # iterate through operations
        for op_type in op_types:
            n_i = i + 1
            # multiply by 2
            if op_type == 1:
                n_new = n_i * 2
            # multiply by 3
            elif op_type == 2:
                n_new = n_i * 3
            # add 1
            elif op_type == 3:
                n_new = n_i + 1
            else:
                raise ValueError("New operation type {}".format(op_type))

            num_operations = min_num_operations[i] + 1
            i_new = n_new - 1

            # check if number of operations is less than the previous number
            if n_new <= n and num_operations < min_num_operations[i_new]:
                min_num_operations[i_new] = num_operations
                ops[i_new] = op_type

    seq = get_sequence(n, ops)

    return seq


def get_sequence(n, ops):
    """
    Get number n from 1 in reversed order (from n to 1)
    """
    n_seq = n
    seq = [n]
    while n_seq != 1:
        i = n_seq - 1
        op_type = ops[i]
        # multiply by 2
        if op_type == 1:
            n_seq = n_seq // 2
        # multiply by 3
        elif op_type == 2:
            n_seq = n_seq // 3
        # add 1
        elif op_type == 3:
            n_seq = n_seq - 1
        else:
            raise ValueError("New operation type {}".format(op_type))
        seq.append(n_seq)
    return seq[::-1]


def get_optimal_operations(value):
    best_num_ops = [value] * (value + 1)
    best_num_ops[0] = 0
    best_ops = [""] * (value + 1)

    for i in range(1, value + 1):
        # +1
        num_ops_1 = best_num_ops[i - 1] + 1

        # x2
        if i % 2 == 0:
            num_ops_2 = best_num_ops[i // 2] + 1
        else:
            num_ops_2 = value

        # x3
        if i % 3 == 0:
            num_ops_3 = best_num_ops[i // 3] + 1
        else:
            num_ops_3 = value

        num_ops = [num_ops_1, num_ops_2, num_ops_3]
        cur_best_num_ops = min(num_ops)
        cur_best_num_ops_idx = num_ops.index(cur_best_num_ops)

        best_num_ops[i] = cur_best_num_ops
        if cur_best_num_ops_idx == 0:
            best_ops[i] = "+1"
        elif cur_best_num_ops_idx == 1:
            best_ops[i] = "x2"
        elif cur_best_num_ops_idx == 2:
            best_ops[i] = "x3"
        else:
            raise

    values = []
    res = value
    while res != 0:
        values.append(res)
        if best_ops[res] == "+1":
            res -= 1
        elif best_ops[res] == "x2":
            res = res // 2
        elif best_ops[res] == "x3":
            res = res // 3
        else:
            raise

    values.reverse()

    print(len(values) - 1, values)


if __name__ == '__main__':
    n = int(input())
    sequence = list(optimal_sequence(n))
    print(len(sequence) - 1)
    for x in sequence:
        print(x, end=' ')

    # get_optimal_operations(n)
