-- Migration: Them cot so_du (so du vi) vao bang users
-- Chay: psql -U elearn -d elearning -f database/add_user_balance.sql

-- Them cot so_du neu chua co
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'so_du'
    ) THEN
        ALTER TABLE users ADD COLUMN so_du NUMERIC(12, 2) DEFAULT 0 NOT NULL;
        COMMENT ON COLUMN users.so_du IS 'So du vi cua nguoi dung (VND)';
    END IF;
END $$;

