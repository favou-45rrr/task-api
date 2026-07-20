from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class TaskCreate(BaseModel):
    title:str


tasks = [
    {
        "id": 1,
        "title": "Learn FastAPI",
        "done": False
    },
    {
        "id": 2,
        "title": "Build a CRUD API",
        "done": False
    },

    {
        "id": 3,
        "title": "learn Python",
        "done": True
    } 
 ]

@app.get("/")
def describe():
    return{ "name": "Task API",
            "version": "1.0", 
            "endpoints": ["/tasks"]}

@app.get("/health")
def check_status():
    return{
        "status": "ok"
    }

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return {"error": "Task 99 not found"}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    new_id = len(tasks) + 1  # simple for now, we'll improve this later
    new_task = {
        "id": new_id,
        "title": task.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task

