#!/usr/bin/env python3
"""
Script to fix the priority enum in the database.
This version tries multiple database connection methods.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

def try_database_connections():
    """Try different database connection methods."""
    
    # Common database URLs to try
    possible_urls = [
        # Docker setup
        "postgresql://user:password@localhost:5432/tracker",
        "postgresql://postgres:password@localhost:5432/issue_tracker",
        "postgresql://postgres:postgres@localhost:5432/postgres",
        
        # Local PostgreSQL common setups
        "postgresql://postgres:admin@localhost:5432/postgres",
        "postgresql://postgres:root@localhost:5432/postgres",
        "postgresql://localhost:5432/postgres",
    ]
    
    # Also try environment variable
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        possible_urls.insert(0, env_url)
    
    for url in possible_urls:
        print(f"Trying database URL: {url}")
        try:
            engine = create_engine(url)
            with engine.connect() as conn:
                # Test the connection
                result = conn.execute(text("SELECT 1"))
                print(f"✅ Successfully connected to database!")
                return engine, url
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}...")
            continue
    
    return None, None

def check_and_fix_priority_enum():
    """Check the current priority enum values and fix if needed."""
    
    # Try to connect to database
    engine, url = try_database_connections()
    
    if not engine:
        print("\n❌ Could not connect to any database!")
        print("\nTo fix this, you need to:")
        print("1. Start Docker Desktop and run: docker-compose up db -d")
        print("2. OR install PostgreSQL locally and create a database")
        print("3. OR update the DATABASE_URL environment variable")
        return
    
    print(f"\n✅ Connected to: {url}")
    
    # Expected values from the model
    expected_values = ['BLOCKER', 'CRITICAL', 'MINOR', 'TRIVIAL']
    
    with engine.connect() as conn:
        try:
            # Check if the priority enum exists
            result = conn.execute(text("SELECT unnest(enum_range(NULL::priority))"))
            current_values = [row[0] for row in result]
            print(f"Current priority enum values in database: {current_values}")
            print(f"Expected priority enum values: {expected_values}")
            
            if set(current_values) == set(expected_values):
                print("✅ Priority enum is already correct!")
                return
            
            print("❌ Priority enum mismatch detected. Fixing...")
            
            # Check if there are any issues with MINOR priority
            result = conn.execute(text("SELECT COUNT(*) FROM issues WHERE priority = 'MINOR'"))
            minor_count = result.scalar()
            print(f"Found {minor_count} issues with MINOR priority")
            
            if minor_count > 0:
                print("⚠️  There are existing issues with MINOR priority. Updating them to TRIVIAL...")
                conn.execute(text("UPDATE issues SET priority = 'TRIVIAL' WHERE priority = 'MINOR'"))
                conn.commit()
            
            # Drop and recreate the enum
            print("Dropping and recreating priority enum...")
            
            # Drop the column constraint first
            conn.execute(text("ALTER TABLE issues ALTER COLUMN priority DROP DEFAULT"))
            
            # Drop the enum type
            conn.execute(text("DROP TYPE priority"))
            
            # Recreate the enum with all values
            enum_values = "', '".join(expected_values)
            conn.execute(text(f"CREATE TYPE priority AS ENUM ('{enum_values}')"))
            
            # Alter the column to use the new enum type
            conn.execute(text("ALTER TABLE issues ALTER COLUMN priority TYPE priority USING priority::text::priority"))
            
            # Restore the default
            conn.execute(text("ALTER TABLE issues ALTER COLUMN priority SET DEFAULT 'MINOR'"))
            
            conn.commit()
            
            # Verify the fix
            result = conn.execute(text("SELECT unnest(enum_range(NULL::priority))"))
            new_values = [row[0] for row in result]
            print(f"✅ New priority enum values: {new_values}")
            
            if set(new_values) == set(expected_values):
                print("✅ Priority enum has been successfully fixed!")
            else:
                print("❌ Failed to fix priority enum!")
                
        except Exception as e:
            print(f"❌ Error during enum fix: {str(e)}")
            print("\nThis might mean:")
            print("1. The database doesn't exist yet")
            print("2. The issues table doesn't exist yet")
            print("3. You need to run migrations first")

if __name__ == "__main__":
    check_and_fix_priority_enum() 