import axios from 'axios'

// Lấy API base URL từ environment variable hoặc dùng default
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

// Nếu có API_BASE_URL, set baseURL cho axios
if (API_BASE_URL) {
  axios.defaults.baseURL = API_BASE_URL
}

// Thêm interceptor để tự động thêm token vào headers
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default axios

