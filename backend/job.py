from backend.enums import State, Priority
from datetime import datetime

class Job:
    def __init__(self, job_id, user_id, shots, priority):
        self.id = job_id
        self.user_id = user_id
        self.shots = shots
        self.priority = priority
        self.state = State.created
        self.time_created = datetime.now()

    def __repr__(self):
        return f"Job('{self.id}', {self.user_id}, {len(self.shots)}, {self.priority}, {self.time_created})"

    
