import os
from fastapi import FastAPI, HTTPException
from pymongo import AsyncMongoClient
from bson import ObjectId
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import app.settings as settings

app = FastAPI()
client = AsyncMongoClient(os.getenv("MONGO_URI"))
db = client.myproject
todos = db.todos
users = db.users
general = db.general

# CORS, Т.к. порты разные, чтобы не было проблем в браузере
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # или ["*"] для разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Todo(BaseModel):
    title: str
    complexity: str
    done: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    complexity: str | None = None
    done: bool | None = None

class RegisterData(BaseModel):
    username: str
    email: str
    password: str

@app.get("/todos")
async def list_todos():
    items = await todos.find().to_list(10)
    for i in items:
        i["_id"] = str(i["_id"])
        i["crystals"] = settings.CRYSTALS_BY_COMPLEXITY[i["complexity"]]
    return items

@app.post("/todos")
async def create_todo(todo: Todo):
    result = await todos.insert_one(todo.dict())
    return {
        "id": str(result.inserted_id),
        **todo.dict()
    }

# @app.put("/todos/{todo_id}")
# async def update_todo(todo: Todo, todo_id: str):
#     result = await todos.update_one(
#         {"_id": ObjectId(todo_id)},
#         {"$set": todo.model_dump()}
#     )

#     if result.matched_count == 0:
#         raise HTTPException(404, "Not found")

#     return {"ok": True}

@app.patch("/todos/{todo_id}")
async def update_status(todo: TodoUpdate, todo_id: str):
    result = await todos.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": todo.model_dump(exclude_unset=True)}
    )

    if result.matched_count == 0:
        raise HTTPException(404, "Not found")

    item = await todos.find_one({"_id": ObjectId(todo_id)})
    count = settings.CRYSTALS_BY_COMPLEXITY[item["complexity"]] if item["done"] else -1
    print("count: ")
    print(count)
    return {"ok": True}

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    res = await todos.delete_one({"_id": ObjectId(todo_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Not found")
    return {"ok": True}

@app.post("/auth/register")
async def register(data: RegisterData):

    result = await users.insert_one({
        "username": data.username,
        "email": data.email,
        "password": data.password,
    })

    return {
        "id": str(result.inserted_id),
        "username": data.username,
        "email": data.email,
    }