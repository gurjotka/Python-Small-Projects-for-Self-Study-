# A Simple ToDo API using redis #

from fastapi import FastAPI
from schemas import TaskCreate

from database import tasks_db
from redis_client import redis_client

import json

app = FastAPI()

@app.get("/tasks")
def get_tasks():

    cached_tasks = redis_client.get("tasks")

    if cached_tasks:
        print("CACHE HIT 🔥")

        return json.loads(cached_tasks)
    print("DATABASE HIT 🗄️")

    redis_client.set(
        "tasks",
        json.dumps(tasks_db),
        ex=30 # expiry
    )

    return tasks_db

@app.post("/tasks")
def create_task(task: TaskCreate):

    new_task = {
        "id": len(tasks_db) + 1,
        "title": task.title
    }

    tasks_db.append(new_task)
    redis_client.delete("tasks")

    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    for task in tasks_db:
        if task["id"] == task_id:
            tasks_db.remove(task)

            redis_client.delete("tasks")

            return {
                "message": "Deleted"
            }

    return {
        "message": "Task not found"
    }