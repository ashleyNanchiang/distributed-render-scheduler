from enum import IntEnum

# for jobs and tasks
class State(IntEnum):
    pending = 1
    in_progress = 2
    completed = 3
    failed = 4
    paused = 5
    terminated = 6

# for workers themselves
class Status(IntEnum):
    starting = 1
    idle = 2
    busy = 3
    disabled = 4
    failure = 5
    shutting_down = 6
    off = 7

# for scheduler tracking workers
class StatusForWorker(IntEnum):
    idle = 1
    busy = 2
    disabled = 3
    disconnected = 4
    off = 5

# for jobs and tasks
class Priority(IntEnum):
    high = 1
    mid = 2
    low = 3

# for shots
class Complexity(IntEnum):
    high = 4
    mid = 2
    low = 1