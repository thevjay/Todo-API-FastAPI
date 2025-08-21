from fastapi import FastAPI,Depends
from pydantic import BaseModel
from typing import Optional
import os
from models import TodoModel
from sqlalchemy.orm import Session
from database import engine, Sessionlocal
from dotenv import load_dotenv
load_dotenv()

print(os.getenv('FOO'))
app = FastAPI() # Create an instance of FastAPI

TodoModel.metadata.create_all(bind=engine) # Create the table in the database
# The app instance is the main companent of our FastAPI application. It is used to configure the application

# /ping is the path of the endpoint

# class Custom(BaseModel):
#     name: str
#     age: int

# @app.get("/ping")
# async def root():
#     return {"message":"Hello World"}

# @app.get("/")
# async def root():
#     return {"message":"Welcome"}

# @app.post ("/blogs/{blog_id}")
# async def read_blog(blog_id: int, request_body: Custom ,q: str = None, name: str = ''):
#     print(request_body)
#     print(q,name)
#     return {"blog_id":blog_id} 
 
# TODO:
# todos = []  # Create an empty list to store todos, in memory db 

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int

class Config:
    orm_mode = True


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/todos",response_model=list[TodoResponse])
def get_todos(db: Session=Depends(get_db)):
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}",response_model=TodoResponse)
def get_todo(todo_id: int,db: Session=Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    return todo

@app.post("/todos",response_model=TodoResponse)
def create_todo(todo:TodoBase,db: Session = Depends(get_db)):
    db_todo = TodoModel(title=todo.title,description=todo.description,completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int):
#     for todo in todos:
#         if todo['id'] == todo_id:
#             todos.remove(todo)
#             return {"message":"Todo deleted successfully"}
#     return {"error":"Todo not found"}

@app.delete("/todos/{todo_id}",response_model=TodoResponse)
def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    db.delete(todo)
    db.commit()
    return todo