from fastapi import APIRouter, HTTPException
from database import users
from schemas import UserCreate, UserResponse, UpdateUser
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/db", status_code=201, response_model=UserResponse)
def post_user_db(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/db", response_model=list[UserResponse])
def get_user_db(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/db/{user_id}", response_model=UserResponse)
def get_user_by_id_db(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/db/{user_id}", response_model=UserResponse)
def update_user_db(
    user_id: int,
    updated_user: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
    user.name = updated_user.name
    user.email = updated_user.email
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/db/{user_id}")
def delete_user_db(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
                status_code=404,
                detail="User not found"
            )
    db.delete(user)
    db.commit()
    users = db.query(User).all()
    return {"message" : "user deleted", "current users":users}


@router.patch("/db/{user_id}", response_model=UserResponse)
def patch_user_db(
    user_id: int,
    updated_user: UpdateUser,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
            raise HTTPException(
                    status_code=404,
                    detail="User not found"
                )
    update_data = updated_user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    return user

    


#####################################################################


# Get all users
@router.get("")
def get_users():
    return users


# Search user by name
@router.get("/search")
def search_by_name(name: str = None):
    if name:
        username = name.lower()

        for i in users:
            if username == i["name"].lower():
                return i

    return "no data found"


# Get user by ID
@router.get("/{user_id}")
def get_user_by_id(user_id: int):
    for i in users:
        if user_id == i["id"]:
            return i

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# Create user
@router.post("", status_code=201, response_model=UserResponse)
def post_user(user: UserCreate):
    new_user = user.model_dump()

    allId = []

    for i in users:
        allId.append(i["id"])

    if allId:
        new_user["id"] = max(allId) + 1
    else:
        new_user["id"] = 1

    users.append(new_user)

    return new_user


# Delete user
@router.delete("/{user_id}")
def delete_user(user_id: int):
    for i in users:
        if i["id"] == user_id:
            users.remove(i)
            return users

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# Full update
@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate):
    for i in users:
        if i["id"] == user_id:
            i["name"] = user.name
            i["email"] = user.email

            return i

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# Partial update
@router.patch("/{user_id}")
def patch_user(user: UpdateUser, user_id: int):
    update_data = user.model_dump(exclude_unset=True)

    for i in users:
        if i["id"] == user_id:
            i.update(update_data)
            return i

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )