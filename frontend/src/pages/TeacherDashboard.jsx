import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import CourseScheduleManager from '../components/CourseScheduleManager'

export default function TeacherDashboard() {
  const { user } = useAuth()
  const [courses, setCourses] = useState([])
  const [students, setStudents] = useState([])
  const [pendingSubmissions, setPendingSubmissions] = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [stats, setStats] = useState({
    totalCourses: 0,
    totalStudents: 0,
    pendingSubmissions: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      // Lấy stats và courses cùng lúc
      const [statsRes, coursesRes, studentsRes, submissionsRes] = await Promise.all([
        axios.get('/api/teachers/me/stats'),
        axios.get('/api/teachers/me/courses/with-stats'),
        axios.get('/api/teachers/me/students'),
        axios.get('/api/teachers/me/pending-submissions')
      ])
      
      setStats(statsRes.data)
      setCourses(coursesRes.data)
      setStudents(studentsRes.data)
      setPendingSubmissions(submissionsRes.data)
    } catch (error) {
      console.error('Failed to fetch data:', error)
      // Fallback: lấy courses như cũ
      try {
        const response = await axios.get('/api/courses')
        const myCourses = response.data.filter(course => course.teacher_id === user?.id)
        setCourses(myCourses)
      } catch (err) {
        console.error('Failed to fetch courses:', err)
      }
    } finally {
      setLoading(false)
    }
  }
  
  useEffect(() => {
    if (activeTab === 'students' || activeTab === 'submissions') {
      fetchData()
    }
  }, [activeTab])

  if (loading) {
    return (
      <div className="text-center py-8">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Đang tải...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="container my-5">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1 className="title-gradient">
          <i className="bi bi-person-badge"></i> Dashboard - Giáo viên
        </h1>
        <Link to="/courses" className="btn btn-primary-custom">
          <i className="bi bi-plus-circle"></i> Tạo khóa học mới
        </Link>
      </div>

      <div className="row mb-4">
        <div className="col-md-4">
          <div className="card-soft text-center">
            <h3 className="text-brand-sky">{stats.totalCourses}</h3>
            <p className="text-muted mb-0">Khóa học của tôi</p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card-soft text-center">
            <h3 className="text-brand-green">{stats.totalStudents}</h3>
            <p className="text-muted mb-0">Học viên</p>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card-soft text-center">
            <h3 className="text-warning">{stats.pendingSubmissions}</h3>
            <p className="text-muted mb-0">Bài tập cần chấm</p>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <i className="bi bi-speedometer2"></i> Tổng quan
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'students' ? 'active' : ''}`}
            onClick={() => setActiveTab('students')}
          >
            <i className="bi bi-people"></i> Học viên
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'submissions' ? 'active' : ''}`}
            onClick={() => setActiveTab('submissions')}
          >
            <i className="bi bi-file-earmark-check"></i> Bài tập cần chấm
            {pendingSubmissions.length > 0 && (
              <span className="badge bg-danger ms-2">{pendingSubmissions.length}</span>
            )}
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === 'schedule' ? 'active' : ''}`}
            onClick={() => setActiveTab('schedule')}
          >
            <i className="bi bi-calendar-event"></i> Thời khóa biểu
          </button>
        </li>
      </ul>

      {/* Tab: Tổng quan */}
      {activeTab === 'overview' && (
      <div className="card-soft">
        <h5 className="mb-4">
          <i className="bi bi-book text-brand-sky me-2"></i>Khóa học của tôi
        </h5>
        {courses.length === 0 ? (
          <div className="text-center py-5">
            <i className="bi bi-book text-muted" style={{ fontSize: '4rem' }}></i>
            <p className="text-muted mt-3">Bạn chưa có khóa học nào.</p>
            <Link to="/courses" className="btn btn-primary-custom mt-2">
              <i className="bi bi-plus-circle"></i> Tạo khóa học mới
            </Link>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Tên khóa học</th>
                  <th>Cấp độ</th>
                  <th>Hình thức</th>
                  <th>Học viên</th>
                  <th>Giá</th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr key={course.id}>
                    <td><strong>{course.tieu_de}</strong></td>
                    <td>
                      <span className="badge-custom badge-info">{course.cap_do || 'N/A'}</span>
                    </td>
                    <td>
                      <span className="badge-custom badge-success">{course.hinh_thuc || 'online'}</span>
                    </td>
                    <td>
                      <span className="badge-custom badge-info">
                        <i className="bi bi-people"></i> {course.student_count || 0}
                      </span>
                    </td>
                    <td>{new Intl.NumberFormat('vi-VN').format(course.gia)} VNĐ</td>
                    <td>
                      <Link
                        to={`/learn/${course.id}`}
                        className="btn btn-sm btn-primary-custom me-2"
                      >
                        <i className="bi bi-eye"></i> Xem
                      </Link>
                      <Link
                        to={`/learn/${course.id}?tab=assignments`}
                        className="btn btn-sm btn-outline-custom"
                      >
                        <i className="bi bi-file-earmark-check"></i> Bài tập
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      )}

      {/* Tab: Học viên */}
      {activeTab === 'students' && (
        <div className="card-soft">
          <h5 className="mb-4">
            <i className="bi bi-people text-brand-sky me-2"></i>Học viên đã mua khóa học
          </h5>
          {students.length === 0 ? (
            <div className="alert alert-info">
              <i className="bi bi-info-circle"></i> Chưa có học viên nào đăng ký khóa học của bạn.
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Học viên</th>
                    <th>Email</th>
                    <th>Khóa học</th>
                    <th>Tiến độ hoàn thành</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((student, idx) => (
                    <tr key={`${student.student_id}-${student.course_id}-${idx}`}>
                      <td>
                        <strong>{student.student_name}</strong>
                      </td>
                      <td>{student.student_email}</td>
                      <td>
                        <Link to={`/learn/${student.course_id}`} className="text-decoration-none">
                          {student.course_name}
                        </Link>
                      </td>
                      <td>
                        <div className="d-flex align-items-center">
                          <div className="progress flex-grow-1 me-2" style={{ height: '20px', minWidth: '150px' }}>
                            <div
                              className={`progress-bar ${student.progress_percentage === 100 ? 'bg-success' : 'bg-info'}`}
                              style={{ width: `${student.progress_percentage}%` }}
                            >
                              {student.progress_percentage}%
                            </div>
                          </div>
                          <small className="text-muted">
                            {student.completed_lessons}/{student.total_lessons} bài
                          </small>
                        </div>
                      </td>
                      <td>
                        <Link
                          to={`/learn/${student.course_id}`}
                          className="btn btn-sm btn-outline-primary"
                        >
                          <i className="bi bi-eye"></i> Xem
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Tab: Bài tập cần chấm */}
      {activeTab === 'submissions' && (
        <div className="card-soft">
          <h5 className="mb-4">
            <i className="bi bi-file-earmark-check text-warning me-2"></i>Bài tập cần chấm
          </h5>
          {pendingSubmissions.length === 0 ? (
            <div className="alert alert-success">
              <i className="bi bi-check-circle"></i> Không có bài tập nào cần chấm. Tất cả đã được chấm!
            </div>
          ) : (
            <div className="table-responsive">
              <table className="table table-hover">
                <thead>
                  <tr>
                    <th>Học viên</th>
                    <th>Email</th>
                    <th>Khóa học</th>
                    <th>Bài tập</th>
                    <th>Ngày nộp</th>
                    <th>Thao tác</th>
                  </tr>
                </thead>
                <tbody>
                  {pendingSubmissions.map((submission) => (
                    <tr key={submission.submission_id}>
                      <td>
                        <strong>{submission.student_name}</strong>
                      </td>
                      <td>{submission.student_email}</td>
                      <td>
                        <Link to={`/learn/${submission.course_id}`} className="text-decoration-none">
                          {submission.course_name}
                        </Link>
                      </td>
                      <td>
                        <strong>{submission.assignment_title}</strong>
                        <br />
                        <small className="text-muted">Điểm tối đa: {submission.max_score}</small>
                      </td>
                      <td>
                        {new Date(submission.submitted_at).toLocaleString('vi-VN')}
                      </td>
                      <td>
                        <Link
                          to={`/grade/${submission.course_id}/${submission.assignment_id}`}
                          className="btn btn-sm btn-warning"
                        >
                          <i className="bi bi-pencil"></i> Chấm bài
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Tab: Thời khóa biểu */}
      {activeTab === 'schedule' && (
        <div className="card-soft">
          <h5 className="mb-4">
            <i className="bi bi-calendar-event text-brand-sky me-2"></i>Thời khóa biểu các khóa học
          </h5>
          {courses.length === 0 ? (
            <div className="alert alert-info">
              <i className="bi bi-info-circle"></i> Bạn chưa có khóa học nào. Hãy tạo khóa học để quản lý thời khóa biểu.
            </div>
          ) : (
            <div>
              {courses.map((course) => (
                <div key={course.id} className="mb-4">
                  <CourseScheduleManager courseId={course.id} courseTitle={course.tieu_de} />
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
