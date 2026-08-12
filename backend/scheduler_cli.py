from backend.scheduler import Scheduler
from backend.worker import Worker
from backend.shot import Shot
from backend.job import Job
from backend.enums import Priority
from backend.user import User
import csv

class SchedulerCLI:

    def __init__(self):
        self.workers = []
        self.job_list = []
        self.users = {}
        self.users["demo"] = User(0, "demo")    # for ease of use purposes
        self.curr_worker_id = 0
        self.curr_user_id = 1
        self.curr_job_id = 0

        self.FORMAT_SPACING = 15

        self.sched = Scheduler()

        self.cmd_list = {"submit": self.submit_job,
                    "delete": self.delete_job,
                    "help": self.handle_help,
                    "add": self.handle_add,
                    "status": self.show_status,
                    "exit": self.exit_prog}
        
    def exit_prog(self, arg):
        print("Turning off scheduler...")
        exit()

    def check_user(self, username):
        if username not in self.users:
            print("user not found")
            return 0
        else:
            return self.users[username]
        
    def handle_add(self, arg):
        if len(arg) != 3:
            print("invalid add command: wrong argument length")
            return

        if arg[1] == "-u":
            self.add_user(arg)
        elif arg[1] == "-w":
            self.add_worker(arg)
        else:
            print("invalid add command: invalid tag")
            return

    def add_user(self, arg):

        self.users[arg[2]] = User(self.curr_user_id, arg[2])
        self.curr_user_id += 1

    def add_worker(self, arg):

        try:
            float(arg[2])
        except ValueError:
            print("invalid add command: efficieny should be a number")
            return
        
        self.workers.append(Worker(self.sched, self.curr_worker_id, float(arg[2])))
        self.curr_worker_id += 1

    def submit_job(self, arg):

        if len(arg) == 4:
            if arg[3] == "high":
                priority = Priority.high
            elif arg[3] == "low":
                priority = Priority.low
            elif arg[3] == "mid":
                        priority = Priority.mid
            else:
                print("invalid submit command")
                return
        else:
            print("invalid submit command")
            return

        owner = self.check_user(arg[1])
        if owner == 0:
            return
        
        shot_list = []
        with open(arg[2], "r") as f:
            reader = csv.reader(f)
            next(reader)
            for line in reader:
                shot_list.append(Shot(line[0], line[1], line[2]))

        self.job_list.append(Job(self.curr_job_id, owner.id, shot_list, priority))
        self.curr_job_id += 1

    def delete_job(self, arg):
        print("delete")

    def handle_help(self, arg):
        print("Commands:")
        print("\"submit [user] [csv file] [priority]\"")

    def show_status(self, arg):
        print()
        print(f"{'Worker ID':<{self.FORMAT_SPACING}}{'Efficiency':<{self.FORMAT_SPACING}}{'Status':<{self.FORMAT_SPACING}}")
        print("-" * self.FORMAT_SPACING*3)
        for worker in self.workers:
            print(f"{worker.id:<{self.FORMAT_SPACING}}{worker.efficiency:<{self.FORMAT_SPACING}}{worker.status:<{self.FORMAT_SPACING}}")
        print()

        print(f"{'User ID':<{self.FORMAT_SPACING}}{'Username':<{self.FORMAT_SPACING}}")
        print("-" * self.FORMAT_SPACING*3)
        for user in self.users.values():
            print(f"{user.id:<{self.FORMAT_SPACING}}{user.username:<{self.FORMAT_SPACING}}")
        print()

        print(f"{'Job ID':<{self.FORMAT_SPACING}}{'Priority':<{self.FORMAT_SPACING}}{'Shots':<{self.FORMAT_SPACING}}")
        print("-" * self.FORMAT_SPACING*4)
        for job in self.job_list:
            print(f"{job.id:<{self.FORMAT_SPACING}}{job.priority:<{self.FORMAT_SPACING}}", end="")
            print(f"{job.shots[0]}")
            for shot in job.shots[1:]:
                print(f"{"":<{self.FORMAT_SPACING*2}}{shot}")
        print()

    def run(self):

        print("Distributed Render Scheduler")

        self.workers.append(Worker(self.sched, self.curr_worker_id, 1))
        self.curr_worker_id += 1
        self.workers.append(Worker(self.sched, self.curr_worker_id, 0.8))
        self.curr_worker_id += 1
        self.workers.append(Worker(self.sched, self.curr_worker_id, 1.2))
        self.curr_worker_id += 1

        for worker in self.workers:
            worker.start()
            print(f"Worker {worker.id} online")

        while True:
            cmd = str(input(">> "))
            arg = cmd.split()

            if arg[0] in self.cmd_list:
                self.cmd_list[arg[0]](arg)
            else:
                print(cmd)

        # commands: run scheduler, add worker, status, submit job, cancel job, 

