import heapq

arr = []
arr2 = []

heapq.heappush(arr, (1, "cat"))
heapq.heappush(arr, (5, "dog"))
heapq.heappush(arr, (3, "bear"))
arr2.append(arr.pop()[1])
arr2.append(arr.pop()[1])
arr2.append(arr.pop()[1])
print(arr2)
