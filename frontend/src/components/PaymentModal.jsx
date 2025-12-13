import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

export default function PaymentModal({ course, onClose, onSuccess }) {
  const { user, fetchUser } = useAuth()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [walletBalance, setWalletBalance] = useState(0)
  const [showInsufficientBalanceModal, setShowInsufficientBalanceModal] = useState(false)

  useEffect(() => {
    // Lấy số dư ví
    if (user?.so_du !== undefined) {
      setWalletBalance(user.so_du)
    } else {
      fetchWalletBalance()
    }
  }, [user])

  const fetchWalletBalance = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('/api/wallet/balance', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setWalletBalance(parseFloat(response.data.so_du) || 0)
    } catch (err) {
      console.error('Failed to fetch wallet balance:', err)
    }
  }

  const handlePayment = async () => {
    if (!course || !course.gia || course.gia <= 0) {
      setError('Khóa học này miễn phí, không cần thanh toán')
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      
      // Kiểm tra số dư
      if (walletBalance < course.gia) {
        setShowInsufficientBalanceModal(true)
        setLoading(false)
        return
      }

      // Mua khóa học bằng ví
      const response = await axios.post(
        `/api/payments/buy-with-wallet?khoa_hoc_id=${course.id}`,
        null,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      // Tính số dư mới (trừ đi giá khóa học)
      const newBalance = walletBalance - course.gia
      setWalletBalance(newBalance)
      
      // Cập nhật số dư từ server để đảm bảo đồng bộ
      if (fetchUser) {
        await fetchUser()
      } else {
        // Nếu không có fetchUser, lấy trực tiếp từ API
        const balanceResponse = await axios.get('/api/wallet/balance', {
          headers: { Authorization: `Bearer ${token}` }
        })
        setWalletBalance(parseFloat(balanceResponse.data.so_du) || 0)
      }
      
      // Gọi callback thành công
      if (onSuccess) {
        onSuccess()
      }
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Thanh toán thất bại')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal fade show" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-dialog-centered">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">
              <i className="bi bi-credit-card me-2"></i>
              Thanh toán khóa học
            </h5>
            <button type="button" className="btn-close" onClick={onClose}></button>
          </div>
          <div className="modal-body">
            {course && (
              <>
                <div className="mb-3">
                  <h6>{course.tieu_de}</h6>
                  <p className="text-muted mb-0">Giá: <strong className="text-success">{new Intl.NumberFormat('vi-VN').format(course.gia)} VNĐ</strong></p>
                </div>

                <div className="mb-3 p-3 bg-light rounded">
                  <div className="d-flex justify-content-between align-items-center">
                    <span className="fw-bold">Số dư ví:</span>
                    <span className={`fw-bold ${walletBalance >= course.gia ? 'text-success' : 'text-danger'}`}>
                      {new Intl.NumberFormat('vi-VN').format(walletBalance)} VNĐ
                    </span>
                  </div>
                  {walletBalance < course.gia && (
                    <small className="text-danger d-block mt-2">
                      <i className="bi bi-exclamation-triangle me-1"></i>
                      Số dư không đủ. Vui lòng nạp thêm tiền.
                    </small>
                  )}
                </div>

                {error && (
                  <div className="alert alert-danger">
                    <i className="bi bi-exclamation-circle me-2"></i>
                    {error}
                  </div>
                )}
              </>
            )}
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={onClose} disabled={loading}>
              Hủy
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handlePayment}
              disabled={loading || walletBalance < course.gia}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2"></span>
                  Đang xử lý...
                </>
              ) : (
                <>
                  <i className="bi bi-check-circle me-2"></i>
                  Thanh toán
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Modal số dư không đủ */}
      {showInsufficientBalanceModal && (
        <div className="modal fade show" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1060 }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header bg-warning text-dark">
                <h5 className="modal-title">
                  <i className="bi bi-exclamation-triangle me-2"></i>
                  Số dư không đủ
                </h5>
                <button 
                  type="button" 
                  className="btn-close" 
                  onClick={() => setShowInsufficientBalanceModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                <div className="text-center mb-3">
                  <i className="bi bi-wallet2 text-warning" style={{ fontSize: '3rem' }}></i>
                </div>
                <p className="text-center mb-3">
                  Số dư ví của bạn không đủ để thanh toán khóa học này.
                </p>
                <div className="card bg-light mb-3">
                  <div className="card-body">
                    <div className="row text-center">
                      <div className="col-6">
                        <small className="text-muted d-block">Số dư hiện tại</small>
                        <strong className="text-danger">
                          {new Intl.NumberFormat('vi-VN').format(walletBalance)} VNĐ
                        </strong>
                      </div>
                      <div className="col-6">
                        <small className="text-muted d-block">Giá khóa học</small>
                        <strong className="text-success">
                          {new Intl.NumberFormat('vi-VN').format(course.gia)} VNĐ
                        </strong>
                      </div>
                    </div>
                    <hr />
                    <div className="text-center">
                      <small className="text-muted d-block">Cần thêm</small>
                      <strong className="text-warning">
                        {new Intl.NumberFormat('vi-VN').format(course.gia - walletBalance)} VNĐ
                      </strong>
                    </div>
                  </div>
                </div>
                <p className="text-center text-muted small mb-0">
                  Vui lòng nạp thêm tiền vào ví để tiếp tục thanh toán.
                </p>
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={() => setShowInsufficientBalanceModal(false)}
                >
                  Hủy
                </button>
                <button
                  type="button"
                  className="btn btn-primary"
                  onClick={() => {
                    setShowInsufficientBalanceModal(false)
                    onClose()
                    navigate('/addfunds')
                  }}
                >
                  <i className="bi bi-wallet2 me-2"></i>
                  Nạp tiền ngay
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

