import { Link } from 'react-router-dom'

export default function SecurityPolicy() {
  return (
    <div className="container my-5" style={{ paddingTop: '100px' }}>
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card-soft">
            <div className="mb-4">
              <Link to="/courses" className="text-decoration-none text-brand-sky">
                <i className="bi bi-arrow-left me-2"></i>Về trang chủ
              </Link>
            </div>
            
            <h1 className="title-gradient mb-4">
              <i className="bi bi-shield-check me-2"></i>Chính sách an toàn
            </h1>

            <div className="content-section">
              <h3 className="mb-3">1. Bảo mật thông tin cá nhân</h3>
              <p>
                Code Đơ cam kết bảo vệ thông tin cá nhân của người dùng. Tất cả thông tin được mã hóa 
                và lưu trữ an toàn trên hệ thống.
              </p>
              <ul>
                <li className="mb-2">Thông tin đăng nhập được mã hóa bằng bcrypt</li>
                <li className="mb-2">Giao dịch được bảo mật bằng JWT tokens</li>
                <li className="mb-2">Không chia sẻ thông tin cá nhân với bên thứ ba</li>
                <li className="mb-2">Tuân thủ các quy định về bảo vệ dữ liệu cá nhân</li>
              </ul>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">2. Bảo mật giao dịch</h3>
              <p>
                Tất cả các giao dịch nạp tiền và thanh toán đều được xử lý an toàn:
              </p>
              <ul>
                <li className="mb-2">Mỗi giao dịch có mã giao dịch duy nhất</li>
                <li className="mb-2">Giao dịch được xác thực bởi admin trước khi cộng tiền</li>
                <li className="mb-2">Lịch sử giao dịch được lưu trữ đầy đủ</li>
                <li className="mb-2">Không lưu trữ thông tin thẻ ngân hàng trên hệ thống</li>
              </ul>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">3. Bảo vệ tài khoản</h3>
              <p>Để bảo vệ tài khoản của bạn:</p>
              <ul>
                <li className="mb-2">Sử dụng mật khẩu mạnh (ít nhất 8 ký tự, có chữ hoa, chữ thường, số)</li>
                <li className="mb-2">Không chia sẻ thông tin đăng nhập với người khác</li>
                <li className="mb-2">Đăng xuất sau khi sử dụng trên thiết bị công cộng</li>
                <li className="mb-2">Báo cáo ngay nếu phát hiện hoạt động đáng ngờ</li>
              </ul>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">4. Quyền riêng tư</h3>
              <p>
                Code Đơ tôn trọng quyền riêng tư của người dùng:
              </p>
              <ul>
                <li className="mb-2">Thông tin cá nhân chỉ được sử dụng cho mục đích cung cấp dịch vụ</li>
                <li className="mb-2">Không gửi email quảng cáo không mong muốn</li>
                <li className="mb-2">Người dùng có quyền yêu cầu xóa tài khoản và dữ liệu</li>
                <li className="mb-2">Thông tin học tập được bảo mật và chỉ hiển thị cho giáo viên liên quan</li>
              </ul>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">5. Báo cáo sự cố bảo mật</h3>
              <p>
                Nếu bạn phát hiện lỗ hổng bảo mật hoặc hoạt động đáng ngờ, vui lòng:
              </p>
              <ul>
                <li className="mb-2">Liên hệ ngay với admin qua email: <a href="mailto:support@codedo.com">support@codedo.com</a></li>
                <li className="mb-2">Mô tả chi tiết vấn đề bạn gặp phải</li>
                <li className="mb-2">Cung cấp thông tin cần thiết để xác minh</li>
                <li className="mb-2">Không chia sẻ thông tin lỗ hổng công khai trước khi được xử lý</li>
              </ul>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">6. Cập nhật chính sách</h3>
              <p>
                Code Đơ có quyền cập nhật chính sách an toàn này. Người dùng sẽ được thông báo 
                về các thay đổi quan trọng qua email hoặc thông báo trên website.
              </p>
              <p className="text-muted">
                <strong>Lần cập nhật cuối:</strong> {new Date().toLocaleDateString('vi-VN')}
              </p>
            </div>

            <div className="mt-4 pt-4 border-top">
              <p className="text-muted mb-0">
                <i className="bi bi-info-circle me-2"></i>
                Nếu bạn có câu hỏi về chính sách an toàn, vui lòng liên hệ: 
                <a href="mailto:support@codedo.com" className="ms-1">support@codedo.com</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

