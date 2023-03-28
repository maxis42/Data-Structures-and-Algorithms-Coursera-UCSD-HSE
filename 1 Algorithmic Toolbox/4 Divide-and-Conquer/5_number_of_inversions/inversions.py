# Uses python3


def num_of_inversions(arr):
    if len(arr) == 1:
        return arr, 0

    mid = len(arr) // 2
    left_sorted, n_inv_left = num_of_inversions(arr[:mid])
    right_sorted, n_inv_right = num_of_inversions(arr[mid:])
    arr_sorted, n_inv_merge = num_of_inversions_merge(left_sorted, right_sorted)
    n_inv = n_inv_left + n_inv_right + n_inv_merge
    return arr_sorted, n_inv


def num_of_inversions_merge(sorted_arr1, sorted_arr2):
    sorted_arr = list()
    n_inv, i, j = 0, 0, 0

    while (i < len(sorted_arr1)) and (j < len(sorted_arr2)):
        if sorted_arr1[i] <= sorted_arr2[j]:
            sorted_arr.append(sorted_arr1[i])
            i += 1
        else:
            sorted_arr.append(sorted_arr2[j])
            j += 1
            n_inv += len(sorted_arr1[i:])

    sorted_arr.extend(sorted_arr1[i:])
    sorted_arr.extend(sorted_arr2[j:])
    return sorted_arr, n_inv


if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))

    print(num_of_inversions(arr)[1])
