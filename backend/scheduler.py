from backend.job import Job
from backend.task import Task
from backend.shot import Shot
from backend.enums import StatusForWorker, State
import heapq
import time
import threading

class Scheduler:
    def __init__(self):
        self.worker_list = {}       # key: worker id, value: (status, time of last received heartbeat)
        self.job_list = {}          # for display purposes
        self.task_list = {}         # all tasks (finished or not), key is task id, value is task object
        self.pending_tasks = []     # tasks not assigned yet, priority queue
        self.assigned_tasks = {}    # assigned tasks, key is worker id, value is task id (-1 if no worker is assigned)
        self.FRAME_SPLIT = 50
        self.FRAME_THRESHOLD = 5
        self.current_task_id = 0
        self.current_job_id = 0
        self.HEARTBEAT_TIMECHECK = 30
        self.lock = threading.Lock()

    def start(self):
        self.thread_track = threading.Thread(target=self.track_heartbeats)
        self.thread_rearrange = threading.Thread(target=self.rearrange_queue)
        self.thread_track.start()
        self.thread_rearrange.start()
        
    # heartbeat = [worker_id, worker_status, worker_current_task_id]
    def receive_heartbeat(self, heartbeat):
        match heartbeat[1]:
            case StatusForWorker.idle:
                status = StatusForWorker.idle
            case StatusForWorker.busy:
                status = StatusForWorker.busy
        with self.lock:
            self.assigned_tasks[heartbeat[0]] = heartbeat[2]
            self.worker_list[heartbeat[0]] = (status, time.time())
    
    def add_job(self, job):
        self.job_list[job.id] = job
        self.split_job_to_tasks(job)

    def track_heartbeats(self):
        while True:
            for id, record in self.worker_list.items():
                # id: worker id
                # record: (status, time of last received heartbeat)
                if (time.time() - record[1]) > self.HEARTBEAT_TIMECHECK:
                    record[0] = StatusForWorker.disconnected
                    # reassign task: push task back to pending
                    reassigned_task_id = self.assigned_tasks[id]
                    with self.lock:
                        self.assigned_tasks[id] = -1
                        reassigned_task = self.task_list[reassigned_task_id]
                        heapq.heappush(self.pending_tasks, (reassigned_task.priority, reassigned_task.time_created, reassigned_task.id, reassigned_task.id))
            time.sleep(5)

    # split jobs into tasks, based on number of frames
    def split_job_to_tasks(self, job):
        
        for sh in job.shots:
            if sh.frames <= self.FRAME_SPLIT:
                with self.lock:
                    self.task_list[self.current_task_id] = Task(self.current_task_id, job.id, sh, 1, sh.frames, job.time_created, job.priority)
                    heapq.heappush(self.pending_tasks, (job.priority, job.time_created, self.current_task_id, self.current_task_id))
                    self.current_task_id += 1
            else:
                curr_frame = 0
                while curr_frame < sh.frames:
                    end_frame = curr_frame + self.FRAME_SPLIT
                    if end_frame > sh.frames or sh.frames - end_frame <= self.FRAME_THRESHOLD:
                        end_frame = sh.frames
                    curr_frame += 1
                    with self.lock:
                        self.task_list[self.current_task_id] = Task(self.current_task_id, job.id, sh, curr_frame, end_frame, job.time_created, job.priority)
                        heapq.heappush(self.task_list, (job.priority, job.time_created, self.current_task_id, self.current_task_id))
                        self.current_task_id += 1
                    curr_frame = end_frame
                    
    def rearrange_queue(self):
        while True:
            current_time = time.time()
            for task in self.pending_tasks:
                if current_time - task.time_created >= 60:
                    pass
            time.sleep(5)
    
    def request_task(self, worker_id):
        if len(self.pending_tasks) > 0:
            task_id = heapq.heappop(self.pending_tasks)
            task = self.task_list[task_id]
            with self.lock:
                self.assigned_tasks[worker_id] = task_id
            task.state = State.in_progress
            task.assigned_worker = worker_id
            return task
        return None

    def finish_task(self, worker_id, task_id):
        with self.lock:
            task = self.task_list[task_id]
            task.state = State.completed
            task.time_completed = time.time()
            task.worker_complete = worker_id
            self.assigned_tasks[worker_id] = -1

    def terminate_task(self, worker_id, task_id):
        with self.lock:
            task = self.task_list[task_id]
            task.state = State.terminated
            task.time_completed = time.time()
            task.worker_complete = worker_id
            self.assigned_tasks[worker_id] = -1

