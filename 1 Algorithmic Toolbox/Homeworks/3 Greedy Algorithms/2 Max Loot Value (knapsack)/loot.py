# Uses python3
import sys


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
    data = list(map(int, sys.stdin.read().split()))

    n, capacity = data[0:2]
    values = data[2:(2 * n + 2):2]
    weights = data[3:(2 * n + 2):2]

    opt_value = get_optimal_value(capacity, weights, values)
    print("{:.10f}".format(opt_value))
