from backend.enums import Status
from backend.job import Job
from backend.task import Task
from backend.scheduler import Scheduler
import time
import threading
import random

class Worker:
    EXE_TIME_PER_FRAME = 3                # 3 sec

    def __init__(self, scheduler, worker_id, efficiency):
        self.shceduler = scheduler
        self.id = worker_id
        self.efficiency = efficiency
        self.status = Status.starting
        self.HEARTBEAT_TIME = 5
        self.curr_task = None

    def start(self):
        self.thread_heartbeat = threading.Thread(target=self.send_heartbeat)
        self.thread_run = threading.Thread(target=self.run)
        self.status = Status.idle
        self.thread_heartbeat.start()
        self.thread_run.start()

    def execute_task(self):
        self.status = Status.busy
        print(f"Worker {self.id} start task {self.curr_task.task.id}")
        execution_time = Worker.EXE_TIME_PER_FRAME * self.curr_task.task.complexity * (1 / self.efficiency) * self.curr_task.task.end_frame
        time.sleep(execution_time)
        print(f"Worker {self.id} finish task {self.curr_task.task.id}: time = {execution_time}")
        self.status = Status.idle

    def request_task(self):
        return self.scheduler.request_task()

    def send_heartbeat(self):
        while True:
            check_failure = random.random()
            if check_failure < 0.01: 
                self.Status = Status.failure

            match self.status:
                case Status.idle | Status.busy | Status.sleeping:
                    if self.curr_task is None:
                        task_id = -1
                    else:
                        task_id = self.curr_task.id
                    self.shceduler.receive_heartbeat([self.id, self.status, task_id])
                    
                case Status.failure | _:
                    check_recovery = random.random()
                    if check_recovery < 0.01:
                        self.Status = Status.idle
                    return None

    def run(self):
        while True:
            match self.status:
                case Status.shutting_down:
                    break
                case Status.idle:
                    if self.curr_task is None:
                        self.curr_task = self.request_task()
                        if self.curr_task is not None:
                            self.execute_task()
                            self.status = Status.busy                
                 
    def shutdown(self):
        self.status = Status.shutting_down
        self.thread_heartbeat.join()
        self.thread_run.join()
        self.status = Status.off
         
    def __repr__(self):
            return f"Worker('{self.id}', {self.efficiency})"
    
        