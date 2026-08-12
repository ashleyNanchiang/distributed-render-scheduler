from backend.enums import Status
from backend.job import Job
from backend.task import Task
from backend.scheduler import Scheduler
import time

class Worker:
    EXE_TIME_PER_FRAME = 3                # 3 sec

    def __init__(self, scheduler, worker_id, efficiency):
        self.shceduler = scheduler
        self.id = worker_id
        self.efficiency = efficiency
        self.status = Status.starting

    def start(self):
        self.status = Status.idle

    def execute_task(self, task):
        print(f"Worker {self.id} start task {task.id}")
        execution_time = Worker.EXE_TIME_PER_FRAME * task.complexity * (1 / self.efficiency) * task.end_frame
        time.sleep(execution_time)
        print(f"Worker {self.id} finish task {task.id}: time = {execution_time}")

    def __repr__(self):
            return f"Worker('{self.id}', {self.efficiency})"
    
        