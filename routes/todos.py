from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Todo, User
from schemas import TodoCreate, TodoResponse, TodoWithUserResponse, TodoDetailResponse, UserWithTodosResponse, TodoComplete
from dependencies import get_current_user

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("", status_code=201, response_model=TodoWithUserResponse)
# def create_todo(todo: TodoCreate, db:Session= Depends(get_db)):
#     user = db.query(User).filter(User.id == todo.user_id).first()
#     if user is None:
#         raise HTTPException(
#                     status_code=404,
#                     detail="User not found"
#                 )
#     new_todo = Todo(
#         title=todo.title,
#         description=todo.description,
#         user_id = todo.user_id
#     )

#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
#     return {
#         "todo": new_todo,
#         "user": user
#     }
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        user_id = current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return {
        "todo": new_todo,
        "user": current_user
    }
     
     
     

@router.get("", response_model= list[TodoDetailResponse])
def get_todos(db: Session = Depends(get_db)):
    todo = db.query(Todo).all()
    return todo

@router.get("/db/with-todos", response_model=list[UserWithTodosResponse])
def get_users_with_todos(db: Session = Depends(get_db)):
        users = db.query(User).all()
        return users

@router.get("/db/{user_id}/todos", response_model=list[TodoResponse])
def get_user_todos(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return user.todos


@router.patch("/{todo_id}/complete", response_model=TodoResponse)
def complete_todo(
    todo_id: int,
    data: TodoComplete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
     todo = db.query(Todo).filter(Todo.id== todo_id).first()
     if todo is None:
          raise HTTPException(
                      status_code=404,
                      detail="User not found"
                  )
     if todo.user_id != current_user.id:
          raise HTTPException(
                                status_code=403,
                                detail="Access denied"
                            )
     todo.completed = data.completed
     db.commit()
     db.refresh(todo)
     return todo

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
     todo = db.query(Todo).filter(Todo.id== todo_id).first()
     if todo is None:
               raise HTTPException(
                           status_code=404,
                           detail="User not found"
                       )
     if todo.user_id != current_user.id:
        raise HTTPException(
                                status_code=403,
                                detail="Access denied"
                            )
     db.delete(todo)
     db.commit()
     return {"message": "Todo deleted successfully"}