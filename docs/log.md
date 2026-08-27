### 2026-8-15:
 - Started a log. I'm currently working on heartbeat for the workers.

### 2026-8-21:
 - Revisit how the scheduler track tasks. Will use a master list for all task objects, a list for pending tasks (not yet assigned) and a list for assigned tasks. This should allow me to keep track of which worker is doing what task, and if a task fails this allows the scheduler to know which task it is and reassign.
 - Continue to work on track_heartbeat in scheduler

### 2026-8-24:
 - Notes on threads:
    - worker: one thread executes tasks, one thread sends periodic heartbeats
       - worker calls scheduler methods to receive and finish tasks (will change in the future)
    - scheduler: just one thread that's in a loop that checks timeouts of the workers
 - Finished track_heartbeats() in Scheduler, added finish_task() and terminate_task()

### 2026-8-25
 - How command line interface mode works:
    - after start up, user can submit jobs and add users
    - then the "start" command will start the scheduler
    - the scheduler will run until all the jobs are done
    - then the control goes bac kto the user to submit more jobs
 - Added a random factor to the worker execution time to make it a bit more realistic