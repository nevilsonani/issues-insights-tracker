#!/usr/bin/env python3
"""
Script to fix the priority enum in the database using the correct connection from config.
"""

import os
import sys
from sqlalchemy import create_engine, text

def check_and_fix_priority_enum():
    """Check the current priority enum values and fix if needed."""
    
    # Use the exact same database connection as the backend
    database_url = "postgresql://postgres:281003@localhost:5432/tracker"
    
    print(f"Connecting to database: {database_url}")
    
    try:
        # Create database connection
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Test connection
            result = conn.execute(text("SELECT 1"))
            print("✅ Successfully connected to database!")
            
            # Expected values from the model
            expected_values = ['BLOCKER', 'CRITICAL', 'MINOR', 'TRIVIAL']
            
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
                
                # Drop and recreate the enum
                print("Dropping and recreating priority enum...")
                
                # Drop the column constraint first
                conn.execute(text("ALTER TABLE issues ALTER COLUMN priority DROP DEFAULT"))
                
                # Convert the column to text first to remove the enum dependency
                conn.execute(text("ALTER TABLE issues ALTER COLUMN priority TYPE text"))
                
                # Drop the enum type
                conn.execute(text("DROP TYPE priority"))
                
                # Recreate the enum with all values
                enum_values = "', '".join(expected_values)
                conn.execute(text(f"CREATE TYPE priority AS ENUM ('{enum_values}')"))
                
                # Alter the column to use the new enum type
                conn.execute(text("ALTER TABLE issues ALTER COLUMN priority TYPE priority USING priority::priority"))
                
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
                
    except Exception as e:
        print(f"❌ Failed to connect to database: {str(e)}")
        print("\nTo fix this:")
        print("1. Make sure PostgreSQL is running on localhost:5432")
        print("2. Make sure the database 'tracker' exists")
        print("3. Make sure user 'postgres' with password '281003' can connect")
        print("4. Or update the database connection in app/core/config.py")

if __name__ == "__main__":
    check_and_fix_priority_enum() 