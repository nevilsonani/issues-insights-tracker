from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.db.session import SessionLocal
from app.models.user import User, Role
from app.schemas.user import TokenData
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud.user import get_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user
