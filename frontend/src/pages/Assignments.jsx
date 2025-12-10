import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

export default function Assignments() {
  const { id: courseId } = useParams()
  const { user } = useAuth()
  const [assignments, setAssignments] = useState([])
  const [submissions, setSubmissions] = useState({})
  const [loading, setLoading] = useState(true)
  const [selectedAssignment, setSelectedAssignment] = useState(null)
  const [submissionText, setSubmissionText] = useState('')
  const [submissionFile, setSubmissionFile] = useState(null)

  useEffect(() => {
    fetchAssignments()
  }, [courseId])

  const fetchAssignments = async () => {
    try {
      const response = await axios.get(`/api/courses/${courseId}/assignments`)
      setAssignments(response.data)
      
      // Fetch submissions for each assignment
      for (const assignment of response.data) {
        try {
          const subResponse = await axios.get(`/api/assignments/${assignment.id}/submissions`)
          if (subResponse.data.length > 0) {
            setSubmissions(prev => ({
              ...prev,
              [assignment.id]: subResponse.data[0]
            }))
          }
        } catch (error) {
          console.error(`Failed to fetch submissions for assignment ${assignment.id}:`, error)
        }
      }
    } catch (error) {
      console.error('Failed to fetch assignments:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (assignmentId) => {
    try {
      const formData = new FormData()
      formData.append('noi_dung', submissionText)
      if (submissionFile) {
        formData.append('file', submissionFile)
      }

      await axios.post(`/api/assignments/${assignmentId}/submit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      alert('Nộp bài thành công!')
      setSubmissionText('')
      setSubmissionFile(null)
      setSelectedAssignment(null)
      fetchAssignments()
    } catch (error) {
      alert('Nộp bài thất bại: ' + (error.response?.data?.detail || error.message))
    }
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Không có hạn'
    const date = new Date(dateString)
    return date.toLocaleDateString('vi-VN')
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
        <h1 className="title-gradient">
          <i className="bi bi-file-earmark-check"></i> Bài tập
        </h1>
        <Link to={`/learn/${courseId}`} className="btn btn-outline-custom">
          <i className="bi bi-arrow-left"></i> Quay lại
        </Link>
      </div>

      {assignments.length === 0 ? (
        <div className="alert alert-info text-center">
          <i className="bi bi-info-circle"></i> Chưa có bài tập nào.
        </div>
      ) : (
        <div className="row">
          {assignments.map((assignment) => {
            const submission = submissions[assignment.id]
            const isOverdue = assignment.han_nop && new Date(assignment.han_nop) < new Date()
            const isSubmitted = submission && submission.trang_thai !== 'cancelled'

            return (
              <div key={assignment.id} className="col-md-6 mb-4">
                <div className="card-soft h-100">
                  <div className="d-flex justify-content-between align-items-start mb-3">
                    <h5 className="mb-0">{assignment.tieu_de}</h5>
                    {assignment.is_required && (
                      <span className="badge bg-danger">Bắt buộc</span>
                    )}
                  </div>
                  
                  <div className="mb-3">
                    <p className="text-muted">{assignment.noi_dung}</p>
                  </div>

                  <div className="mb-3">
                    <small className="text-muted d-block">
                      <i className="bi bi-calendar"></i> Hạn nộp: {formatDate(assignment.han_nop)}
                    </small>
                    <small className="text-muted d-block">
                      <i className="bi bi-star"></i> Điểm tối đa: {assignment.diem_toi_da}
                    </small>
                  </div>

                  {isSubmitted ? (
                    <div className="alert alert-success">
                      <h6>Đã nộp bài</h6>
                      {submission.diem !== null && (
                        <p className="mb-1">
                          <strong>Điểm: {submission.diem}/{assignment.diem_toi_da}</strong>
                        </p>
                      )}
                      {submission.nhan_xet && (
                        <p className="mb-0">
                          <strong>Nhận xét:</strong> {submission.nhan_xet}
                        </p>
                      )}
                      {submission.file_path && (
                        <a href={submission.file_path} target="_blank" rel="noopener noreferrer" className="btn btn-sm btn-outline-primary mt-2">
                          <i className="bi bi-download"></i> Tải file đã nộp
                        </a>
                      )}
                    </div>
                  ) : (
                    <>
                      {isOverdue && (
                        <div className="alert alert-warning">
                          <i className="bi bi-exclamation-triangle"></i> Đã quá hạn nộp bài
                        </div>
                      )}
                      <button
                        className="btn btn-primary-custom w-100"
                        onClick={() => setSelectedAssignment(assignment)}
                      >
                        <i className="bi bi-upload"></i> Nộp bài
                      </button>
                    </>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* Submission Modal */}
      {selectedAssignment && (
        <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Nộp bài: {selectedAssignment.tieu_de}</h5>
                <button
                  type="button"
                  className="btn-close"
                  onClick={() => {
                    setSelectedAssignment(null)
                    setSubmissionText('')
                    setSubmissionFile(null)
                  }}
                ></button>
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Nội dung bài làm:</label>
                  <textarea
                    className="form-control"
                    rows="5"
                    value={submissionText}
                    onChange={(e) => setSubmissionText(e.target.value)}
                    placeholder="Nhập nội dung bài làm của bạn..."
                  ></textarea>
                </div>
                <div className="mb-3">
                  <label className="form-label">File đính kèm (nếu có):</label>
                  <input
                    type="file"
                    className="form-control"
                    onChange={(e) => setSubmissionFile(e.target.files[0])}
                  />
                </div>
                <div className="alert alert-info">
                  <small>
                    <i className="bi bi-info-circle"></i> Hạn nộp: {formatDate(selectedAssignment.han_nop)}
                  </small>
                </div>
              </div>
              <div className="modal-footer">
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => {
                    setSelectedAssignment(null)
                    setSubmissionText('')
                    setSubmissionFile(null)
                  }}
                >
                  Hủy
                </button>
                <button
                  type="button"
                  className="btn btn-primary-custom"
                  onClick={() => handleSubmit(selectedAssignment.id)}
                  disabled={!submissionText && !submissionFile}
                >
                  <i className="bi bi-upload"></i> Nộp bài
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

