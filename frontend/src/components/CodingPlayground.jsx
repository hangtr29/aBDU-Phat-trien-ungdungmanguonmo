import { useState } from 'react'
import axios from 'axios'

export default function CodingPlayground({ lessonId, courseId }) {
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [stdin, setStdin] = useState('')
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [executionTime, setExecutionTime] = useState(null)

  const handleRun = async () => {
    if (!code.trim()) {
      setError('Vui lòng nhập code!')
      return
    }

    setLoading(true)
    setOutput('')
    setError('')
    setExecutionTime(null)

    try {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        '/api/code/execute',
        {
          code: code,
          language: language,
          stdin: stdin || null
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      if (response.data.error) {
        setError(response.data.error)
      } else {
        setOutput(response.data.output || '(Không có output)')
      }
      setExecutionTime(response.data.execution_time)
    } catch (err) {
      setError(err.response?.data?.detail || 'Lỗi khi chạy code')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setCode('')
    setStdin('')
    setOutput('')
    setError('')
    setExecutionTime(null)
  }

  const codeTemplates = {
    python: `# Nhập code Python của bạn ở đây
print("Hello, World!")
`,
    javascript: `// Nhập code JavaScript của bạn ở đây
console.log("Hello, World!");
`,
    cpp: `#include <iostream>
using namespace std;

int main() {
    cout << "Hello, World!" << endl;
    return 0;
}
`,
    java: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
`
  }

  const handleLanguageChange = (e) => {
    const newLang = e.target.value
    setLanguage(newLang)
    if (!code.trim() || code === codeTemplates[language]) {
      setCode(codeTemplates[newLang] || '')
    }
  }

  return (
    <div className="coding-playground mt-4">
      <div className="card">
        <div className="card-header bg-primary text-white">
          <div className="d-flex justify-content-between align-items-center">
            <h5 className="mb-0">
              <i className="bi bi-code-square me-2"></i>
              Coding Playground
            </h5>
            <div className="d-flex gap-2">
              <select
                className="form-select form-select-sm"
                value={language}
                onChange={handleLanguageChange}
                disabled={loading}
                style={{ width: 'auto' }}
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="cpp">C++</option>
                <option value="java">Java</option>
              </select>
              <button
                className="btn btn-sm btn-light"
                onClick={handleRun}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Đang chạy...
                  </>
                ) : (
                  <>
                    <i className="bi bi-play-fill me-2"></i>
                    Chạy code
                  </>
                )}
              </button>
              <button
                className="btn btn-sm btn-outline-light"
                onClick={handleClear}
                disabled={loading}
              >
                <i className="bi bi-x-circle me-2"></i>
                Xóa
              </button>
            </div>
          </div>
        </div>

        <div className="card-body p-0">
          <div className="row g-0">
            {/* Code Editor */}
            <div className="col-md-6 border-end">
              <div className="p-3">
                <label className="form-label fw-bold">
                  <i className="bi bi-file-code me-2"></i>
                  Code Editor
                </label>
                <textarea
                  className="form-control font-monospace"
                  rows="15"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder={`Nhập code ${language} của bạn...`}
                  disabled={loading}
                  style={{
                    fontSize: '14px',
                    fontFamily: 'Consolas, Monaco, "Courier New", monospace',
                    backgroundColor: '#f8f9fa',
                    border: '1px solid #dee2e6'
                  }}
                />
              </div>
            </div>

            {/* Output & Input */}
            <div className="col-md-6">
              <div className="p-3">
                <label className="form-label fw-bold">
                  <i className="bi bi-terminal me-2"></i>
                  Input (stdin) - Tùy chọn
                </label>
                <textarea
                  className="form-control font-monospace mb-3"
                  rows="3"
                  value={stdin}
                  onChange={(e) => setStdin(e.target.value)}
                  placeholder="Nhập input cho chương trình (nếu cần)..."
                  disabled={loading}
                  style={{
                    fontSize: '14px',
                    fontFamily: 'Consolas, Monaco, "Courier New", monospace'
                  }}
                />

                <label className="form-label fw-bold">
                  <i className="bi bi-display me-2"></i>
                  Output
                </label>
                <div
                  className="form-control font-monospace"
                  style={{
                    minHeight: '200px',
                    maxHeight: '300px',
                    overflowY: 'auto',
                    backgroundColor: '#1e1e1e',
                    color: '#d4d4d4',
                    fontSize: '14px',
                    fontFamily: 'Consolas, Monaco, "Courier New", monospace',
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    border: '1px solid #333'
                  }}
                >
                  {loading ? (
                    <div className="text-center text-muted py-3">
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Đang chạy code...
                    </div>
                  ) : error ? (
                    <div className="text-danger">
                      <strong>Lỗi:</strong><br />
                      {error}
                    </div>
                  ) : output ? (
                    <div className="text-success">
                      {output}
                    </div>
                  ) : (
                    <div className="text-muted">
                      Kết quả sẽ hiển thị ở đây...
                    </div>
                  )}
                </div>

                {executionTime !== null && (
                  <div className="mt-2">
                    <small className="text-muted">
                      <i className="bi bi-stopwatch me-1"></i>
                      Thời gian thực thi: {executionTime.toFixed(3)}s
                    </small>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="card-footer bg-light">
          <small className="text-muted">
            <i className="bi bi-info-circle me-1"></i>
            <strong>Lưu ý:</strong> Code được chạy trên server với timeout 10 giây. 
            Một số thư viện có thể không được hỗ trợ.
          </small>
        </div>
      </div>
    </div>
  )
}

