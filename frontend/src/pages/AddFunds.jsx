import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function AddFunds() {
  const navigate = useNavigate()
  const [amount, setAmount] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [qrData, setQrData] = useState(null)
  const [showSuccessModal, setShowSuccessModal] = useState(false)
  
  // Thông tin người nhận mặc định
  const [bankInfo] = useState({
    stk: '0377070269',
    ten_nguoi_nhan: 'LE GIA BAO',
    ten_ngan_hang: 'Vietcombank'
  })

  const [transferContent, setTransferContent] = useState('')
  const [submittedAmount, setSubmittedAmount] = useState(null)

  const handleGenerateQR = async () => {
    // Validate
    if (!amount || amount === '') {
      setError('Vui lòng nhập số tiền')
      return
    }

    const amountNum = parseFloat(amount)
    if (isNaN(amountNum) || amountNum < 50000) {
      setError('Số tiền tối thiểu là 50,000 VNĐ')
      return
    }

    if (amountNum !== Math.floor(amountNum)) {
      setError('Chỉ nhập số nguyên (không có phần thập phân)')
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        '/api/wallet/add-funds',
        { so_tien: amountNum },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setTransferContent(response.data.noi_dung_chuyen_khoan)
      setQrData(response.data.qr_code_data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setAmount('')
    setQrData(null)
    setTransferContent('')
    setError('')
  }

  const handleCopy = (text, label) => {
    navigator.clipboard.writeText(text)
    alert(`Đã copy ${label}!`)
  }

  const handleSubmitPayment = async () => {
    if (!transferContent || !amount) {
      setError('Vui lòng tạo QR code trước khi báo đã thanh toán')
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      const amountNum = parseFloat(amount)
      
      await axios.post(
        '/api/wallet/submit-payment',
        {
          so_tien: amountNum,
          noi_dung_chuyen_khoan: transferContent
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setSubmittedAmount(amountNum)
      setShowSuccessModal(true)
      setAmount('')
      setTransferContent('')
      setQrData(null)
    } catch (err) {
      setError(err.response?.data?.detail || 'Có lỗi xảy ra khi gửi yêu cầu')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container my-5">
      <div className="row">
        <div className="col-12 mb-4">
          <button 
            className="btn btn-outline-secondary"
            onClick={() => navigate(-1)}
          >
            <i className="bi bi-arrow-left me-2"></i>
            Quay lại
          </button>
          <h2 className="mt-3">Nạp tiền vào tài khoản</h2>
        </div>
      </div>

      <div className="row g-4">
        {/* A. Thông tin người nhận (bên trái) */}
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-header bg-primary text-white">
              <h5 className="mb-0">
                <i className="bi bi-info-circle me-2"></i>
                Thông tin người nhận
              </h5>
            </div>
            <div className="card-body">
              <>
                <div className="mb-3">
                  <label className="form-label fw-bold">Số tài khoản (STK):</label>
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control"
                      value={bankInfo.stk}
                      readOnly
                    />
                    <button
                      className="btn btn-outline-secondary"
                      type="button"
                      onClick={() => handleCopy(bankInfo.stk, 'Số tài khoản')}
                    >
                      <i className="bi bi-clipboard"></i> Copy
                    </button>
                  </div>
                </div>

                <div className="mb-3">
                  <label className="form-label fw-bold">Tên người nhận:</label>
                  <input
                    type="text"
                    className="form-control"
                    value={bankInfo.ten_nguoi_nhan}
                    readOnly
                  />
                </div>

                {transferContent && (
                  <div className="mb-3">
                    <label className="form-label fw-bold">Nội dung chuyển khoản:</label>
                    <div className="input-group">
                      <input
                        type="text"
                        className="form-control"
                        value={transferContent}
                        readOnly
                      />
                      <button
                        className="btn btn-outline-secondary"
                        type="button"
                        onClick={() => handleCopy(transferContent, 'Nội dung chuyển khoản')}
                      >
                        <i className="bi bi-clipboard"></i> Copy
                      </button>
                    </div>
                    <small className="text-muted">
                      <i className="bi bi-info-circle me-1"></i>
                      Vui lòng copy và paste chính xác nội dung này khi chuyển khoản
                    </small>
                  </div>
                )}
              </>
            </div>
          </div>
        </div>

        {/* B. QR Code (ở giữa) */}
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-header bg-success text-white">
              <h5 className="mb-0">
                <i className="bi bi-qr-code me-2"></i>
                QR Code VietQR
              </h5>
            </div>
            <div className="card-body text-center">
              <div className="mb-3 position-relative">
                <img 
                  src="/qr-code-payment.png" 
                  alt="VietQR Payment Code" 
                  className="img-fluid rounded"
                  style={{ maxWidth: '100%', height: 'auto', border: '2px solid #28a745' }}
                  onError={(e) => {
                    console.error('Error loading QR image')
                    e.target.style.display = 'none'
                    const errorDiv = e.target.parentElement.querySelector('.qr-error')
                    if (errorDiv) {
                      errorDiv.style.display = 'block'
                    }
                  }}
                />
                <div className="qr-error alert alert-warning" style={{ display: 'none' }}>
                  <i className="bi bi-exclamation-triangle me-2"></i>
                  <strong>Không tìm thấy ảnh QR code</strong>
                  <br />
                  <small>Vui lòng đặt file <code>qr-code-payment.png</code> vào thư mục <code>frontend/public/</code></small>
                </div>
              </div>
              <div className="mb-2 p-2 bg-light rounded">
                <p className="mb-1"><strong>{bankInfo.ten_nguoi_nhan}</strong></p>
                <p className="mb-0 text-muted">{bankInfo.stk}</p>
              </div>
              <p className="text-muted small mt-3">
                <i className="bi bi-info-circle me-1"></i>
                Quét QR code bằng ứng dụng ngân hàng để chuyển khoản
              </p>
            </div>
          </div>
        </div>

        {/* C. Nhập số tiền (bên phải) */}
        <div className="col-md-4">
          <div className="card h-100">
            <div className="card-header bg-warning text-dark">
              <h5 className="mb-0">
                <i className="bi bi-cash-coin me-2"></i>
                Nhập số tiền
              </h5>
            </div>
            <div className="card-body">
              <div className="mb-3">
                <label className="form-label fw-bold">Số tiền nạp (VNĐ):</label>
                <input
                  type="number"
                  className="form-control form-control-lg"
                  placeholder="Nhập số tiền"
                  value={amount}
                  onChange={(e) => {
                    const value = e.target.value
                    // Chỉ cho phép số nguyên
                    if (value === '' || /^\d+$/.test(value)) {
                      setAmount(value)
                    }
                  }}
                  min="50000"
                  step="1"
                  disabled={loading}
                />
                <small className="text-muted">
                  <i className="bi bi-info-circle me-1"></i>
                  Tối thiểu: 50,000 VNĐ (chỉ nhập số nguyên)
                </small>
              </div>

              {error && (
                <div className="alert alert-danger">
                  <i className="bi bi-exclamation-circle me-2"></i>
                  {error}
                </div>
              )}

              <div className="d-grid gap-2">
                <button
                  className="btn btn-primary btn-lg"
                  onClick={handleGenerateQR}
                  disabled={loading || !amount}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Đang tạo...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-qr-code me-2"></i>
                      Tạo QR
                    </>
                  )}
                </button>

                {transferContent && (
                  <button
                    className="btn btn-success btn-lg"
                    onClick={handleSubmitPayment}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2"></span>
                        Đang gửi...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-check-circle me-2"></i>
                        Đã thanh toán
                      </>
                    )}
                  </button>
                )}

                <button
                  className="btn btn-outline-secondary"
                  onClick={handleReset}
                  disabled={loading}
                >
                  <i className="bi bi-arrow-clockwise me-2"></i>
                  Reset
                </button>
              </div>

              <div className="alert alert-info mt-3">
                <h6 className="alert-heading">
                  <i className="bi bi-lightbulb me-2"></i>
                  Hướng dẫn:
                </h6>
                <ol className="mb-0 small">
                  <li>Nhập số tiền muốn nạp (tối thiểu 50,000 VNĐ)</li>
                  <li>Nhấn "Tạo QR" để tạo QR code</li>
                  <li>Quét QR code bằng app ngân hàng</li>
                  <li>Copy nội dung chuyển khoản và paste khi chuyển tiền</li>
                  <li>Sau khi chuyển khoản, liên hệ admin để xác nhận</li>
                </ol>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modal thông báo đã gửi yêu cầu */}
      {showSuccessModal && (
        <div className="modal fade show" style={{ display: 'block', backgroundColor: 'rgba(0,0,0,0.5)' }}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header bg-success text-white">
                <h5 className="modal-title">
                  <i className="bi bi-check-circle me-2"></i>
                  Đã gửi yêu cầu nạp tiền
                </h5>
                <button 
                  type="button" 
                  className="btn-close btn-close-white" 
                  onClick={() => setShowSuccessModal(false)}
                ></button>
              </div>
              <div className="modal-body">
                <div className="alert alert-info">
                  <h6 className="alert-heading">
                    <i className="bi bi-clock-history me-2"></i>
                    Đang xử lý giao dịch
                  </h6>
                  <p className="mb-0">
                    Vui lòng chờ từ <strong>10-15 phút</strong>, số tiền sẽ được cộng vào tài khoản của bạn sau khi admin duyệt.
                  </p>
                </div>
                {submittedAmount && (
                  <div className="text-center">
                    <p className="mb-1">Số tiền đã gửi:</p>
                    <h4 className="text-success">
                      {new Intl.NumberFormat('vi-VN').format(submittedAmount)} VNĐ
                    </h4>
                  </div>
                )}
              </div>
              <div className="modal-footer">
                <button 
                  type="button" 
                  className="btn btn-primary"
                  onClick={() => {
                    setShowSuccessModal(false)
                    navigate('/dashboard')
                  }}
                >
                  Về Dashboard
                </button>
                <button 
                  type="button" 
                  className="btn btn-secondary"
                  onClick={() => setShowSuccessModal(false)}
                >
                  Ở lại trang này
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

