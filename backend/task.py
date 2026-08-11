from enums import State

class Task:
    def __init__ (self, task_id, job_id, shot, start, end, time):
        self.id = task_id
        self.job_id = job_id
        self.shot = shot
        self.start_frame = start
        self.end_frame = end
        self.time_created = time
        self.state = State.created
        