#!/usr/bin/env python3
"""
Database initialization script
Creates tables and admin user for development
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import SessionLocal
from app.db.init_db import init_admin
from app.db.base import Base
from app.db.session import engine

def init_database():
    """Initialize database tables and create admin user"""
    print("🔧 Initializing database...")
    
    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False
    
    # Create admin user
    try:
        db = SessionLocal()
        init_admin(db)
        db.close()
        print("✅ Database initialization completed")
        return True
    except Exception as e:
        print(f"❌ Failed to create admin user: {e}")
        return False

if __name__ == "__main__":
    success = init_database()
    if success:
        print("\n🎉 Database is ready!")
        print("📧 Admin credentials:")
        print("   Email: admin@example.com")
        print("   Password: admin123")
    else:
        print("\n❌ Database initialization failed")
        sys.exit(1) 