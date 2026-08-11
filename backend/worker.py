from job import Job
from task import Task
from scheduler import Scheduler

class Worker:
    def __init__(self, scheduler, worker_id, efficiency):
        self.shceduler = scheduler
        self.id = worker_id
        self.efficiency = efficiency

    def __repr__(self):
            return f"Worfer('{self.name}', {self.age})"
    
        