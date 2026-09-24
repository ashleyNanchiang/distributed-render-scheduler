from enums import State

class Task:
    def __init__ (self, task_id, job_id, shot, start, end, time, priority):
        self.id = task_id
        self.job_id = job_id
        self.shot = shot
        self.start_frame = start
        self.end_frame = end
        self.time_created = time
        self.state = State.pending
        self.priority = priority
        self.time_completed = 0
        self.assigned_worker = -1
        self.worker_complete = -1
        self.progress = 0           # 0 to 100 (percent)

    def current_progress(self, total_time, elapsed_time):
        self.progress = (int) (elapsed_time / total_time * 100)
        if self.progress > 0:
            self.state = State.in_progress
        elif self.progress == 100:
            self.state = State.completed
        return self.progress

    def __repr__(self):
        return f"Task('{self.id}', {self.job_id}, {self.shot}, {self.start_frame}, {self.end_frame}, {self.time_created}, {self.priority})"

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.id == other.id and self.job_id == other.job_id and self.start_frame == other.start_frame and self.end_frame == other.end_frame and self.time_created == other.time_created and self.priority == other.priority