import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="footer-custom mt-5">
      <div className="container">
        <div className="row g-4">
          {/* Giới thiệu */}
          <div className="col-md-4">
            <h5 className="footer-section-title">
              <i className="bi bi-info-circle"></i>
              Giới thiệu
            </h5>
            <p className="footer-tagline">
              Code Đơ là nền tảng học lập trình trực tuyến hàng đầu, cung cấp các khóa học chất lượng cao 
              cho mọi trình độ từ cơ bản đến nâng cao.
            </p>
          </div>

          {/* Liên hệ */}
          <div className="col-md-4">
            <h5 className="footer-section-title">
              <i className="bi bi-envelope"></i>
              Liên hệ
            </h5>
            <ul className="footer-links">
              <li>
                <a href="mailto:support@codedo.com">
                  <i className="bi bi-envelope-fill"></i> support@codedo.com
                </a>
              </li>
              <li>
                <a href="tel:+84123456789">
                  <i className="bi bi-telephone-fill"></i> +84 123 456 789
                </a>
              </li>
              <li>
                <a href="#">
                  <i className="bi bi-geo-alt-fill"></i> 123 Đường ABC, Quận XYZ, TP.HCM
                </a>
              </li>
            </ul>
          </div>

          {/* Code Đơ - Links */}
          <div className="col-md-4">
            <h5 className="footer-section-title">
              <i className="bi bi-link-45deg"></i>
              Code Đơ
            </h5>
            <ul className="footer-links">
              <li>
                <Link to="/courses">
                  <i className="bi bi-house-door"></i> Trang chủ
                </Link>
              </li>
              <li>
                <Link to="/transaction-guide">
                  <i className="bi bi-book"></i> Hướng dẫn giao dịch
                </Link>
              </li>
              <li>
                <Link to="/security-policy">
                  <i className="bi bi-shield-check"></i> Chính sách an toàn
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Social Icons */}
        <div className="text-center mt-4">
          <div className="footer-social-icons">
            <a 
              href="https://www.facebook.com/ngochang.tranthi.7543" 
              target="_blank" 
              rel="noopener noreferrer"
              className="footer-social-icon" 
              title="Facebook"
            >
              <i className="bi bi-facebook"></i>
            </a>
            <a 
              href="https://www.youtube.com/user/binhduonguniversity" 
              target="_blank" 
              rel="noopener noreferrer"
              className="footer-social-icon" 
              title="YouTube"
            >
              <i className="bi bi-youtube"></i>
            </a>
            <a 
              href="https://github.com/legiabao01/BDU-Phat-trien-ungdungmanguonmo" 
              target="_blank" 
              rel="noopener noreferrer"
              className="footer-social-icon" 
              title="GitHub"
            >
              <i className="bi bi-github"></i>
            </a>
          </div>
        </div>

        {/* Copyright */}
        <div className="border-top mt-4 pt-4 text-center">
          <p className="mb-0" style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
            &copy; {new Date().getFullYear()} Code Đơ. Tất cả quyền được bảo lưu.
          </p>
        </div>
      </div>
    </footer>
  )
}

