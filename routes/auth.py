from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserRegister, UserResponse, UserLogin
from security import hash_password, verify_password

from security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", status_code=201, response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    email = db.query(User).filter(User.email == user.email).first()

    if email:
        raise HTTPException(
                    status_code=409,
                    detail="user already registered"
                )

    hash_pw = hash_password(user.password)
    new_user = User(
            name=user.name,
            email=user.email,
            hashed_password = hash_pw
            )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == credentials.email
    ).first()

    if user is None or user.hashed_password is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    is_password_verified = verify_password(
        credentials.password,
        user.hashed_password
    )

    if not is_password_verified:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token =create_access_token(user.id)
    return {"access_token": token,
            "token_type": "bearer"}