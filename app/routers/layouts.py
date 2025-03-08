from fastapi import APIRouter, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app import models, schemas
from app.db import get_db
from app.oauth2 import get_current_user
from app.util import get_password_hash


router = APIRouter(
    prefix="/layouts",
    tags=["layouts"],
)


@router.get("/")
async def read_layouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    layouts = db.query(models.Layouts).offset(skip).limit(limit).all()
    return layouts


@router.get("/{layout_id}")
async def read_layout(layout_id: int, db: Session = Depends(get_db)):
    layout = db.query(models.Layouts).filter(models.Layouts.id == layout_id).first()
    if layout is None:
        raise HTTPException(status_code=404, detail="Layout not found")
    return HTMLResponse(content=layout.html)


@router.post("/")
async def create_layout(layout: schemas.LayoutBase, db: Session = Depends(get_db)):
    db_layout = models.Layouts(name=layout.name, description=layout.description, html=layout.html, user_id=3)
    db.add(db_layout)
    db.commit()
    db.refresh(db_layout)
    return db_layout



