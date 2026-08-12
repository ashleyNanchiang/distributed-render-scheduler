# High Level:
User -> Interface -> 

# Job
 + job_id
 + job_type
 + job_state
 + user_id
 + shots
 + priority

# Task
 + task_id
 + task_type
 + task_state
 + user_id
 + shots
 + priority

# User
 + user_id
 + user_name
 + username
 + password
 + history

# Worker
 + worker_id
 + worker_status
 + task_list

# State
 + pending
 + in_progress
 + completed
 + failed
 + paused
 + terminated

 # Worker Status
  + starting
  + idle
  + working
  + sleeping
  + off

 # Priority
  + 1
  + 2
  + 3

 # Flow
  1. user submits a job
  2. API creates a job record and store in a table
  3. the scheduler grabs the job details from the table (check for new jobs)
  4. the scheduler split a job into multiple tasks
  5. the workers report to scheduler for tasks when they are idle
  6. the scheduler assigns tasks
  7. the workers report back after the task is finished
  8. the scheduler make sure all tasks are done for a job to be completed
  ** worker registers with shceduler when it starts