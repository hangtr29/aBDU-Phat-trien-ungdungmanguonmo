# 🔧 Sửa lỗi Seed Data

## ❌ Lỗi gặp phải:

1. **`column "vai_tro" does not exist`** 
   - Model dùng `role` chứ không phải `vai_tro`

2. **Encoding errors với tiếng Việt**
   - File SQL có ký tự tiếng Việt không đúng UTF-8

## ✅ Giải pháp:

Đã tạo file mới: `database/seed_programming_courses_fixed_utf8.sql`

### Thay đổi:
- ✅ Dùng `role` thay vì `vai_tro`
- ✅ Bỏ dấu tiếng Việt (dùng không dấu) để tránh lỗi encoding
- ✅ Giữ nguyên logic và cấu trúc

## 🚀 Chạy lại:

```powershell
.\setup-database.ps1
```

Hoặc chạy trực tiếp:

```powershell
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U elearn -d elearning -f database\seed_programming_courses_fixed_utf8.sql
```

## 📝 Lưu ý:

- File mới dùng tiếng Việt không dấu để tránh lỗi encoding
- Có thể thêm lại dấu sau khi đảm bảo database dùng UTF-8
- Password hash cho teacher vẫn giữ nguyên (cần generate lại nếu cần)

