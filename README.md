# Task API

## Why SQLite
Before, task data was stored in a Python list, so everything disappeared 
every time the server restarted — nothing was saved. Now, with SQLite, 
tasks are stored in a tasks.db file that persists across restarts. I 
picked SQLite over other databases because it's lightweight — no server 
to install, no account to set up, it's just a file.

## Database location
tasks.db is created automatically,it's not in the file itself, since it's git-ignored, so it won't be included when someone clones the repo. when the app is ran for the first time the file get filled with the 3 seed tasks

## How to run
```
pip install -r requirements.txt
uvicorn demo:app --reload
```


## Example query (Stage 4)
```sql
SELECT * FROM tasks WHERE done = 1;
```
This query returns all the tasks in the tasks table whose `done` status is completed.

## Database screenshot
![Database in DB Browser](task_img.png)