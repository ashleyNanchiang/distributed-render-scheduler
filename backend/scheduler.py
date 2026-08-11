from job import Job
from task import Task
from shot import Shot
from worker import Worker
import heapq

class Scheduler:
    def __init__(self):
        self.worker_list = []
        self.job_list = []          # for display purposes
        self.task_list = []         # tasks given to workers, priority queue
        self.frame_threshold = 50
        self.current_task_id = 0
        self.current_job_id = 0

    def addWorker(self, worker):
        self.worker_list.append(worker)
    
    def addJob(self, job):
        self.job_list.append(job)

    def splitJobToTasks(self, job):
        # split base on frames
        for sh in job.shots:
            if sh.frames <= self.frame_threshold:
                curr_task = Task(self.current_task_id, job.id, sh, 1, sh.frames, job.time_created)
                heapq.heappush(self.task_list, (job.priority, job.time_created, curr_task.id, curr_task))
                self.current_task_id += 1
            else:
                curr_frame = 0
                while curr_frame < sh.frames:
                    end_frame = curr_frame + self.frame_threshold
                    if end_frame > sh.frames:
                        end_frame = sh.frames
                    curr_frame += 1
                    curr_task = Task(self.current_task_id, job.id, sh, curr_frame, end_frame, job.time_created)
                    curr_frame = end_frame
                    self.current_task_id += 1
                    





    def request_task():
        return 0

    

