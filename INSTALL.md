# Hướng dẫn cài đặt và chạy ứng dụng

## Yêu cầu hệ thống

- Python 3.8 trở lên
- MySQL 5.7 trở lên hoặc MariaDB 10.3 trở lên
- pip (Python package manager)

## Bước 1: Cài đặt MySQL

### Windows:
1. Tải MySQL từ: https://dev.mysql.com/downloads/installer/
2. Cài đặt MySQL Server
3. Ghi nhớ username và password root

### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

### Mac:
```bash
brew install mysql
brew services start mysql
```

## Bước 2: Tạo môi trường ảo Python

```bash
# Di chuyển vào thư mục project
cd Webhoctructuyen

# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment

# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

## Bước 3: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Bước 4: Cấu hình database

1. Tạo file `.env` từ `.env.example`:
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Chỉnh sửa file `.env`:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=webhoctructuyen
SECRET_KEY=your-secret-key-here
```

3. Tạo secret key (tùy chọn):
```bash
python -c "import secrets; print(secrets.token_hex(24))"
```

## Bước 5: Khởi tạo database

### Cách 1: Sử dụng script Python (Khuyến nghị)
```bash
python init_db.py
```

### Cách 2: Chạy SQL thủ công
```bash
mysql -u root -p < database/schema.sql
```

Sau đó tạo tài khoản mặc định:
```bash
python -c "from werkzeug.security import generate_password_hash; print('Admin hash:', generate_password_hash('admin123')); print('Teacher hash:', generate_password_hash('teacher123'))"
```

## Bước 6: Chạy ứng dụng

```bash
python app.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## Tài khoản mặc định

Sau khi chạy `init_db.py`, bạn có thể đăng nhập với:

- **Admin**: 
  - Email: `admin@example.com`
  - Password: `admin123`

- **Teacher**: 
  - Email: `teacher@example.com`
  - Password: `teacher123`

## Xử lý lỗi thường gặp

### Lỗi: "ModuleNotFoundError: No module named 'flask'"
```bash
# Đảm bảo đã kích hoạt virtual environment
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

### Lỗi: "Can't connect to MySQL server"
- Kiểm tra MySQL đã chạy chưa
- Kiểm tra thông tin trong file `.env`
- Kiểm tra MySQL user có quyền tạo database

### Lỗi: "Access denied for user"
- Kiểm tra username và password trong `.env`
- Đảm bảo MySQL user có đủ quyền

### Lỗi: "Table already exists"
- Database đã được tạo trước đó
- Có thể bỏ qua hoặc xóa database và tạo lại:
```sql
DROP DATABASE IF EXISTS webhoctructuyen;
CREATE DATABASE webhoctructuyen;
```

## Cấu trúc thư mục sau khi cài đặt

```
Webhoctructuyen/
├── app.py                 # File chính
├── init_db.py            # Script khởi tạo DB
├── requirements.txt      # Dependencies
├── .env                  # Cấu hình (tạo từ .env.example)
├── venv/                 # Virtual environment
├── database/
│   └── schema.sql        # Database schema
├── templates/            # HTML templates
├── static/               # CSS, JS, images
└── uploads/              # Files uploaded (tự động tạo)
```

## Phát triển tiếp

Sau khi cài đặt thành công, bạn có thể:

1. Chạy ứng dụng: `python app.py`
2. Truy cập: http://localhost:5000
3. Đăng nhập với tài khoản admin hoặc teacher
4. Bắt đầu phát triển các tính năng mới

## Gợi ý cho bài tập

1. **Chức năng nâng cao đã có**:
   - ✅ Hệ thống đánh giá khóa học
   - ✅ Quản lý bài tập và nộp bài
   - ✅ Hệ thống thông báo

2. **Có thể mở rộng thêm**:
   - Chat trực tuyến giữa học viên và giáo viên
   - Video streaming cho bài giảng
   - Hệ thống điểm danh tự động
   - Báo cáo và thống kê chi tiết
   - Export dữ liệu ra Excel/PDF


