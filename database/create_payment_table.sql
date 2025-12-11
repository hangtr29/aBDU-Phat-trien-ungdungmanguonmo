-- Tạo bảng thanh_toan
CREATE TABLE IF NOT EXISTS thanh_toan (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    khoa_hoc_id INTEGER NOT NULL REFERENCES khoa_hoc(id) ON DELETE CASCADE,
    so_tien NUMERIC(10, 2) NOT NULL,
    phuong_thuc VARCHAR(50) NOT NULL,  -- momo, zalopay, paypal, bank_transfer
    trang_thai VARCHAR(50) NOT NULL DEFAULT 'pending',  -- pending, processing, completed, failed, cancelled
    ma_giao_dich VARCHAR(100) UNIQUE,
    ma_don_hang VARCHAR(100) UNIQUE NOT NULL,
    thong_tin_them TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ngay_thanh_toan TIMESTAMP WITH TIME ZONE
);

-- Index để query nhanh
CREATE INDEX IF NOT EXISTS idx_thanh_toan_user_id ON thanh_toan(user_id);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_khoa_hoc_id ON thanh_toan(khoa_hoc_id);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_trang_thai ON thanh_toan(trang_thai);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_ma_don_hang ON thanh_toan(ma_don_hang);
CREATE INDEX IF NOT EXISTS idx_thanh_toan_ma_giao_dich ON thanh_toan(ma_giao_dich);

