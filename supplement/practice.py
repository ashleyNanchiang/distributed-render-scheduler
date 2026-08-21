import heapq
import time

arr = []
arr2 = []

heapq.heappush(arr, (1, "cat"))
heapq.heappush(arr, (5, "dog"))
heapq.heappush(arr, (3, "bear"))
arr2.append(arr.pop()[1])
arr2.append(arr.pop()[1])
arr2.append(arr.pop()[1])
print(arr2)

i = 0

while i <= 10:
    print(f"\r{"=" * i}{"-" * (10-i)}", end="")
    i += 1
    time.sleep(0.1)
print()

total = 20
for i in range(total + 1):
    filled = "█" * i
    empty = "░" * (total - i)
    percent = (i / total) * 100
    print(f"\r[{filled}{empty}] {percent:.0f}%", end="")
    time.sleep(0.2)

print()