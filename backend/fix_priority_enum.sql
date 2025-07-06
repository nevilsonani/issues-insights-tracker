-- SQL script to fix the priority enum in the database
-- This ensures the database enum matches the SQLAlchemy model

-- First, check current enum values
SELECT unnest(enum_range(NULL::priority)) as current_priority_values;

-- Check if there are any issues with MINOR priority
SELECT COUNT(*) as minor_issues_count FROM issues WHERE priority = 'MINOR';

-- If there are issues with MINOR priority, update them to TRIVIAL first
UPDATE issues SET priority = 'TRIVIAL' WHERE priority = 'MINOR';

-- Drop the column default constraint
ALTER TABLE issues ALTER COLUMN priority DROP DEFAULT;

-- Drop the enum type (this will fail if there are other columns using it)
DROP TYPE priority;

-- Recreate the enum with all the correct values
CREATE TYPE priority AS ENUM ('BLOCKER', 'CRITICAL', 'MINOR', 'TRIVIAL');

-- Alter the column to use the new enum type
ALTER TABLE issues ALTER COLUMN priority TYPE priority USING priority::text::priority;

-- Restore the default value
ALTER TABLE issues ALTER COLUMN priority SET DEFAULT 'MINOR';

-- Verify the fix
SELECT unnest(enum_range(NULL::priority)) as new_priority_values; 