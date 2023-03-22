# Uses python3


def get_optimal_value(capacity, values, weights):
    value = 0.

    cost = [v/w for v, w in zip(values, weights)]
    sort_ind = [i for _, i in sorted(zip(cost, range(len(cost))), reverse=True)]

    for i in range(len(cost)):
        i_sorted = sort_ind[i]

        if capacity == 0:
            return value

        capacity_red = min(weights[i_sorted], capacity)
        capacity -= capacity_red
        value += capacity_red * cost[i_sorted]

    return value


if __name__ == "__main__":
    n, capacity = map(int, input().split())
    values = []
    weights = []
    for _ in range(n):
        v, w = map(int, input().split())
        values.append(v)
        weights.append(w)

    opt_value = get_optimal_value(capacity, values, weights)
    print("{:.10f}".format(opt_value))
