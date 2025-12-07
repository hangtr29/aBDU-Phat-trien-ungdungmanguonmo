# Hướng dẫn kiểm tra CSS

## Cách kiểm tra CSS đã được load

1. **Mở trình duyệt và vào trang web**
2. **Nhấn F12 để mở Developer Tools**
3. **Vào tab Network**
4. **Refresh trang (F5)**
5. **Tìm file `style.css` trong danh sách**
6. **Kiểm tra Status code phải là 200 (OK)**

## Nếu CSS không load được

### Kiểm tra đường dẫn
- Đảm bảo file `static/css/style.css` tồn tại
- Kiểm tra trong `base.html` có dòng:
  ```html
  <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
  ```

### Kiểm tra Flask static folder
- Flask mặc định serve static files từ thư mục `static/`
- Đảm bảo cấu trúc thư mục đúng:
  ```
  Webhoctructuyen/
  ├── app.py
  ├── static/
  │   └── css/
  │       └── style.css
  └── templates/
      └── base.html
  ```

### Hard refresh
- Nhấn `Ctrl + F5` (Windows) hoặc `Cmd + Shift + R` (Mac) để hard refresh
- Xóa cache trình duyệt

### Kiểm tra console
- Mở Developer Tools (F12)
- Vào tab Console
- Xem có lỗi nào không

## Test CSS

Thêm dòng này vào đầu `style.css` để test:
```css
body {
    background-color: red !important; /* Test - xóa sau */
}
```

Nếu background đổi màu đỏ, CSS đã được load thành công.

## Các class CSS chính

- `.btn-primary-custom` - Button gradient
- `.btn-outline-custom` - Button outline
- `.card-soft` - Card mềm mại
- `.course-card` - Card khóa học
- `.title-gradient` - Tiêu đề gradient
- `.hero-section` - Hero section
- `.badge-custom` - Badge tùy chỉnh


