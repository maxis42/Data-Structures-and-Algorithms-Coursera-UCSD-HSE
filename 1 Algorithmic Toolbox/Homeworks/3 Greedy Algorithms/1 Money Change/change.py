# Uses python3


def get_change(m):
    types_of_coins = [1, 5, 10]
    counter_of_coins = 0
    while m != 0:
        if m // max(types_of_coins) != 0:
            counter_of_coins += 1
            m -= max(types_of_coins)
        else:
            types_of_coins.remove(max(types_of_coins))
    return counter_of_coins


if __name__ == '__main__':
    m = int(input())
    print(get_change(m))
