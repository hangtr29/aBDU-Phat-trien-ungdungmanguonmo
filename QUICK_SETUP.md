# ⚡ Quick Setup Database

## Cách 1: Dùng script (Dễ nhất) ⭐

```powershell
.\setup-database.ps1
```

Script sẽ tự động:
1. Tạo bảng enrollment
2. Seed dữ liệu khóa học

## Cách 2: Chạy từng file

```powershell
# Tạo bảng
.\run-sql.ps1 database\create_enrollment_table.sql

# Seed data
.\run-sql.ps1 database\seed_programming_courses_fixed.sql
```

## Cách 3: Chạy thủ công (nếu script không chạy)

```powershell
# Tạo bảng
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U elearn -d elearning -f database\create_enrollment_table.sql

# Seed data
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U elearn -d elearning -f database\seed_programming_courses_fixed.sql
```

**Lưu ý:** Sẽ hỏi password của user `elearn`

## Kiểm tra kết quả

```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U elearn -d elearning
```

Sau đó chạy:
```sql
SELECT id, tieu_de, cap_do, gia FROM khoa_hoc;
\q
```

Bạn sẽ thấy 4 khóa học về lập trình!

