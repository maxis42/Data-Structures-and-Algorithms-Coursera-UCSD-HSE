# Uses python3


def get_change(m):
    types_of_coins = [10, 5, 1]
    types_of_coins.sort(reverse=True)
    coins_cnt = 0

    while m != 0:
        cur_coin = types_of_coins[0]

        if m >= cur_coin:
            first_coin_cnt = m // cur_coin
            coins_cnt += first_coin_cnt

            m -= first_coin_cnt * cur_coin

        types_of_coins = types_of_coins[1:]
    return coins_cnt


if __name__ == '__main__':
    m = int(input())
    print(get_change(m))
