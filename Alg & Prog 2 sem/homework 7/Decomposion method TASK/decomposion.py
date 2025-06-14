def find_peak(arr, left, right):

    while left <= right:
        mid = (left + right) // 2
        
        # проверка границы
        if (mid == 0 or arr[mid] >= arr[mid - 1]) and \
           (mid == len(arr) - 1 or arr[mid] >= arr[mid + 1]):
            return arr[mid]
        
        # если левый сосед больше идем влево
        elif mid > 0 and arr[mid - 1] > arr[mid]:
            right = mid - 1
        
        # если правый сосед больше идем вправо
        else:
            left = mid + 1
    
    return arr[left]

def main():

    n = int(input())
    arr = list(map(int, input().split()))
    print(find_peak(arr, 0, n - 1))

if __name__ == "__main__":
    main()

    