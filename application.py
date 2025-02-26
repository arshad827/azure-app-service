from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import logging
from fastapi import FastAPI

app = FastAPI(title="To-Do API", description="A simple To-Do API using FastAPI", version="1.0", tags=["todos"])
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Model for To-Do items
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

# In-memory storage
todos = []
todo_router = APIRouter(prefix="/todos", tags=["Todos"])

@todo_router.post('/todos/', response_model=Todo)
def create_todo(todo: Todo):
    todos.append(todo)
    return todo


@todo_router.get("/", response_model=List[Todo])
def get_todos():
    logging.info("Root endpoint was accessed", extra={"todos": todos})    
    print(todos)
    return todos


@todo_router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@todo_router.delete("/{todo_id}", response_model=Todo)
def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            return todos.pop(index)
    raise HTTPException(status_code=404, detail="Todo not found")

app.include_router(todo_router)
