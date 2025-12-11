-- Thêm cột diem_toi_da vào bảng bai_tap
ALTER TABLE bai_tap
ADD COLUMN IF NOT EXISTS diem_toi_da NUMERIC(5, 2) DEFAULT 10.0;

-- Cập nhật các bản ghi hiện có nếu NULL
UPDATE bai_tap
SET diem_toi_da = 10.0
WHERE diem_toi_da IS NULL;

