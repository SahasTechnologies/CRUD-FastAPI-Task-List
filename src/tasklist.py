from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json

app = FastAPI()

TASKS_FILE = "tasks.json"

class TaskBody(BaseModel):
    task: str


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)


@app.get("/tasks")
def get_tasks():
    return load_tasks()


@app.post("/tasks")
def add_task(body: TaskBody):
    tasks = load_tasks()

    new_id = 1 if len(tasks) == 0 else tasks[-1]["id"] + 1

    new_task = {
        "id": new_id,
        "task": body.task,
        "done": False
    }

    tasks.append(new_task)
    save_tasks(tasks)
    return new_task


@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return task

    raise HTTPException(status_code=404, detail="Task not found")
    # in case someone tries to game the server yk


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]

    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    save_tasks(new_tasks)
    return {"message": "Task deleted"}


def main():
    import uvicorn
    uvicorn.run(
        "CRUD-FastAPI-Task-List.main:app",
        host="127.0.0.1",
        port=8000
    )


if __name__ == "__main__":
    main()
