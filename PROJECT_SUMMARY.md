# Tóm tắt dự án - Ứng dụng Học Trực Tuyến

## 📋 Thông tin dự án

- **Tên dự án**: Ứng dụng Học Trực Tuyến
- **Môn học**: Phát triển ứng dụng mã nguồn mở
- **Công nghệ**: Python Flask + MySQL + Jinja2 Templates

## ✅ Đã hoàn thành

### 1. Cấu trúc dự án
- ✅ Flask backend với cấu trúc rõ ràng
- ✅ Database schema MySQL đầy đủ
- ✅ Templates HTML với Bootstrap 5
- ✅ Static files (CSS, JS)

### 2. Chức năng cơ bản
- ✅ Đăng ký/Đăng nhập/Đăng xuất
- ✅ Quản lý khóa học (xem danh sách, chi tiết)
- ✅ Đăng ký khóa học
- ✅ Dashboard cho Student/Teacher/Admin
- ✅ Phân quyền người dùng

### 3. Chức năng nâng cao (3 chức năng - mỗi cái 0.5 điểm)

#### 🎯 Chức năng 1: Hệ thống đánh giá khóa học (0.5 điểm)
- Học viên có thể đánh giá khóa học (1-5 sao)
- Xem đánh giá của các học viên khác
- Tính điểm trung bình tự động
- Hiển thị số lượng đánh giá
- **File liên quan**: 
  - `app.py`: Route `add_review()`
  - `templates/course_detail.html`: Form đánh giá

#### 🎯 Chức năng 2: Quản lý bài tập và nộp bài (0.5 điểm)
- Giáo viên tạo bài tập cho khóa học
- Học viên xem danh sách bài tập
- Học viên nộp bài (text + file đính kèm)
- Giáo viên chấm điểm và nhận xét
- Xem trạng thái nộp bài
- **File liên quan**:
  - `app.py`: Routes `assignments()`, `submit_assignment()`, `grade_assignment()`, `create_assignment()`
  - `templates/assignments.html`: Danh sách bài tập
  - `templates/submit_assignment.html`: Form nộp bài

#### 🎯 Chức năng 3: Hệ thống thông báo (0.5 điểm)
- Admin tạo thông báo (hệ thống, khóa học, bài tập)
- Học viên xem thông báo liên quan
- Phân loại thông báo
- **File liên quan**:
  - `app.py`: Routes `notifications()`, `create_notification()`
  - `templates/notifications.html`: Danh sách thông báo
  - `templates/admin/create_notification.html`: Form tạo thông báo

## 📁 Cấu trúc file

```
Webhoctructuyen/
├── app.py                          # File chính Flask
├── init_db.py                      # Script khởi tạo database
├── requirements.txt                # Python dependencies
├── env.example                     # Mẫu file cấu hình
├── README.md                       # Hướng dẫn tổng quan
├── INSTALL.md                      # Hướng dẫn cài đặt
├── GITHUB_GUIDE.md                 # Hướng dẫn Git/GitHub
├── PROJECT_SUMMARY.md             # File này
├── .gitignore                      # Git ignore rules
│
├── database/
│   └── schema.sql                  # Database schema
│
├── templates/                      # Jinja2 templates
│   ├── base.html                   # Template cơ sở
│   ├── index.html                  # Trang chủ
│   ├── courses.html                # Danh sách khóa học
│   ├── course_detail.html          # Chi tiết khóa học
│   ├── login.html                  # Đăng nhập
│   ├── register.html               # Đăng ký
│   ├── assignments.html            # Danh sách bài tập
│   ├── submit_assignment.html      # Nộp bài
│   ├── notifications.html          # Thông báo
│   ├── student/
│   │   └── dashboard.html          # Dashboard học viên
│   ├── teacher/
│   │   ├── dashboard.html          # Dashboard giáo viên
│   │   └── create_assignment.html  # Tạo bài tập
│   └── admin/
│       ├── dashboard.html          # Dashboard admin
│       └── create_notification.html # Tạo thông báo
│
└── static/                         # Static files
    ├── css/
    │   └── style.css               # Custom CSS
    └── js/
        └── main.js                 # Custom JavaScript
```

## 🗄️ Database Schema

### Các bảng chính:
1. **users** - Người dùng (student, teacher, admin)
2. **khoa_hoc** - Khóa học
3. **chi_tiet_khoa_hoc** - Chi tiết nội dung khóa học
4. **dang_ky_khoa_hoc** - Đăng ký khóa học
5. **danh_gia_khoa_hoc** - Đánh giá khóa học ⭐
6. **bai_tap** - Bài tập ⭐
7. **nop_bai** - Nộp bài tập ⭐
8. **thong_bao** - Thông báo ⭐
9. **lich_hoc** - Lịch học

⭐ = Bảng cho chức năng nâng cao

## 🚀 Cách chạy

1. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

2. **Cấu hình database**:
- Tạo file `.env` từ `env.example`
- Điền thông tin MySQL

3. **Khởi tạo database**:
```bash
python init_db.py
```

4. **Chạy ứng dụng**:
```bash
python app.py
```

5. **Truy cập**: http://localhost:5000

## 📝 Tài khoản mặc định

- **Admin**: admin@example.com / admin123
- **Teacher**: teacher@example.com / teacher123

## 🔗 Kết nối GitHub

Xem file `GITHUB_GUIDE.md` để biết cách:
- Tạo repository trên GitHub
- Kết nối project với GitHub
- Commit và push code
- Sử dụng Git commands

## 📊 Điểm số dự kiến

- **Chức năng cơ bản**: 7 điểm
- **Chức năng nâng cao 1** (Đánh giá): 0.5 điểm
- **Chức năng nâng cao 2** (Bài tập): 0.5 điểm
- **Chức năng nâng cao 3** (Thông báo): 0.5 điểm
- **Tổng**: 8.5 điểm

## 🎯 Hướng phát triển tiếp

Có thể mở rộng thêm:
- Chat trực tuyến
- Video streaming
- Điểm danh tự động
- Export báo cáo
- Payment gateway
- Email notifications

## 📞 Hỗ trợ

Nếu gặp vấn đề, kiểm tra:
1. File `INSTALL.md` - Hướng dẫn cài đặt chi tiết
2. File `GITHUB_GUIDE.md` - Hướng dẫn Git/GitHub
3. File `README.md` - Tổng quan dự án

---

**Chúc bạn làm bài tốt! 🎉**


