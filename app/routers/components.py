from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.oauth2 import get_current_user
from app.util import get_password_hash


router = APIRouter(
    prefix="/components",
    tags=["components"],
)


@router.get("/")
async def read_components(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    components = db.query(models.Components).offset(skip).limit(limit).all()
    return components


@router.get("/{component_id}")
async def read_component(component_id: int, db: Session = Depends(get_db)):
    component = db.query(models.Components).filter(models.Components.id == component_id).first()
    if component is None:
        raise HTTPException(status_code=404, detail="Component not found")
    return component



@router.post("/")
async def create_component(component: schemas.ComponentBase, db: Session = Depends(get_db), user: schemas.User = Depends(get_current_user)):
    db_component = models.Components(description=component.description, html=component.html, user_id=user.id)
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    print(db_component)
    component = db.query(models.Components).filter(models.Components.id == db_component.id).first()
    return component


@router.get("/user/{user_id}")
async def read_user_components(user_id: int, db: Session = Depends(get_db)):
    components = db.query(models.Components).filter(models.Components.user_id == user_id).all()
    return components