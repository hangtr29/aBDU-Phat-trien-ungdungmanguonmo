import { Link } from 'react-router-dom'

export default function TransactionGuide() {
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
              <i className="bi bi-book me-2"></i>Hướng dẫn giao dịch
            </h1>

            <div className="content-section">
              <h3 className="mb-3">1. Nạp tiền vào tài khoản</h3>
              <ol>
                <li className="mb-2">Truy cập trang <Link to="/addfunds">Nạp tiền</Link> từ menu hoặc header</li>
                <li className="mb-2">Nhập số tiền muốn nạp (tối thiểu 50,000 VNĐ)</li>
                <li className="mb-2">Click nút "Tạo QR" để tạo mã QR và nội dung chuyển khoản</li>
                <li className="mb-2">Quét QR code hoặc chuyển khoản theo thông tin được cung cấp</li>
                <li className="mb-2">Sau khi chuyển khoản, click nút "Đã thanh toán"</li>
                <li className="mb-2">Chờ admin duyệt giao dịch (thường từ 10-15 phút)</li>
                <li className="mb-2">Số tiền sẽ được cộng vào tài khoản sau khi được duyệt</li>
              </ol>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">2. Thanh toán khóa học</h3>
              <ol>
                <li className="mb-2">Chọn khóa học muốn mua</li>
                <li className="mb-2">Click nút "Mua khóa học" hoặc "Đăng ký"</li>
                <li className="mb-2">Kiểm tra số dư trong ví của bạn</li>
                <li className="mb-2">Nếu số dư đủ, số tiền sẽ tự động được trừ khi mua khóa học</li>
                <li className="mb-2">Nếu số dư không đủ, bạn sẽ được chuyển đến trang nạp tiền</li>
                <li className="mb-2">Sau khi mua thành công, bạn có thể truy cập khóa học ngay</li>
              </ol>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">3. Thông tin tài khoản ngân hàng</h3>
              <div className="alert alert-info">
                <strong>Số tài khoản:</strong> 0377070269<br />
                <strong>Tên người nhận:</strong> LE GIA BAO<br />
                <strong>Ngân hàng:</strong> Vietcombank
              </div>
              <p className="text-muted">
                <strong>Lưu ý:</strong> Khi chuyển khoản, vui lòng nhập đúng nội dung chuyển khoản được cung cấp 
                để hệ thống có thể tự động nhận diện giao dịch của bạn.
              </p>
            </div>

            <div className="content-section mt-4">
              <h3 className="mb-3">4. Xử lý sự cố</h3>
              <ul>
                <li className="mb-2">
                  <strong>Giao dịch chưa được duyệt sau 15 phút:</strong> 
                  Vui lòng liên hệ admin qua email hoặc chat để được hỗ trợ
                </li>
                <li className="mb-2">
                  <strong>Chuyển khoản sai nội dung:</strong> 
                  Liên hệ admin với mã giao dịch để được xử lý thủ công
                </li>
                <li className="mb-2">
                  <strong>Số tiền không khớp:</strong> 
                  Admin sẽ kiểm tra và điều chỉnh số tiền nếu cần
                </li>
              </ul>
            </div>

            <div className="mt-4 pt-4 border-top">
              <p className="text-muted mb-0">
                <i className="bi bi-info-circle me-2"></i>
                Nếu bạn có thắc mắc, vui lòng liên hệ bộ phận hỗ trợ qua email: 
                <a href="mailto:support@codedo.com" className="ms-1">support@codedo.com</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

