from enums import State
class Job:
    def __init__(self, job_id, user_id, shots, priority):
        self.id = job_id
        self.user_id = user_id
        self.shots = shots
        self.priority = priority
        self.state = State.created

    
