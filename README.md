# Ứng dụng Học Trực Tuyến

Dự án cuối kỳ môn **Phát triển ứng dụng mã nguồn mở**

## 📋 Mô tả

Hệ thống quản lý học trực tuyến với đầy đủ chức năng cho học viên, giáo viên và quản trị viên.

## 🛠️ Công nghệ sử dụng

- **Backend**: Python Flask
- **Frontend**: Jinja2 Templates, HTML, CSS, JavaScript
- **Database**: MySQL
- **Authentication**: Session-based với password hashing

## 📦 Cài đặt

### 1. Clone repository

```bash
git clone <your-repo-url>
cd Webhoctructuyen
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình Database

1. Tạo database MySQL:
```sql
mysql -u root -p < database/schema.sql
```

2. Tạo file `.env` từ `.env.example`:
```bash
cp .env.example .env
```

3. Chỉnh sửa file `.env` với thông tin MySQL của bạn:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=webhoctructuyen
```

### 5. Chạy ứng dụng

```bash
python app.py
```

Truy cập: http://localhost:5000

## 👥 Tài khoản mặc định

- **Admin**: admin@example.com / admin123
- **Teacher**: teacher@example.com / teacher123

## 📁 Cấu trúc dự án

```
Webhoctructuyen/
├── app.py                 # File chính của ứng dụng
├── requirements.txt       # Dependencies
├── .env.example          # Mẫu file cấu hình
├── .gitignore            # Git ignore file
├── README.md             # File này
├── database/
│   └── schema.sql        # Database schema
├── templates/            # Jinja2 templates
│   ├── index.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── login.html
│   ├── register.html
│   ├── student/
│   ├── teacher/
│   └── admin/
├── static/               # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── uploads/             # Uploaded files
```

## 🚀 Chức năng nâng cao

### 1. Hệ thống đánh giá và phản hồi (0.5 điểm)
- Học viên có thể đánh giá khóa học (1-5 sao)
- Xem đánh giá của các học viên khác
- Tính điểm trung bình tự động

### 2. Quản lý bài tập và nộp bài (0.5 điểm)
- Giáo viên tạo bài tập cho khóa học
- Học viên nộp bài và xem điểm
- Giáo viên chấm điểm và nhận xét

### 3. Hệ thống thông báo (0.5 điểm)
- Thông báo hệ thống
- Thông báo theo khóa học
- Thông báo về bài tập mới

## 📝 Hướng dẫn sử dụng Git

### 1. Khởi tạo Git repository

```bash
git init
```

### 2. Thêm remote repository (GitHub)

```bash
git remote add origin https://github.com/your-username/your-repo-name.git
```

### 3. Commit và push code

```bash
# Thêm tất cả file
git add .

# Commit với message
git commit -m "Initial commit: Ứng dụng học trực tuyến"

# Push lên GitHub
git branch -M main
git push -u origin main
```

### 4. Các lệnh Git thường dùng

```bash
# Xem trạng thái
git status

# Xem lịch sử commit
git log

# Tạo branch mới
git checkout -b feature/new-feature

# Merge branch
git merge feature/new-feature

# Pull code mới nhất
git pull origin main
```

## 📄 License

MIT License

## 👨‍💻 Tác giả

Nhóm sinh viên - Môn Phát triển ứng dụng mã nguồn mở


