def binary_search(data, target):
    data.sort()
    start = 0
    end = len(data) - 1

    while start <= end:
        mid = (start + end) // 2

        if data[mid] == target:
            return mid # 함수를 끝내버린다.
        elif data[mid] < target:
            start = mid + 1
        else:
            end = mid -1

    return -1


def bubble_sort_with_key(arr, key_arr):
    end = len(arr) - 1
    while end > 0:
        last_swap = 0
        for i in range(end):
            if arr[i] < arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                key_arr[i], key_arr[i + 1] = key_arr[i + 1], key_arr[i]
                last_swap = i
        end = last_swap

    return {key_arr[k]: arr[k] for k in range(len(arr))}