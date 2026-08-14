from backend.scheduler import Scheduler
from backend.shot import Shot
from backend.job import Job
from backend.task import Task
from backend.enums import Complexity
from backend.enums import Priority
import heapq

def test_splitTask_at_threshold():
    sched = Scheduler()
    shot_1_1 = Shot("shot_1_1", 55, Complexity.high)
    shot_1_2 = Shot("shot_1_2", 3, Complexity.mid)
    shot_1_3 = Shot("shot_1_3", 56, Complexity.mid)

    job_1 = Job(0, 0, [], Priority.mid)
    job_1.add_shot(shot_1_1)
    job_1.add_shot(shot_1_2)
    job_1.add_shot(shot_1_3)

    sched.add_job(job_1)

    task_list_correct = [
                 Task(0, 0, shot_1_1, 1, 55, job_1.time_created, job_1.priority),
                 Task(1, 0, shot_1_2, 1, 3, job_1.time_created, job_1.priority),
                 Task(2, 0, shot_1_3, 1, 50, job_1.time_created, job_1.priority),
                 Task(3, 0, shot_1_3, 51, 56, job_1.time_created, job_1.priority),
                 ]
    
    task_list_result = []

    while len(sched.task_list) != 0:
        task_list_result.append(heapq.heappop(sched.task_list)[3])

    assert task_list_result == task_list_correct


def test_splitTask_multiple_jobs():
    sched = Scheduler()
    shot_1_1 = Shot("shot_1_1", 50, Complexity.high)
    shot_1_2 = Shot("shot_1_2", 55, Complexity.mid)
    shot_1_3 = Shot("shot_1_3", 125, Complexity.high)
    shot_1_4 = Shot("shot_1_4", 101, Complexity.low)
    shot_2_1 = Shot("shot_2_1", 37, Complexity.low)
    shot_2_2 = Shot("shot_2_2", 32, Complexity.mid)

    job_1 = Job(0, 0, [], Priority.mid)
    job_1.add_shot(shot_1_1)
    job_1.add_shot(shot_1_2)
    job_1.add_shot(shot_1_3)
    job_1.add_shot(shot_1_4)

    job_2 = Job(1, 0, [], Priority.high)
    job_2.add_shot(shot_2_1)
    job_2.add_shot(shot_2_2)

    sched.add_job(job_1)
    sched.add_job(job_2)

    task_list_correct = [Task(7, 1, shot_2_1, 1, 37, job_2.time_created, job_2.priority),
                 Task(8, 1, shot_2_2, 1, 32, job_2.time_created, job_2.priority),
                 Task(0, 0, shot_1_1, 1, 50, job_1.time_created, job_1.priority),
                 Task(1, 0, shot_1_2, 1, 55, job_1.time_created, job_1.priority),
                 Task(2, 0, shot_1_3, 1, 50, job_1.time_created, job_1.priority),
                 Task(3, 0, shot_1_3, 51, 100, job_1.time_created, job_1.priority),
                 Task(4, 0, shot_1_3, 101, 125, job_1.time_created, job_1.priority),
                 Task(5, 0, shot_1_4, 1, 50, job_1.time_created, job_1.priority),
                 Task(6, 0, shot_1_4, 51, 101, job_1.time_created, job_1.priority)]
    
    task_list_result = []

    while len(sched.task_list) != 0:
        task_list_result.append(heapq.heappop(sched.task_list)[3])

    assert task_list_result == task_list_correct

    # tasks:
    # Task(0, 0, shot_1_1, 1, 50, job_1.time_created, job_1.priority)
    # Task(1, 0, shot_1_2, 1, 55, job_1.time_created, job_1.priority)
    # Task(2, 0, shot_1_3, 1, 50, job_1.time_created, job_1.priority)
    # Task(3, 0, shot_1_3, 51, 100, job_1.time_created, job_1.priority)
    # Task(4, 0, shot_1_3, 101, 125, job_1.time_created, job_1.priority)
    # Task(5, 0, shot_1_4, 1, 50, job_1.time_created, job_1.priority)
    # Task(6, 0, shot_1_4, 51, 101, job_1.time_created, job_1.priority)
    # Task(7, 1, shot_2_1, 1, 37, job_2.time_created, job_2.priority)
    # Task(8, 1, shot_2_2, 1, 32, job_2.time_created, job_2.priority)
