from enum import Enum

# for jobs
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

# for jobs
class Priority(Enum):
    top = 1
    general = 2
    low = 3