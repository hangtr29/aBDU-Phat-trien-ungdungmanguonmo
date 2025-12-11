import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'

export default function NotificationBell() {
  const { user } = useAuth()
  const [notifications, setNotifications] = useState([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [showDropdown, setShowDropdown] = useState(false)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (user) {
      fetchNotifications()
      fetchUnreadCount()
      // Poll mỗi 30 giây
      const interval = setInterval(() => {
        fetchUnreadCount()
      }, 30000)
      return () => clearInterval(interval)
    }
  }, [user])

  const fetchNotifications = async () => {
    try {
      const response = await axios.get('/api/notifications?unread_only=true')
      setNotifications(response.data)
    } catch (error) {
      console.error('Failed to fetch notifications:', error)
    }
  }

  const fetchUnreadCount = async () => {
    try {
      const response = await axios.get('/api/notifications/unread-count')
      setUnreadCount(response.data.count)
    } catch (error) {
      console.error('Failed to fetch unread count:', error)
    }
  }

  const handleMarkAsRead = async (notificationId) => {
    try {
      await axios.put(`/api/notifications/${notificationId}/read`)
      fetchNotifications()
      fetchUnreadCount()
    } catch (error) {
      console.error('Failed to mark as read:', error)
    }
  }

  const handleMarkAllAsRead = async () => {
    setLoading(true)
    try {
      await axios.put('/api/notifications/read-all')
      fetchNotifications()
      fetchUnreadCount()
    } catch (error) {
      console.error('Failed to mark all as read:', error)
    } finally {
      setLoading(false)
    }
  }

  const getNotificationIcon = (loai) => {
    switch (loai) {
      case 'submission':
        return 'bi-file-earmark-check'
      case 'discussion':
        return 'bi-chat-dots'
      case 'grade':
        return 'bi-star-fill'
      default:
        return 'bi-bell'
    }
  }

  const getNotificationColor = (loai) => {
    switch (loai) {
      case 'submission':
        return 'text-primary'
      case 'discussion':
        return 'text-info'
      case 'grade':
        return 'text-warning'
      default:
        return 'text-secondary'
    }
  }

  if (!user) return null

  return (
    <div className="position-relative">
      <button
        className="btn btn-link text-dark position-relative"
        onClick={() => {
          setShowDropdown(!showDropdown)
          if (!showDropdown) {
            fetchNotifications()
          }
        }}
        style={{ fontSize: '1.25rem' }}
      >
        <i className="bi bi-bell"></i>
        {unreadCount > 0 && (
          <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger" style={{ fontSize: '0.6rem' }}>
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <>
          <div
            className="position-fixed top-0 start-0 end-0 bottom-0"
            onClick={() => setShowDropdown(false)}
            style={{ zIndex: 1040 }}
          />
          <div
            className="position-absolute end-0 mt-2 bg-white rounded shadow-lg border"
            style={{ width: '350px', maxHeight: '500px', overflowY: 'auto', zIndex: 1050 }}
          >
            <div className="d-flex justify-content-between align-items-center p-3 border-bottom">
              <h6 className="mb-0">Thông báo</h6>
              {notifications.length > 0 && (
                <button
                  className="btn btn-sm btn-link p-0"
                  onClick={handleMarkAllAsRead}
                  disabled={loading}
                >
                  Đánh dấu tất cả đã đọc
                </button>
              )}
            </div>

            {notifications.length === 0 ? (
              <div className="text-center py-4 text-muted">
                <i className="bi bi-bell-slash" style={{ fontSize: '2rem' }}></i>
                <p className="mb-0 mt-2">Không có thông báo mới</p>
              </div>
            ) : (
              <div className="list-group list-group-flush">
                {notifications.map((notif) => (
                  <Link
                    key={notif.id}
                    to={notif.link || '#'}
                    className={`list-group-item list-group-item-action ${!notif.da_doc ? 'bg-light' : ''}`}
                    onClick={() => {
                      if (!notif.da_doc) {
                        handleMarkAsRead(notif.id)
                      }
                      setShowDropdown(false)
                    }}
                  >
                    <div className="d-flex align-items-start">
                      <i className={`bi ${getNotificationIcon(notif.loai)} ${getNotificationColor(notif.loai)} me-2`} style={{ fontSize: '1.25rem' }}></i>
                      <div className="flex-grow-1">
                        <h6 className="mb-1">{notif.tieu_de}</h6>
                        {notif.noi_dung && (
                          <p className="mb-1 text-muted small">{notif.noi_dung}</p>
                        )}
                        <small className="text-muted">
                          {new Date(notif.created_at).toLocaleString('vi-VN')}
                        </small>
                      </div>
                      {!notif.da_doc && (
                        <span className="badge bg-primary rounded-pill ms-2"></span>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  )
}

