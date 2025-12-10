-- Seed data cho khóa học lập trình
-- Xóa dữ liệu cũ (nếu có)
TRUNCATE TABLE chi_tiet_khoa_hoc CASCADE;
TRUNCATE TABLE khoa_hoc CASCADE;

-- Reset sequence
ALTER SEQUENCE IF EXISTS khoa_hoc_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS chi_tiet_khoa_hoc_id_seq RESTART WITH 1;

-- Tạo giáo viên mẫu (nếu chưa có) - password: teacher123
INSERT INTO users (email, password_hash, ho_ten, vai_tro, so_dien_thoai)
VALUES 
    ('teacher1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5Z5Z5u', 'Nguyễn Văn Giảng', 'teacher', '0901234567'),
    ('teacher2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJqZ5Z5Z5u', 'Trần Thị Code', 'teacher', '0901234568')
ON CONFLICT (email) DO NOTHING;

-- Khóa học 1: Python Cơ Bản
INSERT INTO khoa_hoc (tieu_de, mo_ta, cap_do, hinh_anh, gia, gia_goc, so_buoi, thoi_luong, hinh_thuc, teacher_id, trang_thai)
VALUES (
    'Python Cơ Bản - Từ Zero đến Hero',
    'Khóa học Python toàn diện cho người mới bắt đầu. Học từ cú pháp cơ bản đến xây dựng ứng dụng thực tế. Bao gồm: biến, hàm, OOP, xử lý file, API, và nhiều hơn nữa.',
    'Beginner',
    'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=800',
    1990000,
    2990000,
    20,
    '40 giờ',
    'online',
    (SELECT id FROM users WHERE email = 'teacher1@example.com' LIMIT 1),
    'active'
);

-- Bài học cho Python Cơ Bản
INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT 
    id,
    'Giới thiệu Python và Cài đặt',
    'Tìm hiểu về Python, lịch sử phát triển, và cách cài đặt môi trường phát triển.',
    1,
    'https://www.youtube.com/watch?v=kqtD5dpn9C8',
    true,
    NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Biến và Kiểu Dữ Liệu', 'Học về các kiểu dữ liệu cơ bản: số, chuỗi, boolean, list, tuple, dictionary.', 2, 'https://www.youtube.com/watch?v=khKv-8q7YmY', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Câu Lệnh Điều Kiện và Vòng Lặp', 'If/else, for, while loops và cách sử dụng hiệu quả.', 3, 'https://www.youtube.com/watch?v=OnDr4J2UXSA', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Hàm và Module', 'Cách tạo và sử dụng hàm, import module, và tổ chức code.', 4, 'https://www.youtube.com/watch?v=NSbOtYzIQI0', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Lập Trình Hướng Đối Tượng (OOP)', 'Class, Object, Inheritance, Polymorphism trong Python.', 5, 'https://www.youtube.com/watch?v=JeznW_7DlB0', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Xử Lý File và Exception', 'Đọc/ghi file, xử lý lỗi với try/except.', 6, NULL, true, NOW() + INTERVAL '1 day'
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Làm Việc với Database', 'Kết nối và thao tác với SQLite, MySQL bằng Python.', 7, NULL, false, NOW() + INTERVAL '2 days'
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Xây Dựng API với Flask', 'Tạo RESTful API đơn giản với Flask framework.', 8, NULL, false, NOW() + INTERVAL '3 days'
FROM khoa_hoc WHERE tieu_de LIKE 'Python Cơ Bản%';

-- Khóa học 2: JavaScript Full Stack
INSERT INTO khoa_hoc (tieu_de, mo_ta, cap_do, hinh_anh, gia, gia_goc, so_buoi, thoi_luong, hinh_thuc, teacher_id, trang_thai)
VALUES (
    'JavaScript Full Stack - React & Node.js',
    'Khóa học JavaScript toàn diện từ frontend đến backend. Học React, Node.js, Express, MongoDB. Xây dựng ứng dụng web hoàn chỉnh.',
    'Intermediate',
    'https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?w=800',
    2990000,
    3990000,
    25,
    '50 giờ',
    'online',
    (SELECT id FROM users WHERE email = 'teacher2@example.com' LIMIT 1),
    'active'
);

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'JavaScript ES6+ Cơ Bản', 'Arrow functions, destructuring, spread operator, promises.', 1, 'https://www.youtube.com/watch?v=NCwa_xi0Uuc', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'JavaScript Full Stack%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'DOM Manipulation và Events', 'Thao tác với DOM, xử lý events, tạo tương tác.', 2, 'https://www.youtube.com/watch?v=0ik6X4DJKCc', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'JavaScript Full Stack%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'React Cơ Bản', 'Components, Props, State, Hooks (useState, useEffect).', 3, 'https://www.youtube.com/watch?v=DLX62G4lc44', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'JavaScript Full Stack%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'React Router và State Management', 'Điều hướng với React Router, quản lý state với Context API.', 4, NULL, true, NOW() + INTERVAL '1 day'
FROM khoa_hoc WHERE tieu_de LIKE 'JavaScript Full Stack%';

-- Khóa học 3: Web Development
INSERT INTO khoa_hoc (tieu_de, mo_ta, cap_do, hinh_anh, gia, gia_goc, so_buoi, thoi_luong, hinh_thuc, teacher_id, trang_thai)
VALUES (
    'Web Development Cơ Bản - HTML, CSS, JavaScript',
    'Khóa học web development cho người mới bắt đầu. Học HTML5, CSS3, JavaScript từ cơ bản đến nâng cao. Xây dựng website responsive và tương tác.',
    'Beginner',
    'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=800',
    1490000,
    1990000,
    15,
    '30 giờ',
    'online',
    (SELECT id FROM users WHERE email = 'teacher1@example.com' LIMIT 1),
    'active'
);

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'HTML5 Cơ Bản', 'Cấu trúc HTML, semantic tags, forms, tables.', 1, 'https://www.youtube.com/watch?v=UB1O30fR-EE', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Web Development Cơ Bản%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'CSS3 Styling', 'Selectors, box model, flexbox, grid layout.', 2, 'https://www.youtube.com/watch?v=yfoY53QXEnI', true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Web Development Cơ Bản%';

-- Khóa học 4: Data Science
INSERT INTO khoa_hoc (tieu_de, mo_ta, cap_do, hinh_anh, gia, gia_goc, so_buoi, thoi_luong, hinh_thuc, teacher_id, trang_thai)
VALUES (
    'Data Science với Python - Pandas, NumPy, Matplotlib',
    'Khóa học phân tích dữ liệu với Python. Học Pandas để xử lý data, NumPy cho tính toán, Matplotlib để visualize. Thực hành với dataset thực tế.',
    'Advanced',
    'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800',
    3990000,
    4990000,
    30,
    '60 giờ',
    'online',
    (SELECT id FROM users WHERE email = 'teacher2@example.com' LIMIT 1),
    'active'
);

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'Giới thiệu Data Science', 'Tổng quan về Data Science, các công cụ và thư viện.', 1, NULL, true, NOW()
FROM khoa_hoc WHERE tieu_de LIKE 'Data Science%';

INSERT INTO chi_tiet_khoa_hoc (khoa_hoc_id, tieu_de_muc, noi_dung, thu_tu, video_path, is_unlocked, unlock_date)
SELECT id, 'NumPy - Tính Toán Số Học', 'Arrays, operations, broadcasting, linear algebra.', 2, NULL, true, NOW() + INTERVAL '1 day'
FROM khoa_hoc WHERE tieu_de LIKE 'Data Science%';

