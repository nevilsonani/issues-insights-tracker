from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_db
from app.crud.user import get_users
from app.schemas.user import User, UserCreate, UserLogin

router = APIRouter()

@router.get("/", response_model=List[User])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)
