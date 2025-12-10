# 🗄️ Hướng dẫn Setup Database

## 📍 Vị trí chạy lệnh

**Chạy từ thư mục gốc của project:**
```
D:\Manguonmo\BDU-Phat-trien-ungdungmanguonmo
```

## 🔄 Thoát khỏi venv (nếu đang trong venv)

```powershell
deactivate
```

Sau khi thoát, prompt sẽ không còn `(venv)` ở đầu.

## ✅ Bước 1: Tạo bảng Enrollment

```powershell
# Đảm bảo đang ở thư mục gốc
cd D:\Manguonmo\BDU-Phat-trien-ungdungmanguonmo

# Chạy SQL để tạo bảng
psql -U elearn -d elearning -f database\create_enrollment_table.sql
```

**Lưu ý:** 
- Nếu hỏi password, nhập password của user `elearn`
- Nếu lỗi "file not found", kiểm tra đường dẫn file

## ✅ Bước 2: Seed dữ liệu khóa học

```powershell
# Vẫn ở thư mục gốc
psql -U elearn -d elearning -f database\seed_programming_courses_fixed.sql
```

## 🔍 Kiểm tra dữ liệu đã seed

```powershell
# Vào psql
psql -U elearn -d elearning
```

Sau đó chạy các lệnh SQL:

```sql
-- Xem khóa học
SELECT id, tieu_de, cap_do, gia FROM khoa_hoc;

-- Xem số lượng bài học
SELECT khoa_hoc_id, COUNT(*) as so_bai_hoc 
FROM chi_tiet_khoa_hoc 
GROUP BY khoa_hoc_id;

-- Xem giáo viên
SELECT id, email, ho_ten, vai_tro FROM users WHERE vai_tro = 'teacher';

-- Thoát psql
\q
```

## 🐛 Troubleshooting

### Lỗi "psql: command not found"
- PostgreSQL chưa được thêm vào PATH
- Thêm PostgreSQL bin vào PATH hoặc dùng full path:
```powershell
"C:\Program Files\PostgreSQL\16\bin\psql.exe" -U elearn -d elearning -f database\create_enrollment_table.sql
```

### Lỗi "permission denied"
- User `elearn` chưa có quyền
- Chạy với user `postgres`:
```powershell
psql -U postgres -d elearning -f database\create_enrollment_table.sql
```

### Lỗi "relation already exists"
- Bảng đã tồn tại, bỏ qua bước 1 hoặc xóa bảng cũ:
```sql
DROP TABLE IF EXISTS dang_ky_khoa_hoc CASCADE;
```

## 📝 Tóm tắt lệnh (copy-paste)

```powershell
# 1. Thoát venv (nếu đang trong venv)
deactivate

# 2. Đảm bảo ở thư mục gốc
cd D:\Manguonmo\BDU-Phat-trien-ungdungmanguonmo

# 3. Tạo bảng enrollment
psql -U elearn -d elearning -f database\create_enrollment_table.sql

# 4. Seed dữ liệu
psql -U elearn -d elearning -f database\seed_programming_courses_fixed.sql

# 5. Kiểm tra (tùy chọn)
psql -U elearn -d elearning
# Sau đó chạy: SELECT * FROM khoa_hoc;
```

