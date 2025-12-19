-- Tạo bảng thời khóa biểu học
CREATE TABLE IF NOT EXISTS thoi_khoa_bieu (
    id SERIAL PRIMARY KEY,
    khoa_hoc_id INTEGER NOT NULL REFERENCES khoa_hoc(id) ON DELETE CASCADE,
    tieu_de VARCHAR(200) NOT NULL,
    mo_ta TEXT,
    ngay_hoc TIMESTAMP WITH TIME ZONE NOT NULL,
    thoi_gian_bat_dau VARCHAR(10),
    thoi_gian_ket_thuc VARCHAR(10),
    link_google_meet VARCHAR(500),
    link_zoom VARCHAR(500),
    link_khac VARCHAR(500),
    ghi_chu TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tạo index để tìm kiếm nhanh
CREATE INDEX IF NOT EXISTS idx_thoi_khoa_bieu_khoa_hoc_id ON thoi_khoa_bieu(khoa_hoc_id);
CREATE INDEX IF NOT EXISTS idx_thoi_khoa_bieu_ngay_hoc ON thoi_khoa_bieu(ngay_hoc);

-- Comment cho các cột
COMMENT ON TABLE thoi_khoa_bieu IS 'Thời khóa biểu học - Giáo viên tạo lịch học cho khóa học';
COMMENT ON COLUMN thoi_khoa_bieu.ngay_hoc IS 'Ngày giờ học (bao gồm cả ngày và giờ)';
COMMENT ON COLUMN thoi_khoa_bieu.thoi_gian_bat_dau IS 'Giờ bắt đầu (format: HH:MM)';
COMMENT ON COLUMN thoi_khoa_bieu.thoi_gian_ket_thuc IS 'Giờ kết thúc (format: HH:MM)';
COMMENT ON COLUMN thoi_khoa_bieu.is_completed IS 'Đánh dấu buổi học đã hoàn thành';

