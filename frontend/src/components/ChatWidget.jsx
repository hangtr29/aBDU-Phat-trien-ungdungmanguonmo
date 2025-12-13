import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { useAuth } from '../context/AuthContext'
import './ChatWidget.css'

function ChatWidget() {
  const { user } = useAuth()
  const [isOpen, setIsOpen] = useState(false)
  const [conversations, setConversations] = useState([])
  const [availableUsers, setAvailableUsers] = useState([])
  const [selectedConversation, setSelectedConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [newMessage, setNewMessage] = useState('')
  const [unreadCount, setUnreadCount] = useState(0)
  const [loading, setLoading] = useState(false)
  const [showAvailableUsers, setShowAvailableUsers] = useState(false)
  const messagesEndRef = useRef(null)
  const messagesContainerRef = useRef(null)

  useEffect(() => {
    if (user && isOpen) {
      fetchConversations()
      fetchAvailableUsers()
      if (selectedConversation) {
        fetchMessages(selectedConversation.user_id)
      }
    }
  }, [user, isOpen, selectedConversation])

  useEffect(() => {
    // Auto scroll to bottom when new messages arrive
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [messages])

  useEffect(() => {
    // Poll for unread count
    if (user) {
      fetchUnreadCount()
      const interval = setInterval(fetchUnreadCount, 5000) // Check every 5 seconds
      return () => clearInterval(interval)
    }
  }, [user])

  const fetchConversations = async () => {
    try {
      const response = await axios.get('/api/messages/conversations')
      setConversations(response.data)
    } catch (error) {
      console.error('Failed to fetch conversations:', error)
    }
  }

  const fetchAvailableUsers = async () => {
    try {
      const response = await axios.get('/api/messages/available-users')
      setAvailableUsers(response.data)
    } catch (error) {
      console.error('Failed to fetch available users:', error)
    }
  }

  const fetchMessages = async (otherUserId) => {
    try {
      setLoading(true)
      const response = await axios.get(`/api/messages/conversations/${otherUserId}`)
      setMessages(response.data)
      // Update unread count after fetching messages
      fetchUnreadCount()
      fetchConversations()
    } catch (error) {
      console.error('Failed to fetch messages:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchUnreadCount = async () => {
    try {
      const response = await axios.get('/api/messages/unread-count')
      setUnreadCount(response.data.unread_count || 0)
    } catch (error) {
      console.error('Failed to fetch unread count:', error)
    }
  }

  const handleSendMessage = async (e) => {
    e.preventDefault()
    if (!newMessage.trim() || !selectedConversation) return

    try {
      await axios.post('/api/messages', {
        receiver_id: selectedConversation.user_id,
        noi_dung: newMessage
      })
      setNewMessage('')
      // Refresh messages
      fetchMessages(selectedConversation.user_id)
      fetchConversations()
    } catch (error) {
      alert('Gửi tin nhắn thất bại: ' + (error.response?.data?.detail || error.message))
    }
  }

  const handleSelectConversation = (conversation) => {
    setSelectedConversation(conversation)
    fetchMessages(conversation.user_id)
  }

  const formatTime = (dateString) => {
    if (!dateString) return ''
    const date = new Date(dateString)
    const now = new Date()
    const diff = now - date
    const minutes = Math.floor(diff / 60000)
    
    if (minutes < 1) return 'Vừa xong'
    if (minutes < 60) return `${minutes} phút trước`
    if (minutes < 1440) return `${Math.floor(minutes / 60)} giờ trước`
    return date.toLocaleDateString('vi-VN')
  }

  if (!user) return null

  return (
    <div className="chat-widget">
      {/* Chat Button */}
      <button
        className="chat-button"
        onClick={() => setIsOpen(!isOpen)}
        title="Nhắn tin"
      >
        <i className="bi bi-chat-dots"></i>
        {unreadCount > 0 && (
          <span className="chat-badge">{unreadCount > 99 ? '99+' : unreadCount}</span>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <h5 className="mb-0">
              <i className="bi bi-chat-dots me-2"></i>
              Nhắn tin
            </h5>
            <button
              className="btn btn-sm btn-link text-white"
              onClick={() => {
                setIsOpen(false)
                setSelectedConversation(null)
                setMessages([])
              }}
            >
              <i className="bi bi-x-lg"></i>
            </button>
          </div>

          <div className="chat-body">
            {!selectedConversation ? (
              // Conversations List
              <div className="conversations-list">
                <div className="conversations-header p-2 border-bottom">
                  <div className="d-flex justify-content-between align-items-center">
                    <strong>Cuộc trò chuyện</strong>
                    <button
                      className="btn btn-sm btn-outline-primary"
                      onClick={() => {
                        setShowAvailableUsers(!showAvailableUsers)
                        if (!showAvailableUsers) {
                          fetchAvailableUsers()
                        }
                      }}
                    >
                      <i className="bi bi-plus-lg"></i> Mới
                    </button>
                  </div>
                </div>
                
                {showAvailableUsers && availableUsers.length > 0 && (
                  <div className="available-users-section border-bottom">
                    <div className="p-2 bg-light">
                      <small className="text-muted">Bắt đầu cuộc trò chuyện mới:</small>
                    </div>
                    {availableUsers.map((user) => (
                      <div
                        key={user.user_id}
                        className="conversation-item"
                        onClick={() => {
                          handleSelectConversation(user)
                          setShowAvailableUsers(false)
                        }}
                      >
                        <div className="d-flex align-items-center">
                          <strong>{user.user_name}</strong>
                          {user.user_role === 'teacher' && (
                            <span className="badge bg-danger ms-2" style={{ fontSize: '0.65rem' }}>
                              <i className="bi bi-person-badge"></i> Giáo viên
                            </span>
                          )}
                          {user.user_role === 'admin' && (
                            <span className="badge bg-primary ms-2" style={{ fontSize: '0.65rem' }}>
                              <i className="bi bi-shield-check"></i> Admin
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {conversations.length === 0 && !showAvailableUsers ? (
                  <div className="text-center text-muted p-4">
                    <i className="bi bi-inbox" style={{ fontSize: '3rem' }}></i>
                    <p className="mt-2">Chưa có cuộc trò chuyện nào</p>
                    <button
                      className="btn btn-sm btn-primary mt-2"
                      onClick={() => {
                        setShowAvailableUsers(true)
                        fetchAvailableUsers()
                      }}
                    >
                      <i className="bi bi-plus-lg"></i> Bắt đầu cuộc trò chuyện
                    </button>
                  </div>
                ) : (
                  conversations.map((conv) => (
                    <div
                      key={conv.user_id}
                      className={`conversation-item ${selectedConversation?.user_id === conv.user_id ? 'active' : ''}`}
                      onClick={() => handleSelectConversation(conv)}
                    >
                      <div className="d-flex justify-content-between align-items-start">
                        <div className="flex-grow-1">
                          <div className="d-flex align-items-center">
                            <strong>{conv.user_name}</strong>
                            {conv.user_role === 'teacher' && (
                              <span className="badge bg-danger ms-2" style={{ fontSize: '0.65rem' }}>
                                <i className="bi bi-person-badge"></i> Giáo viên
                              </span>
                            )}
                            {conv.user_role === 'admin' && (
                              <span className="badge bg-primary ms-2" style={{ fontSize: '0.65rem' }}>
                                <i className="bi bi-shield-check"></i> Admin
                              </span>
                            )}
                          </div>
                          {conv.last_message && (
                            <small className="text-muted d-block text-truncate" style={{ maxWidth: '200px' }}>
                              {conv.last_message}
                            </small>
                          )}
                        </div>
                        <div className="text-end">
                          {conv.last_message_time && (
                            <small className="text-muted d-block">
                              {formatTime(conv.last_message_time)}
                            </small>
                          )}
                          {conv.unread_count > 0 && (
                            <span className="badge bg-danger rounded-pill">
                              {conv.unread_count > 99 ? '99+' : conv.unread_count}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            ) : (
              // Messages View
              <div className="messages-view">
                <div className="messages-header">
                  <button
                    className="btn btn-sm btn-link"
                    onClick={() => setSelectedConversation(null)}
                  >
                    <i className="bi bi-arrow-left"></i>
                  </button>
                  <div className="flex-grow-1 ms-2">
                    <strong>{selectedConversation.user_name}</strong>
                    {selectedConversation.user_role === 'teacher' && (
                      <span className="badge bg-danger ms-2" style={{ fontSize: '0.7rem' }}>
                        <i className="bi bi-person-badge"></i> Giáo viên
                      </span>
                    )}
                    {selectedConversation.user_role === 'admin' && (
                      <span className="badge bg-primary ms-2" style={{ fontSize: '0.7rem' }}>
                        <i className="bi bi-shield-check"></i> Admin
                      </span>
                    )}
                  </div>
                </div>

                <div className="messages-container" ref={messagesContainerRef}>
                  {loading ? (
                    <div className="text-center p-4">
                      <div className="spinner-border spinner-border-sm" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    </div>
                  ) : messages.length === 0 ? (
                    <div className="text-center text-muted p-4">
                      <p>Chưa có tin nhắn nào</p>
                    </div>
                  ) : (
                    messages.map((msg) => {
                      const isSent = msg.sender_id === user.id
                      return (
                        <div
                          key={msg.id}
                          className={`message-bubble ${isSent ? 'sent' : 'received'}`}
                        >
                          <div className="message-content">
                            {msg.noi_dung}
                          </div>
                          <small className="message-time">
                            {formatTime(msg.created_at)}
                          </small>
                        </div>
                      )
                    })
                  )}
                  <div ref={messagesEndRef} />
                </div>

                <form onSubmit={handleSendMessage} className="messages-input">
                  <div className="input-group">
                    <input
                      type="text"
                      className="form-control"
                      placeholder="Nhập tin nhắn..."
                      value={newMessage}
                      onChange={(e) => setNewMessage(e.target.value)}
                    />
                    <button className="btn btn-primary" type="submit" disabled={!newMessage.trim()}>
                      <i className="bi bi-send"></i>
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatWidget









