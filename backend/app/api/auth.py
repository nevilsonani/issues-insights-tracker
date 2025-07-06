from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, Token
from app.crud.user import create_user, authenticate
from app.core.security import create_access_token
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if authenticate(db, user.email, user.password):
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = create_user(db, user)
    token = create_access_token({"user_id": new_user.id, "role": new_user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    auth_user = authenticate(db, user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": auth_user.id, "role": auth_user.role})
    return {"access_token": token, "token_type": "bearer"}
