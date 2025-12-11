import { useState } from 'react'
import axios from 'axios'

export default function PaymentModal({ course, onClose, onSuccess }) {
  const [paymentMethod, setPaymentMethod] = useState('momo')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handlePayment = async () => {
    if (!course || !course.gia || course.gia <= 0) {
      setError('Khóa học này miễn phí, không cần thanh toán')
      return
    }

    setLoading(true)
    setError('')

    try {
      const token = localStorage.getItem('token')
      
      // Tạo payment record
      const createResponse = await axios.post(
        '/api/payments/create',
        {
          khoa_hoc_id: course.id,
          phuong_thuc: paymentMethod,
          so_tien: parseFloat(course.gia)
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      // Giả lập thanh toán thành công ngay lập tức (demo mode)
      await axios.post(
        '/api/payments/demo-complete',
        {
          ma_don_hang: createResponse.data.ma_don_hang
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

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

                <div className="mb-3">
                  <label className="form-label fw-bold">Phương thức thanh toán:</label>
                  <select
                    className="form-select"
                    value={paymentMethod}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    disabled={loading}
                  >
                    <option value="momo">Ví MoMo</option>
                    <option value="zalopay">ZaloPay</option>
                    <option value="paypal">PayPal</option>
                    <option value="bank_transfer">Chuyển khoản ngân hàng</option>
                  </select>
                </div>

                {error && (
                  <div className="alert alert-danger">
                    <i className="bi bi-exclamation-circle me-2"></i>
                    {error}
                  </div>
                )}

                <div className="alert alert-warning">
                  <i className="bi bi-info-circle me-2"></i>
                  <small>
                    <strong>Chế độ demo:</strong> Thanh toán sẽ được xử lý tự động để demo. 
                    Trong môi trường thật, bạn sẽ được chuyển đến cổng thanh toán thực tế.
                  </small>
                </div>
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
              disabled={loading}
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
    </div>
  )
}

