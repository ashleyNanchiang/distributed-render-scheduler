from backend.job import Job
from backend.task import Task
from backend.shot import Shot
import heapq

class Scheduler:
    def __init__(self):
        self.worker_list = []
        self.job_list = {}          # for display purposes
        self.task_list = []         # tasks given to workers, priority queue
        self.FRAME_SPLIT = 50
        self.FRAME_THRESHOLD = 5
        self.current_task_id = 0
        self.current_job_id = 0

    def add_worker(self, worker):
        self.worker_list.append(worker)
    
    def add_job(self, job):
        self.job_list[job.id] = job
        self.split_job_to_tasks(job)

    def split_job_to_tasks(self, job):
        # split base on frames
        for sh in job.shots:
            if sh.frames <= self.FRAME_SPLIT:
                curr_task = Task(self.current_task_id, job.id, sh, 1, sh.frames, job.time_created, job.priority)
                heapq.heappush(self.task_list, (job.priority, job.time_created, curr_task.id, curr_task))
                self.current_task_id += 1
            else:
                curr_frame = 0
                while curr_frame < sh.frames:
                    end_frame = curr_frame + self.FRAME_SPLIT
                    if end_frame > sh.frames or sh.frames - end_frame <= self.FRAME_THRESHOLD:
                        end_frame = sh.frames
                    curr_frame += 1
                    curr_task = Task(self.current_task_id, job.id, sh, curr_frame, end_frame, job.time_created, job.priority)
                    heapq.heappush(self.task_list, (job.priority, job.time_created, curr_task.id, curr_task))
                    curr_frame = end_frame
                    self.current_task_id += 1
                    
    def request_task():
        return 0

    

