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

# get tasks
@app.get("/tasks")
async def get_tasks():
    tasks = load_tasks()
    return tasks

@app.post("/tasks")
def add_task(body: TaskBody):
    tasks = load_tasks()

    # get an id
    new_id = 1 if len(tasks) == 0 else tasks[-1]["id"] + 1

    new_task = {
        "id": new_id,
        "task": body.task,
        "done": False
    }

    tasks.append(new_task)
    save_tasks(tasks)

    return new_task


