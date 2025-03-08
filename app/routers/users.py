from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.oauth2 import get_current_user
from app.util import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, name=user.name, password=hashed_password, profile_pic=user.profile_pic)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = schemas.UserOut(**user.__dict__)
    return user


@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user
