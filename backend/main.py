# from scheduler import Scheduler

def exit_prog():
    print("Turning off scheduler...")
    exit()
    

print("Distributed Render Scheduler")

arr = []
cmd_list = ["exit", ""]
while True:
    cmd = str(input(">> "))

    if cmd == "exit":
        exit_prog()
    else:
        print(cmd)

# commands: run scheduler, add worker, status, submit job, cancel job, 

