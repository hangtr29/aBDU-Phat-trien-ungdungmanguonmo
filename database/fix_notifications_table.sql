-- Kiểm tra và thêm các cột còn thiếu
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS user_id INTEGER;
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS loai VARCHAR(50);
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS tieu_de VARCHAR(200);
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS noi_dung TEXT;
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS link VARCHAR(500);
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS da_doc BOOLEAN DEFAULT FALSE;
ALTER TABLE thong_bao ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP;

-- Thêm foreign key nếu chưa có
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'thong_bao_user_id_fkey'
    ) THEN
        ALTER TABLE thong_bao 
        ADD CONSTRAINT thong_bao_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
    END IF;
END $$;

-- Tạo index nếu chưa có
CREATE INDEX IF NOT EXISTS idx_thong_bao_user_id ON thong_bao(user_id);
CREATE INDEX IF NOT EXISTS idx_thong_bao_da_doc ON thong_bao(da_doc);
CREATE INDEX IF NOT EXISTS idx_thong_bao_created_at ON thong_bao(created_at DESC);

