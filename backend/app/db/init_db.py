from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User, Role

def init_admin(db: Session):
    admin_email = "admin@example.com"
    user = db.query(User).filter(User.email == admin_email).first()
    if not user:
        admin = User(
            email=admin_email,
            full_name="Admin",
            hashed_password=get_password_hash("admin123"),
            role=Role.ADMIN
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created.")
    else:
        print("ℹ️ Admin user already exists.")
