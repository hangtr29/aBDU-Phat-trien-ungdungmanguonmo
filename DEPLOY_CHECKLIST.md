# ✅ Checklist Kiểm tra Code trước khi Deploy

## 📋 Kiểm tra Backend

### Dependencies
- [x] `fastapi` - Web framework
- [x] `uvicorn[standard]` - ASGI server
- [x] `SQLAlchemy` - ORM
- [x] `psycopg[binary]` - PostgreSQL driver
- [x] `python-jose` - JWT
- [x] `passlib[bcrypt]` - Password hashing
- [x] `pydantic` - Data validation
- [x] `pydantic-settings` - Settings management
- [x] `python-multipart` - File uploads
- [x] `python-dotenv` - Environment variables
- [x] `bcrypt` - Password hashing
- [x] `email-validator` - Email validation
- [x] `alembic` - Database migrations (optional)

### Files cần có
- [x] `fastapi_app/main.py` - Entry point
- [x] `fastapi_app/requirements.txt` - Dependencies
- [x] `fastapi_app/core/config.py` - Configuration
- [x] `fastapi_app/.env.example` - Environment variables template
- [x] `render.yaml` - Render configuration (optional)
- [x] `scripts/run_migrations.py` - Migration script

### Environment Variables cần set trên Render
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `JWT_SECRET` - Secret key for JWT (random string)
- [ ] `JWT_ALG` - JWT algorithm (HS256)
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiry (30)
- [ ] `REFRESH_TOKEN_EXPIRE_MINUTES` - Refresh token expiry (1440)
- [ ] `ALLOWED_ORIGINS` - CORS allowed origins (JSON array)

### Routes đã được đăng ký
- [x] `/api/auth` - Authentication
- [x] `/api/users` - User management
- [x] `/api/courses` - Courses
- [x] `/api/content` - Course content
- [x] `/api/progress` - User progress
- [x] `/api/discussions` - Discussions
- [x] `/api/certificates` - Certificates
- [x] `/api/enrollments` - Enrollments
- [x] `/api/assignments` - Assignments
- [x] `/api/quiz` - Quizzes
- [x] `/api/stats` - Statistics
- [x] `/api/reviews` - Reviews
- [x] `/api/notifications` - Notifications
- [x] `/api/code` - Code execution
- [x] `/api/payments` - Payments
- [x] `/api/wallet` - Wallet
- [x] `/api/admin` - Admin functions
- [x] `/api/teachers` - Teacher dashboard
- [x] `/api/messages` - Messaging
- [x] `/api/video` - Video streaming

### Static Files
- [x] Static files directory mounted at `/static`
- [x] Upload directories created:
  - `static/uploads/assignments`
  - `static/uploads/assignment_files`
  - `static/uploads/discussions`
  - `static/uploads/videos`

---

## 📋 Kiểm tra Frontend

### Dependencies
- [x] `react` - UI library
- [x] `react-dom` - React DOM
- [x] `react-router-dom` - Routing
- [x] `axios` - HTTP client
- [x] `bootstrap` - CSS framework
- [x] `bootstrap-icons` - Icons
- [x] `qrcode.react` - QR code generation
- [x] `vite` - Build tool
- [x] `@vitejs/plugin-react` - Vite React plugin

### Files cần có
- [x] `frontend/package.json` - Dependencies
- [x] `frontend/vite.config.js` - Vite configuration
- [x] `frontend/src/main.jsx` - Entry point
- [x] `frontend/src/App.jsx` - Main app component
- [x] `frontend/src/config/axios.js` - Axios configuration
- [x] `vercel.json` - Vercel configuration (optional)

### Environment Variables cần set trên Vercel
- [ ] `VITE_API_BASE_URL` - Backend API URL (https://your-backend.onrender.com)

### Pages đã được tạo
- [x] Login page
- [x] Register page
- [x] Courses listing
- [x] Course detail
- [x] Learn page (course content)
- [x] User profile
- [x] Admin dashboard
- [x] Teacher dashboard
- [x] Student dashboard
- [x] Add funds page
- [x] Transaction guide
- [x] Security policy

### Components đã được tạo
- [x] Layout (header, footer)
- [x] Payment modal
- [x] Chat widget
- [x] Notification bell
- [x] Video player
- [x] Quiz section
- [x] Review section
- [x] Footer

### API Integration
- [x] All API calls use axios from `config/axios.js`
- [x] Authentication token automatically added to requests
- [x] Error handling for 401 (token expired)

---

## 📋 Kiểm tra Database

### Tables cần có
- [x] `users` - User accounts
- [x] `khoa_hoc` - Courses
- [x] `bai_hoc` - Lessons
- [x] `dang_ky_khoa_hoc` - Enrollments
- [x] `thong_bao` - Notifications
- [x] `thanh_toan` - Payments
- [x] `bai_tap` - Assignments
- [x] `nop_bai` - Submissions
- [x] `deposit_transactions` - Deposit transactions
- [x] `messages` - Chat messages
- [x] `thao_luan` - Discussions

### Migrations
- [x] `schema_pg.sql` - Base schema
- [x] `create_enrollment_table.sql` - Enrollments
- [x] `create_notifications_table.sql` - Notifications
- [x] `create_payments_table.sql` - Payments
- [x] `add_tai_lieu_to_lessons.sql` - Lesson files
- [x] `add_diem_toi_da_to_assignments.sql` - Assignment max score
- [x] `create_deposit_transactions.sql` - Deposit transactions
- [x] `add_deposit_fields.sql` - Deposit fields
- [x] `add_user_balance.sql` - User balance

---

## 📋 Kiểm tra Deployment

### Render (Backend)
- [ ] Repository connected
- [ ] Build command: `pip install -r fastapi_app/requirements.txt`
- [ ] Start command: `cd fastapi_app && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables set
- [ ] Database connected
- [ ] Migrations run

### Vercel (Frontend)
- [ ] Repository connected
- [ ] Root directory: `frontend` (if needed)
- [ ] Build command: `cd frontend && npm install && npm run build`
- [ ] Output directory: `frontend/dist`
- [ ] Environment variables set
- [ ] CORS updated on backend

---

## 🐛 Common Issues

### Backend không start
- Kiểm tra logs trên Render
- Kiểm tra DATABASE_URL đúng chưa
- Kiểm tra dependencies đã cài đầy đủ chưa

### Frontend không kết nối được backend
- Kiểm tra VITE_API_BASE_URL đúng chưa
- Kiểm tra ALLOWED_ORIGINS trên backend
- Kiểm tra CORS errors trong browser console

### Database connection failed
- Kiểm tra DATABASE_URL format
- Kiểm tra database đã được tạo chưa
- Kiểm tra migrations đã chạy chưa

---

**Sau khi hoàn thành checklist này, bạn có thể deploy với tự tin! 🚀**

