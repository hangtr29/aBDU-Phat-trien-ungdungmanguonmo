# Frontend Setup - React + Vite

## Cài đặt

```bash
cd frontend
npm install
```

## Chạy development server

```bash
npm run dev
```

Frontend sẽ chạy tại `http://localhost:3000`

## Cấu trúc

- `src/pages/` - Các trang chính (Login, Register, Courses, CourseDetail)
- `src/components/` - Components tái sử dụng (Layout)
- `src/context/` - Context API cho authentication
- `src/index.css` - Global styles

## API Integration

Frontend kết nối với FastAPI backend tại `http://127.0.0.1:8001` thông qua proxy trong `vite.config.js`.

## Tính năng đã implement

✅ Login/Register với JWT
✅ Danh sách khóa học
✅ Chi tiết khóa học với Lesson Tree
✅ Video Player (YouTube, Vimeo, HTML5)
✅ Drip Content (hiển thị locked/unlocked)

## Tính năng cần bổ sung

- [ ] Progress Tracking UI
- [ ] File Upload cho giáo viên
- [ ] Certificates page
- [ ] Discussion Forum UI
- [ ] Video streaming optimization

