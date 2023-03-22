# Uses python3


def get_optimal_value(capacity, weights, values):
    value = 0.
    cost = [v/w for w, v in zip(weights, values)]
    for _ in range(len(cost)):
        if capacity == 0:
            return value
        indMaxCost = cost.index(max(cost))
        capacityReduction = min(weights[indMaxCost], capacity)
        capacity -= capacityReduction
        value += capacityReduction * cost[indMaxCost]
        del cost[indMaxCost], weights[indMaxCost]
    return value


if __name__ == "__main__":
    n, capacity = map(int, input().split())
    values = []
    weights = []
    for _ in range(n):
        v, w = map(int, input().split())
        values.append(v)
        weights.append(w)

    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
