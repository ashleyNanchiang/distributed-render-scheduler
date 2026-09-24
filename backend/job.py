from enums import State, Priority
from datetime import datetime

class Job:
    def __init__(self, job_id, user_id, shots, priority):
        self.id = job_id
        self.user_id = user_id
        self.shots = shots
        self.priority = priority
        self.state = State.pending
        self.time_created = datetime.now()
        self.progress = 0                       # 0 to 100 (percent)

    def add_shot(self, shot):
        self.shots.append(shot)

    def current_progress(self):
        pass
        
    def __repr__(self):
        return f"Job('{self.id}', {self.user_id}, {len(self.shots)}, {self.priority}, {self.time_created})"

    def __eq__(self, other):
        if not isinstance(other, Job):
            return False
        return self.id == other.id and self.user_id == other.user_id and self.time_created == other.time_created and self.priority == other.priority
    
