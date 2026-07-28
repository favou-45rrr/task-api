
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3

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

conn = sqlite3.connect("tasks.db",check_same_thread=False)

c = conn.cursor()

c.execute("""CREATE TABLE if not exists tasks (
        id integer PRIMARY KEY,
        title text,
        done bool
    )""")
conn.commit()
c.execute("SELECT COUNT (*) FROM tasks")
count = c.fetchone()[0]
if count == 0:
    c.execute("INSERT INTO tasks (title, done) VALUES ('build',1)")
    c.execute("INSERT INTO tasks (title, done) VALUES ('swim', 0)")
    c.execute("INSERT INTO tasks (title, done) VALUES ('eat', 1)")
conn.commit()



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
    c.execute("SELECT * FROM tasks")
    all = c.fetchall()
    return all



@app.get("/tasks/{task_id}")
def move_task(task_id: int):
    c.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    one = c.fetchone()
    if one is None:
        return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
    return one


@app.post("/tasks", status_code=201)
def create_task(stuff: Create):
    if not stuff.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    c.execute("INSERT INTO tasks (title,done) VALUES (?,?)",(stuff.title,0))
    new_id = c.lastrowid
    conn.commit()
    return {"id":new_id,"title":stuff.title,"done":False}



@app.put("/tasks/{task_id}")
def update_task(task_id: int, stuff: Update):
    c.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    one = c.fetchone()
    if one is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    if stuff.title is not None and not stuff.title.strip():
       raise HTTPException(status_code=400, detail="Title cannot be empty")
    
    if stuff.title is not None:
        final_title = stuff.title
    else:
        final_title = one[1] 
    if stuff.done is not None:
        final_done = stuff.done
    else:
        final_done = one[2]
    c.execute("UPDATE tasks SET title = ?, done = ? WHERE id = ?",(final_title,final_done,task_id))
    conn.commit()
    return{"id":task_id,"title":final_title,"done":final_done}



@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    c.execute("SELECT * FROM tasks WHERE id = ?",(task_id,))
    one = c.fetchone()
    if one is None:
        raise HTTPException(status_code=404, detail="Task not found")
    c.execute("DELETE FROM tasks WHERE id = ?",(task_id,))
    conn.commit()
    return Response(status_code=204)


