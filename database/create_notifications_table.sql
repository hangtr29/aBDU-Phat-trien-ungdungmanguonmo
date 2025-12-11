-- Tạo bảng thông báo
CREATE TABLE IF NOT EXISTS thong_bao (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    loai VARCHAR(50) NOT NULL,  -- submission, discussion, grade, course, etc.
    tieu_de VARCHAR(200) NOT NULL,
    noi_dung TEXT,
    link VARCHAR(500),
    da_doc BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index để query nhanh
CREATE INDEX IF NOT EXISTS idx_thong_bao_user_id ON thong_bao(user_id);
CREATE INDEX IF NOT EXISTS idx_thong_bao_da_doc ON thong_bao(da_doc);
CREATE INDEX IF NOT EXISTS idx_thong_bao_created_at ON thong_bao(created_at DESC);

