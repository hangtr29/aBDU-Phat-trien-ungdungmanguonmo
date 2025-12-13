-- Migration: Thêm cột so_du (số dư ví) vào bảng users
-- Chạy: psql -U elearn -d elearning -f database/add_user_balance.sql

-- Thêm cột so_du nếu chưa có
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'so_du'
    ) THEN
        ALTER TABLE users ADD COLUMN so_du NUMERIC(12, 2) DEFAULT 0 NOT NULL;
        COMMENT ON COLUMN users.so_du IS 'Số dư ví của người dùng (VNĐ)';
    END IF;
END $$;

