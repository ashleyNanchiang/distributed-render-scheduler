import sys
import random

import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.enums import Complexity

MAX_FRAMES = 300

shot_number = 10

if len(sys.argv) > 1:
    shot_number = int(sys.argv[1])

scene_number = random.randint(1, (int) (shot_number / 10 + 1))

shots_per_scene = []

curr_scene = 1
total = shot_number

if scene_number == 1:
    shots_per_scene.append(total)
else:
    while curr_scene <= scene_number and total != 0:
        num = random.randint(1, total)
        if curr_scene == scene_number:
            num = total
        shots_per_scene.append(num)
        total -= num
        curr_scene += 1

scene_number = curr_scene - 1
curr_shot_all = 1
curr_scene = 1
curr_shot = 1

with open("shotlist.csv", "w") as f:
    f.write("id,frames,complexity\n")
    while curr_scene <= scene_number:
        for i in range(shots_per_scene[curr_scene-1]):
            frames = random.randint(1, MAX_FRAMES)
            complexity = random.choice(list(Complexity))
            f.write(f"sc{curr_scene:03}_sh{(i+1):03},{frames},{complexity.name}\n")
        curr_scene += 1



