# Uses python3


def get_change(amount, coins=(1, 3, 4)):
    # initialize minimum number of coins list with max value of m
    min_num_coins = [amount] * (amount + 1)

    # zero money - zero coins
    min_num_coins[0] = 0

    # iterate through all values of money up to m
    for m_i in range(1, amount + 1):
        # iterate through coins
        for coin in coins:
            # check if coin doesn't exceed money
            if coin <= m_i:
                num_coins = min_num_coins[m_i - coin] + 1

                if num_coins < min_num_coins[m_i]:
                    min_num_coins[m_i] = num_coins

    return min_num_coins[amount]


if __name__ == '__main__':
    amount = int(input())
    print(get_change(amount))
