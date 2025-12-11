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
      const response = await axios.post(
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

      // TODO: Redirect đến cổng thanh toán thật (Momo/ZaloPay/PayPal)
      // Hiện tại chỉ giả lập
      alert(`Đã tạo đơn hàng: ${response.data.ma_don_hang}\n\nTrong môi trường thật, bạn sẽ được chuyển đến cổng thanh toán ${paymentMethod.toUpperCase()}.`)
      
      // Giả lập thanh toán thành công (trong thực tế sẽ nhận callback từ cổng thanh toán)
      // Tạm thời tự động đăng ký khóa học
      if (onSuccess) {
        onSuccess()
      }
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || 'Tạo đơn hàng thất bại')
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
                  <label className="form-label fw-bold">Chọn phương thức thanh toán:</label>
                  <div className="d-flex flex-column gap-2">
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="momo"
                        value="momo"
                        checked={paymentMethod === 'momo'}
                        onChange={(e) => setPaymentMethod(e.target.value)}
                      />
                      <label className="form-check-label" htmlFor="momo">
                        <i className="bi bi-phone me-2"></i>
                        Ví MoMo
                      </label>
                    </div>
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="zalopay"
                        value="zalopay"
                        checked={paymentMethod === 'zalopay'}
                        onChange={(e) => setPaymentMethod(e.target.value)}
                      />
                      <label className="form-check-label" htmlFor="zalopay">
                        <i className="bi bi-wallet2 me-2"></i>
                        ZaloPay
                      </label>
                    </div>
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="paypal"
                        value="paypal"
                        checked={paymentMethod === 'paypal'}
                        onChange={(e) => setPaymentMethod(e.target.value)}
                      />
                      <label className="form-check-label" htmlFor="paypal">
                        <i className="bi bi-paypal me-2"></i>
                        PayPal
                      </label>
                    </div>
                    <div className="form-check">
                      <input
                        className="form-check-input"
                        type="radio"
                        name="paymentMethod"
                        id="bank"
                        value="bank_transfer"
                        checked={paymentMethod === 'bank_transfer'}
                        onChange={(e) => setPaymentMethod(e.target.value)}
                      />
                      <label className="form-check-label" htmlFor="bank">
                        <i className="bi bi-bank me-2"></i>
                        Chuyển khoản ngân hàng
                      </label>
                    </div>
                  </div>
                </div>

                {error && (
                  <div className="alert alert-danger">
                    <i className="bi bi-exclamation-circle me-2"></i>
                    {error}
                  </div>
                )}

                <div className="alert alert-info">
                  <i className="bi bi-info-circle me-2"></i>
                  <small>
                    <strong>Lưu ý:</strong> Hiện tại đang ở chế độ demo. 
                    Trong môi trường thật, bạn sẽ được chuyển đến cổng thanh toán để hoàn tất giao dịch.
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

