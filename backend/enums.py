from enum import Enum

# for jobs and tasks
class State(Enum):
    created = 1
    pending = 2
    in_progress = 3
    completed = 4
    failed = 5
    paused = 6
    terminated = 7

# for workers
class Status(Enum):
    starting = 1
    idle = 2
    busy = 3
    sleeping = 4
    disconnected = 5
    off = 6

# for jobs and tasks
class Priority(Enum):
    high = 1
    normal = 2
    low = 3

# for shots
class Complexity(Enum):
    high = 4
    mid = 2
    low = 1