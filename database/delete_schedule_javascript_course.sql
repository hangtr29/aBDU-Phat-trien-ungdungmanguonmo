-- Xóa tất cả thời khóa biểu của khóa học "JavaScript Full Stack - React & Node.js"

-- Tìm ID của khóa học
DO $$
DECLARE
    v_course_id INTEGER;
    v_deleted_count INTEGER;
BEGIN
    -- Tìm ID khóa học
    SELECT id INTO v_course_id 
    FROM khoa_hoc 
    WHERE tieu_de LIKE '%JavaScript Full Stack%' 
       OR tieu_de LIKE '%React & Node.js%'
    LIMIT 1;
    
    IF v_course_id IS NOT NULL THEN
        -- Xóa tất cả thời khóa biểu của khóa học này
        DELETE FROM thoi_khoa_bieu 
        WHERE khoa_hoc_id = v_course_id;
        
        GET DIAGNOSTICS v_deleted_count = ROW_COUNT;
        
        RAISE NOTICE 'Đã xóa % thời khóa biểu của khóa học ID: % (JavaScript Full Stack)', v_deleted_count, v_course_id;
    ELSE
        RAISE NOTICE 'Không tìm thấy khóa học "JavaScript Full Stack - React & Node.js"';
    END IF;
END $$;

-- Kiểm tra kết quả
SELECT 
    tkb.id,
    tkb.tieu_de,
    tkb.ngay_hoc,
    kh.tieu_de as khoa_hoc
FROM thoi_khoa_bieu tkb
JOIN khoa_hoc kh ON tkb.khoa_hoc_id = kh.id
WHERE kh.tieu_de LIKE '%JavaScript Full Stack%' 
   OR kh.tieu_de LIKE '%React & Node.js%';

