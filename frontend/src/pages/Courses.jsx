import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

export default function Courses() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  
  // Filter states
  const [search, setSearch] = useState('')
  const [level, setLevel] = useState('')
  const [mode, setMode] = useState('')
  const [sort, setSort] = useState('newest')

  useEffect(() => {
    fetchCourses()
  }, [level, mode, sort])

  useEffect(() => {
    // Scroll to all-courses section if coming from header link
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get('scroll') === 'true') {
      setTimeout(() => {
        const element = document.getElementById('all-courses')
        if (element) {
          const headerOffset = 80
          const elementPosition = element.getBoundingClientRect().top
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset
          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          })
          // Remove scroll param from URL
          window.history.replaceState({}, '', '/courses')
        }
      }, 300)
    }
  }, [])

  const fetchCourses = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (search) params.append('q', search)
      if (level) params.append('cap_do', level)
      if (mode) params.append('hinh_thuc', mode)
      if (sort) params.append('sort', sort)

      const response = await axios.get(`/api/courses?${params.toString()}`)
      setCourses(response.data)
      setError('')
    } catch (error) {
      setError('Không thể tải danh sách khóa học')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchCourses()
  }

  const handleFilterChange = () => {
    fetchCourses()
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
    <>
      {/* Header Section - Migrated from courses.html */}
      <div className="bg-gradient-sky-green text-white py-5 position-relative overflow-hidden" id="all-courses" style={{ paddingTop: '100px', paddingBottom: '80px' }}>
        <div className="position-absolute top-0 left-0 w-100 h-100" style={{ 
          background: 'radial-gradient(circle at 20% 50%, rgba(255,255,255,0.1) 0%, transparent 50%), radial-gradient(circle at 80% 80%, rgba(255,255,255,0.1) 0%, transparent 50%)',
          pointerEvents: 'none'
        }}></div>
        <div className="container text-center position-relative">
          <h1 className="display-4 fw-bold mb-3" style={{ textShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>Tất cả khóa học</h1>
          <p className="lead fs-5" style={{ opacity: 0.95 }}>Khám phá các chương trình học toàn diện cho mọi trình độ</p>
        </div>
      </div>

      {/* Courses Section */}
      <div className="container my-5" style={{ paddingTop: '2rem' }}>
        {/* Search and Filter */}
        <div className="row mb-5 g-3 align-items-center">
          <div className="col-lg-5">
            <form onSubmit={handleSearch}>
              <div className="input-group input-group-lg">
                <input
                  type="text"
                  className="form-control"
                  placeholder="Tìm kiếm khóa học..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                <button className="btn btn-primary-custom" type="submit">
                  <i className="bi bi-search"></i> Tìm kiếm
                </button>
              </div>
            </form>
          </div>
          <div className="col-lg-2">
            <select
              className="form-select form-select-lg"
              value={level}
              onChange={(e) => {
                setLevel(e.target.value)
                handleFilterChange()
              }}
            >
              <option value="">Tất cả cấp độ</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>
          <div className="col-lg-2">
            <select
              className="form-select form-select-lg"
              value={mode}
              onChange={(e) => {
                setMode(e.target.value)
                handleFilterChange()
              }}
            >
              <option value="">Hình thức</option>
              <option value="online">Online</option>
              <option value="offline">Offline</option>
              <option value="hybrid">Hybrid</option>
            </select>
          </div>
          <div className="col-lg-3">
            <select
              className="form-select form-select-lg"
              value={sort}
              onChange={(e) => {
                setSort(e.target.value)
                handleFilterChange()
              }}
            >
              <option value="newest">Mới nhất</option>
              <option value="price_asc">Giá tăng dần</option>
              <option value="price_desc">Giá giảm dần</option>
            </select>
          </div>
        </div>

        {/* Courses List */}
        {error ? (
          <div className="alert alert-danger text-center">
            <i className="bi bi-exclamation-circle"></i> {error}
          </div>
        ) : courses.length === 0 ? (
          <div className="alert alert-info text-center">
            <i className="bi bi-info-circle"></i> Không tìm thấy khóa học nào.
          </div>
        ) : (
          <div className="row g-4">
            {courses.map((course) => (
              <div key={course.id} className="col-md-4">
                <div className="course-card h-100">
                  {course.hinh_anh ? (
                    <img
                      src={course.hinh_anh}
                      className="course-card-img"
                      alt={course.tieu_de}
                    />
                  ) : (
                    <div className="course-card-img bg-secondary d-flex align-items-center justify-content-center">
                      <i className="bi bi-book text-white" style={{ fontSize: '4rem' }}></i>
                    </div>
                  )}
                  <div className="course-card-body">
                    <h5 className="course-card-title">{course.tieu_de}</h5>
                    <p className="course-card-text">
                      {course.mo_ta
                        ? course.mo_ta.length > 120
                          ? course.mo_ta.substring(0, 120) + '...'
                          : course.mo_ta
                        : 'Không có mô tả'}
                    </p>
                    <div className="d-flex align-items-center gap-2 mb-2">
                      <span className="badge-custom badge-info">
                        {course.cap_do || 'N/A'}
                      </span>
                      <span className="badge-custom badge-success text-uppercase">
                        {course.hinh_thuc || 'online'}
                      </span>
                    </div>
                    <div className="d-flex align-items-center text-muted small mb-2">
                      <i className="bi bi-calendar-check me-1"></i>
                      {course.so_buoi || 0} buổi
                    </div>
                    <div className="mt-auto">
                      <p className="course-card-price mb-3">
                        {new Intl.NumberFormat('vi-VN').format(course.gia)} VNĐ
                      </p>
                      <Link
                        to={`/courses/${course.id}`}
                        className="btn btn-primary-custom w-100"
                      >
                        Xem chi tiết
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  )
}
