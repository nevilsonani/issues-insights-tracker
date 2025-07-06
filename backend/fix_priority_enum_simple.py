#!/usr/bin/env python3
"""
Simple script to fix the priority enum in the database.
This ensures the database enum matches the expected values.
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_and_fix_priority_enum():
    """Check the current priority enum values and fix if needed."""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/issue_tracker")
    
    # Create database connection
    engine = create_engine(database_url)
    
    # Expected values from the model
    expected_values = ['BLOCKER', 'CRITICAL', 'MINOR', 'TRIVIAL']
    
    with engine.connect() as conn:
        # Check current enum values
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

if __name__ == "__main__":
    check_and_fix_priority_enum() 