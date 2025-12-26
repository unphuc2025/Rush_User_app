-- Migration Script: Rename venue_id to court_id in bookings table
-- Run this on your PostgreSQL database

-- Step 1: Rename the column
ALTER TABLE bookings 
RENAME COLUMN venue_id TO court_id;

-- Step 2: Verify the change
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'bookings' 
AND column_name = 'court_id';

-- Expected output: court_id | character varying(36)
