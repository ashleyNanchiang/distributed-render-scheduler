from backend.job import Job
from backend.task import Task
from backend.scheduler import Scheduler

class User:
    def __init__(self, user_id, user_name):
        self.id = user_id
        self.username = user_name
        self.history = []

    def __repr__(self):
            return f"User('{self.id}', {self.username})"
    
        