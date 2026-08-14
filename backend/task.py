from backend.enums import State

class Task:
    def __init__ (self, task_id, job_id, shot, start, end, time, priority):
        self.id = task_id
        self.job_id = job_id
        self.shot = shot
        self.start_frame = start
        self.end_frame = end
        self.time_created = time
        self.state = State.created
        self.priority = priority

    def __repr__(self):
        return f"Task('{self.id}', {self.job_id}, {self.shot}, {self.start_frame}, {self.end_frame}, {self.time_created}, {self.priority})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.id == other.id and self.job_id == other.job_id and self.start_frame == other.start_frame and self.end_frame == other.end_frame and self.time_created == other.time_created and self.priority == other.priority