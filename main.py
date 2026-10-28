from fastapi import FastAPI
from routes import todos, users, auth
from database import engine, Base
import models


app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(todos.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {"message": "hello world"}