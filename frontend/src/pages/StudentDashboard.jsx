import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

export default function StudentDashboard() {
  const { user } = useAuth()
  const [enrolledCourses, setEnrolledCourses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (user) {
      fetchEnrolledCourses()
    }
  }, [user])

  const fetchEnrolledCourses = async () => {
    try {
      const response = await axios.get('/api/users/me/enrollments/with-courses')
      setEnrolledCourses(response.data.map(item => item.course))
    } catch (error) {
      console.error('Failed to fetch enrolled courses:', error)
    } finally {
      setLoading(false)
    }
  }

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
        <h1 className="title-gradient">Dashboard - Học viên</h1>
        <div>
          <Link to="/courses" className="btn btn-outline-custom">
            <i className="bi bi-plus-circle"></i> Đăng ký khóa học mới
          </Link>
        </div>
      </div>

      <div className="row mb-4">
        <div className="col-md-12">
          <div className="card-soft">
            <h5 className="mb-4">
              <i className="bi bi-book text-brand-sky me-2"></i>Khóa học của tôi
            </h5>
            {enrolledCourses.length === 0 ? (
              <div className="text-center py-5">
                <i className="bi bi-book text-muted" style={{ fontSize: '4rem' }}></i>
                <p className="text-muted mt-3">Bạn chưa đăng ký khóa học nào.</p>
                <Link to="/courses" className="btn btn-primary-custom mt-2">
                  <i className="bi bi-search"></i> Tìm khóa học
                </Link>
              </div>
            ) : (
              <div className="table-responsive">
                <table className="table table-hover">
                  <thead>
                    <tr>
                      <th>Tên khóa học</th>
                      <th>Trạng thái</th>
                      <th>Tiến độ</th>
                      <th>Chứng nhận</th>
                      <th>Thao tác</th>
                    </tr>
                  </thead>
                  <tbody>
                    {enrolledCourses.map((course) => (
                      <tr key={course.id}>
                        <td>
                          <strong>{course.tieu_de}</strong>
                        </td>
                        <td>
                          <span className="badge-custom badge-success">Đang học</span>
                        </td>
                        <td>
                          <div className="progress" style={{ height: '8px' }}>
                            <div
                              className="progress-bar bg-success"
                              role="progressbar"
                              style={{ width: '0%' }}
                            ></div>
                          </div>
                        </td>
                        <td>
                          <Link
                            to={`/certificate/${course.id}`}
                            className="btn btn-sm btn-outline-success"
                          >
                            <i className="bi bi-award"></i> Xem chứng nhận
                          </Link>
                        </td>
                        <td>
                          <Link
                            to={`/learn/${course.id}`}
                            className="btn btn-sm btn-primary-custom me-2"
                          >
                            <i className="bi bi-play-circle"></i> Vào học
                          </Link>
                          <Link
                            to={`/courses/${course.id}`}
                            className="btn btn-sm btn-outline-custom"
                          >
                            <i className="bi bi-eye"></i> Chi tiết
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

