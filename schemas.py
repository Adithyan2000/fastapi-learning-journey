from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UpdateUser(BaseModel):
    name: str | None = None
    email: str | None = None

######################################################################
class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    # user_id: int   #for secure todo creation we dont need to provide userid from fronend backend finds out the user id


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    user_id: int

class TodoWithUserResponse(BaseModel):
    todo: TodoResponse
    user: UserResponse

class TodoDetailResponse(TodoResponse):
    user: UserResponse

class UserWithTodosResponse(UserResponse):
    todos: list[TodoResponse]

class TodoComplete(BaseModel):
    completed: bool

######################################################################

class UserRegister(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str