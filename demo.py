from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import conn

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
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        result = cur.fetchone()
        if result is None:
            return JSONResponse(status_code=500, content={"status": "error"})
        return {"status": "ok","db": "ok"}

@app.get("/tasks")
def return_task(search: str | None = None,done: bool | None = None):
    with conn.cursor() as cur:
        if search is not None :
            pattern = f"%{search}%"
            cur.execute("SELECT * FROM tasks WHERE title LIKE %s ORDER BY title",(pattern,))
            one = cur.fetchall()
            return one
        if done is not None:
            cur.execute("SELECT * FROM tasks WHERE done = %s ORDER BY title",(done,))
            one = cur.fetchall()
            return one
        else:
            cur.execute("SELECT * FROM tasks ORDER BY title")
            all = cur.fetchall()
            return all 

@app.get("/tasks/{task_id}")
def move_task(task_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE id = %s",(task_id,))
        one = cur.fetchone()
        if one is None:
            return JSONResponse(status_code=404, content={"error": f"Task {task_id} not found"})
        return one

@app.get("/stats")
def count():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM tasks")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE done = True ")
        completed = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM tasks WHERE done = False ")
        incompleted = cur.fetchone()[0]
        return {
            "total": total,
            "completed": completed,
            "incomplete": incompleted
            }

@app.post("/tasks", status_code=201)
def create_task(stuff: Create):
    if not stuff.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    with conn.cursor() as cur:
        cur.execute("INSERT INTO tasks (title,done) VALUES (%s,%s) RETURNING id",(stuff.title,False))
        new_id = cur.fetchone()[0]
        conn.commit()
        return {"id":new_id,"title":stuff.title,"done":False}






@app.put("/tasks/{task_id}")
def update_task(task_id: int, stuff: Update):
    with conn.cursor() as cur:

        cur.execute("SELECT * FROM tasks WHERE id = %s",(task_id,))
        one = cur.fetchone()
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
        cur.execute("UPDATE tasks SET title = %s, done = %s WHERE id = %s",(final_title,final_done,task_id))
        conn.commit()
        return{"id":task_id,"title":final_title,"done":final_done}



@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE id = %s",(task_id,))
        one = cur.fetchone()
        if one is None:
            raise HTTPException(status_code=404, detail="Task not found")
        cur.execute("DELETE FROM tasks WHERE id = %s",(task_id,))
        conn.commit()
        return Response(status_code=204)


