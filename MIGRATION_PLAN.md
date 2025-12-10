# 📋 Kế hoạch Tái sử dụng Logic & Layout từ Web Flask cũ

## ✅ Có thể tái sử dụng TRỰC TIẾP:

### 1. **CSS Styles** (100% tái sử dụng)
- ✅ File: `static/css/style.css` → Copy vào `frontend/src/styles/`
- ✅ Brand colors, gradients, custom components
- ✅ Bootstrap 5 classes đã dùng
- ✅ Responsive design

### 2. **Static Assets**
- ✅ Images, icons
- ✅ Uploaded files (videos, PDFs)
- ✅ Fonts

### 3. **Business Logic** (đã có ở FastAPI)
- ✅ Course enrollment logic
- ✅ Progress tracking
- ✅ Assignment submission
- ✅ Payment flow
- ✅ Certificate generation

## 🔄 Cần Convert sang React:

### 1. **HTML Templates → React Components**

| Flask Template | React Component | Status |
|---------------|----------------|--------|
| `base.html` | `Layout.jsx` | ✅ Đã có (cần cải thiện) |
| `courses.html` | `Courses.jsx` | ✅ Đã có (cần thêm filter/search) |
| `course_detail.html` | `CourseDetail.jsx` | ✅ Đã có (cần cải thiện) |
| `student/learn.html` | `LearnPage.jsx` | ⏳ Cần tạo |
| `student/dashboard.html` | `StudentDashboard.jsx` | ⏳ Cần tạo |
| `teacher/dashboard.html` | `TeacherDashboard.jsx` | ⏳ Cần tạo |
| `admin/dashboard.html` | `AdminDashboard.jsx` | ⏳ Cần tạo |
| `assignments.html` | `Assignments.jsx` | ⏳ Cần tạo |
| `certificate.html` | `Certificate.jsx` | ⏳ Cần tạo |

### 2. **Jinja2 Logic → React Logic**

**Flask (Jinja2):**
```jinja2
{% if session.user_id %}
  <a href="{{ url_for('dashboard') }}">Dashboard</a>
{% endif %}
```

**React:**
```jsx
{user && <Link to="/dashboard">Dashboard</Link>}
```

## 🎨 Bước tiếp theo - Migrate CSS & Layout:

### Bước 1: Copy CSS vào React
```bash
# Copy CSS file
cp static/css/style.css frontend/src/styles/style.css

# Import vào React
import './styles/style.css'
```

### Bước 2: Cài Bootstrap 5 cho React
```bash
cd frontend
npm install bootstrap bootstrap-icons
```

### Bước 3: Convert Layout Component
- Copy navigation từ `base.html`
- Convert Jinja2 conditionals → React conditionals
- Giữ nguyên CSS classes

## 📝 Checklist Migration:

### Phase 1: Setup & Styling
- [ ] Copy `style.css` vào React
- [ ] Cài Bootstrap 5 + Bootstrap Icons
- [ ] Cập nhật `Layout.jsx` với navigation từ `base.html`
- [ ] Test responsive design

### Phase 2: Core Pages
- [ ] Migrate `courses.html` → `Courses.jsx` (thêm search/filter)
- [ ] Migrate `course_detail.html` → `CourseDetail.jsx`
- [ ] Migrate `student/learn.html` → `LearnPage.jsx`
- [ ] Migrate `student/dashboard.html` → `StudentDashboard.jsx`

### Phase 3: Teacher Features
- [ ] Migrate `teacher/dashboard.html` → `TeacherDashboard.jsx`
- [ ] Migrate `teacher/assignments.html` → `TeacherAssignments.jsx`
- [ ] Migrate `teacher/course_content.html` → `CourseContent.jsx`

### Phase 4: Admin Features
- [ ] Migrate `admin/dashboard.html` → `AdminDashboard.jsx`
- [ ] Migrate `admin/courses.html` → `AdminCourses.jsx`
- [ ] Migrate `admin/payments.html` → `AdminPayments.jsx`

### Phase 5: Advanced Features
- [ ] Migrate `assignments.html` → `Assignments.jsx`
- [ ] Migrate `certificate.html` → `Certificate.jsx`
- [ ] Migrate `notifications.html` → `Notifications.jsx`

## 🚀 Bắt đầu ngay:

Tôi sẽ giúp bạn:
1. Copy CSS và setup Bootstrap
2. Cải thiện Layout component với navigation từ web cũ
3. Migrate từng trang một

Bạn muốn bắt đầu với phần nào trước?

