import { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [loading, setLoading] = useState(true)

  // Setup axios interceptor để xử lý lỗi 401 (token hết hạn)
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token hết hạn hoặc không hợp lệ
          const errorDetail = error.response?.data?.detail || ''
          if (errorDetail.includes('token') || errorDetail.includes('Invalid') || errorDetail.includes('expired')) {
            // Xóa token và logout
            logout()
            // Redirect về trang login nếu không phải đang ở trang login
            if (!window.location.pathname.includes('/login')) {
              window.location.href = '/login'
            }
          }
        }
        return Promise.reject(error)
      }
    )

    return () => {
      axios.interceptors.response.eject(interceptor)
    }
  }, [])

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      setLoading(false)
    }
  }, [token])

  const fetchUser = async () => {
    try {
      const response = await axios.get('/api/users/me')
      const data = response.data || {}
      // Map role -> vai_tro để router/dashboard hoạt động đúng
      setUser({ ...data, vai_tro: data.role || data.vai_tro })
    } catch (error) {
      console.error('Failed to fetch user:', error)
      logout()
    } finally {
      setLoading(false)
    }
  }

  const login = async (email, password) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      const { access_token } = response.data
      setToken(access_token)
      localStorage.setItem('token', access_token)
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
      await fetchUser()
      
      // Kiểm tra bài tập sắp hết hạn (chạy background, không cần đợi)
      // Tạm thời comment để tránh lỗi
      // axios.post('/api/check-deadlines').catch(err => {
      //   console.log('Failed to check deadlines:', err)
      // })
      
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Đăng nhập thất bại' }
    }
  }

  const register = async (email, password, ho_ten, so_dien_thoai) => {
    try {
      await axios.post('/api/auth/register', {
        email,
        password,
        ho_ten,
        so_dien_thoai
      })
      return { success: true }
    } catch (error) {
      return { success: false, error: error.response?.data?.detail || 'Đăng ký thất bại' }
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    delete axios.defaults.headers.common['Authorization']
  }

  return (
    <AuthContext.Provider value={{ user, setUser, token, login, register, logout, loading, fetchUser }}>
      {children}
    </AuthContext.Provider>
  )
}



