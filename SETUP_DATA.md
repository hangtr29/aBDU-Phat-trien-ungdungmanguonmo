# 📊 Hướng dẫn Setup Dữ Liệu

## 1. Tạo bảng Enrollment

```bash
psql -U elearn -d elearning -f database/create_enrollment_table.sql
```

## 2. Seed dữ liệu khóa học lập trình

```bash
psql -U elearn -d elearning -f database/seed_programming_courses_fixed.sql
```

## 3. Kiểm tra dữ liệu

```bash
psql -U elearn -d elearning
```

```sql
-- Xem khóa học
SELECT id, tieu_de, cap_do, gia FROM khoa_hoc;

-- Xem bài học
SELECT khoa_hoc_id, tieu_de_muc, thu_tu FROM chi_tiet_khoa_hoc ORDER BY khoa_hoc_id, thu_tu;

-- Xem giáo viên
SELECT id, email, ho_ten, vai_tro FROM users WHERE vai_tro = 'teacher';
```

## 4. Tạo tài khoản test

### Học viên:
- Email: `student@example.com`
- Password: `student123`

### Giáo viên:
- Email: `teacher1@example.com` hoặc `teacher2@example.com`
- Password: `teacher123`

## 5. Khóa học đã seed:

1. **Python Cơ Bản** - Beginner - 1,990,000 VNĐ
2. **JavaScript Full Stack** - Intermediate - 2,990,000 VNĐ
3. **Web Development Cơ Bản** - Beginner - 1,490,000 VNĐ
4. **Data Science với Python** - Advanced - 3,990,000 VNĐ

Mỗi khóa học có 5-8 bài học với video YouTube và drip content.

