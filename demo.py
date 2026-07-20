from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

tasks = [
    {"id": 1, "title": "build", "done": True},
    {"id": 2, "title": "swim", "done": False},
    {"id": 3, "title": "eat", "done": True}
]


class Create(BaseModel):
    title: str


class Update(BaseModel):
    title: str | None = None
    done: bool | None = None


app = FastAPI()


@app.get("/")
def describe():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def check_status():
    return {"status": "ok"}


@app.get("/tasks")
def return_task():
    return tasks


@app.get("/tasks/{task_id}")
def move_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})


@app.post("/tasks", status_code=201)
def create_task(stuff: Create):
    if not stuff.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    new_id = len(tasks) + 1
    new_task = {
        "id": new_id,
        "title": stuff.title,
        "done": False
    }
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, stuff: Update):
    task = None
    for t in tasks:
        if t["id"] == task_id:
            task = t

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if stuff.title is not None and not stuff.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    if stuff.title is not None:
        task["title"] = stuff.title
    if stuff.done is not None:
        task["done"] = stuff.done

    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail="Task not found")


