import heapq
import time
import random

def test_heapq():
    arr = []
    arr2 = []

    heapq.heappush(arr, (1, "cat"))
    heapq.heappush(arr, (5, "dog"))
    heapq.heappush(arr, (3, "bear"))
    arr2.append(arr.pop()[1])
    arr2.append(arr.pop()[1])
    arr2.append(arr.pop()[1])
    print(arr2)

def random_value():
    x = random.gauss(1.0, 0.17)
    return max(0.5, min(1.5, x))

def test_rand_dist():
    rand = [random_value() for _ in range(100)]
    in_range = 0
    out_range = 0
    for i in rand:
        if i >= 0.8 and i <= 1.2:
            in_range += 1
        else:
            out_range += 1
    print("in_range: ", in_range)
    print("out_range: ", out_range)

def test_progress_bar():
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

test_rand_dist()