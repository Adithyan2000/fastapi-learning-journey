from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import event


DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

users = [
  { "id": 1, 
   "name": "John",
    "email":"john@123" },
  { "id": 2, 
   "name": "Mike",
    "email": "mike@123" }
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
