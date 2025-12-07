# Hướng dẫn kết nối GitHub và Commit code

## Bước 1: Tạo Repository trên GitHub

1. Đăng nhập vào GitHub: https://github.com
2. Click vào dấu **+** ở góc trên bên phải → chọn **New repository**
3. Đặt tên repository (ví dụ: `webhoctructuyen`)
4. Chọn **Public** hoặc **Private**
5. **KHÔNG** tích vào "Initialize this repository with a README"
6. Click **Create repository**

## Bước 2: Cài đặt Git (nếu chưa có)

### Windows:
1. Tải Git từ: https://git-scm.com/download/win
2. Cài đặt với các tùy chọn mặc định

### Kiểm tra cài đặt:
```bash
git --version
```

## Bước 3: Cấu hình Git lần đầu

```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
```

## Bước 4: Khởi tạo Git trong project

Mở terminal/command prompt trong thư mục `Webhoctructuyen`:

```bash
cd Webhoctructuyen

# Khởi tạo git repository
git init

# Thêm tất cả file vào staging area
git add .

# Commit lần đầu
git commit -m "Initial commit: Ứng dụng học trực tuyến - Flask + MySQL"
```

## Bước 5: Kết nối với GitHub

Sau khi tạo repository trên GitHub, bạn sẽ thấy URL như:
`https://github.com/username/webhoctructuyen.git`

```bash
# Thêm remote repository
git remote add origin https://github.com/username/webhoctructuyen.git

# Đổi tên branch thành main (nếu cần)
git branch -M main

# Push code lên GitHub
git push -u origin main
```

Nếu được yêu cầu đăng nhập:
- Username: Tên đăng nhập GitHub của bạn
- Password: Sử dụng **Personal Access Token** (xem bước 6)

## Bước 6: Tạo Personal Access Token (nếu cần)

1. Vào GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click **Generate new token (classic)**
3. Đặt tên token (ví dụ: "Webhoctructuyen")
4. Chọn quyền: **repo** (full control)
5. Click **Generate token**
6. **Lưu token lại** (chỉ hiện 1 lần)
7. Dùng token này làm password khi push code

## Bước 7: Các lệnh Git thường dùng

### Xem trạng thái
```bash
git status
```

### Thêm file vào staging
```bash
# Thêm tất cả file đã thay đổi
git add .

# Thêm file cụ thể
git add app.py
```

### Commit
```bash
git commit -m "Mô tả thay đổi"
```

Ví dụ:
```bash
git commit -m "Thêm chức năng đánh giá khóa học"
git commit -m "Sửa lỗi đăng nhập"
git commit -m "Cập nhật giao diện dashboard"
```

### Push lên GitHub
```bash
git push origin main
```

### Pull code mới nhất
```bash
git pull origin main
```

### Xem lịch sử commit
```bash
git log
```

### Tạo branch mới
```bash
git checkout -b feature/new-feature
git push -u origin feature/new-feature
```

## Bước 8: Workflow làm việc hàng ngày

```bash
# 1. Kiểm tra trạng thái
git status

# 2. Thêm file đã thay đổi
git add .

# 3. Commit với message rõ ràng
git commit -m "Mô tả ngắn gọn về thay đổi"

# 4. Push lên GitHub
git push origin main
```

## Lưu ý quan trọng

1. **Luôn commit với message rõ ràng**: Mô tả ngắn gọn về những gì đã thay đổi
2. **Commit thường xuyên**: Không để quá nhiều thay đổi trong 1 commit
3. **Kiểm tra trước khi push**: Dùng `git status` và `git log` để xem thay đổi
4. **Không commit file nhạy cảm**: `.env`, `__pycache__/`, etc. (đã có trong .gitignore)

## Xử lý lỗi thường gặp

### Lỗi: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/username/webhoctructuyen.git
```

### Lỗi: "Updates were rejected"
```bash
# Pull code mới nhất trước
git pull origin main --rebase
# Sau đó push lại
git push origin main
```

### Quên commit message
```bash
git commit --amend -m "Message mới"
```

## Tài liệu tham khảo

- Git Documentation: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com
- Git Cheat Sheet: https://education.github.com/git-cheat-sheet-education.pdf


