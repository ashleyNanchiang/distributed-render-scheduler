from enums import Status
from job import Job
from task import Task
from scheduler import Scheduler
import time
import threading
import random

class Worker:
    EXE_TIME_PER_FRAME = 3                # 3 sec

    def __init__(self, scheduler, worker_id, efficiency):
        self.scheduler = scheduler
        self.id = worker_id
        self.efficiency = efficiency
        self.status = Status.starting
        self.curr_task = None

        self.HEARTBEAT_TIME = 5
        self.HEARTBEAT_FAILURE = 0.01
        self.HEARTBEAT_RECOVER = 0.01

        self.EXE_UPPER_LIMIT = 1.5
        self.EXE_LOWER_LIMIT = 0.5
        self.EXE_CENTER = 1.0
        self.EXE_STD = 0.17

        self.lock = threading.Lock()

    def start(self):
        self.status = Status.idle
        self.thread_heartbeat = threading.Thread(target=self.send_heartbeat)
        self.thread_run = threading.Thread(target=self.run)
        self.thread_heartbeat.start()
        self.thread_run.start()

    def execute_task(self):
        random_factor = random.gauss(self.EXE_CENTER, self.EXE_STD)
        random_factor = max(self.EXE_LOWER_LIMIT, min(self.EXE_UPPER_LIMIT, random_factor))
        execution_time = Worker.EXE_TIME_PER_FRAME * self.curr_task.task.complexity * (1 / self.efficiency) * self.curr_task.task.end_frame * random_factor
        elapsed_time = 0
        with self.lock:
            self.status = Status.busy

        while(self.status != Status.failure):

            if elapsed_time+1 < execution_time:
                time.sleep(1)
                elapsed_time+=1
            else:
                time.sleep(execution_time - elapsed_time)
                elapsed_time = execution_time
                break
            self.curr_task.current_progress(execution_time, elapsed_time)

            # print(f"Worker {self.id} start task {self.curr_task.task.id}")
            # print(f"Worker {self.id} finish task {self.curr_task.task.id}: time = {execution_time}")
        if(elapsed_time == execution_time):
            with self.lock:
                self.status = Status.idle
        # if exited while loop with status as failure, will just exit function

    def request_task(self):
        return self.scheduler.request_task(self.id)

    def send_heartbeat(self):
        while self.status == Status.idle or self.status == Status.busy or self.status == Status.failure:
            check_failure = random.random()
            if check_failure < self.HEARTBEAT_FAILURE: 
                with self.lock:
                    self.Status = Status.failure

            match self.status:
                case Status.idle | Status.busy | Status.disabled:
                    if self.curr_task is None:
                        task_id = -1
                    else:
                        task_id = self.curr_task.id
                    self.scheduler.receive_heartbeat([self.id, self.status, task_id])
                    
                case Status.failure | _:
                    check_recovery = random.random()
                    if check_recovery < self.HEARTBEAT_RECOVER:
                        with self.lock:
                            self.Status = Status.idle
                    return None

    def run(self):
        while self.status == Status.idle or self.status == Status.busy or self.status == Status.failure:
            match self.status:
                case Status.shutting_down:
                    break
                case Status.idle:
                    if self.curr_task is None:
                        self.curr_task = self.request_task()
                        if self.curr_task is not None: 
                            self.execute_task()
                                    
    def shutdown(self):
        with self.lock:
            self.status = Status.shutting_down
        self.thread_heartbeat.join()
        self.thread_run.join()
        self.status = Status.off
         
    def __repr__(self):
            return f"Worker('{self.id}', {self.efficiency})"
    
        