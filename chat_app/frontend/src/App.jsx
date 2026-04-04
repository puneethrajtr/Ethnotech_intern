import './App.css'
import { useEffect, useMemo, useRef, useState } from 'react'

const API_BASE = '/api'
const WS_BASE =
  import.meta.env.VITE_WS_BASE ||
  `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}`

const parseJwt = (token) => {
  try {
    const base64 = token.split('.')[1]
    const normalized = base64.replace(/-/g, '+').replace(/_/g, '/')
    const payload = JSON.parse(atob(normalized))
    return payload
  } catch {
    return null
  }
}

function App() {
  const [authToken, setAuthToken] = useState(
    localStorage.getItem('chat_token') || '',
  )
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [email, setEmail] = useState('')
  const [registerMode, setRegisterMode] = useState(false)
  const [authError, setAuthError] = useState('')
  const [currentUserId, setCurrentUserId] = useState(null)
  const [users, setUsers] = useState([])
  const [statusLookupId, setStatusLookupId] = useState('')
  const [statusInfo, setStatusInfo] = useState(null)

  const [privateTargetId, setPrivateTargetId] = useState('')
  const [privateMessages, setPrivateMessages] = useState([])
  const [privateMessageText, setPrivateMessageText] = useState('')
  const [activeChatMode, setActiveChatMode] = useState('private')

  const [groupId, setGroupId] = useState('')
  const [groupName, setGroupName] = useState('')
  const [groupMemberId, setGroupMemberId] = useState('')
  const [groups, setGroups] = useState([])
  const [groupMessages, setGroupMessages] = useState([])
  const [groupMessageText, setGroupMessageText] = useState('')

  const [activeWsType, setActiveWsType] = useState('private')
  const [activeWsTarget, setActiveWsTarget] = useState('')
  const [wsStatus, setWsStatus] = useState('disconnected')
  const wsRef = useRef(null)
  const presenceWsRef = useRef(null)

  const authHeaders = useMemo(() => {
    if (!authToken) {
      return {}
    }
    return { Authorization: `Bearer ${authToken}` }
  }, [authToken])

  const updatePresence = async (action, tokenOverride) => {
    const token = tokenOverride || authToken
    if (!token) {
      return
    }
    await fetch(`${API_BASE}/users/presence/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ action }),
      keepalive: true,
    })
  }

  const loadUsers = async (tokenOverride) => {
    const token = tokenOverride || authToken
    if (!token) {
      return
    }
    const response = await fetch(`${API_BASE}/users/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setUsers(data)
  }

  const loadGroups = async (tokenOverride) => {
    const token = tokenOverride || authToken
    if (!token) {
      return
    }
    const response = await fetch(`${API_BASE}/groups/list/`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setGroups(data)
  }

  const initCurrentUser = (token) => {
    const payload = parseJwt(token)
    if (payload?.user_id) {
      setCurrentUserId(payload.user_id)
    }
  }

  useEffect(() => {
    if (!authToken) {
      setCurrentUserId(null)
      if (presenceWsRef.current) {
        presenceWsRef.current.close()
      }
      return
    }
    initCurrentUser(authToken)
    loadUsers()
    loadGroups()
    updatePresence('online')

    if (presenceWsRef.current) {
      presenceWsRef.current.close()
    }
    const presenceSocket = new WebSocket(
      `${WS_BASE}/ws/presence/?token=${encodeURIComponent(authToken)}`,
    )
    presenceWsRef.current = presenceSocket
    presenceSocket.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      if (payload.type !== 'presence_update') {
        return
      }
      setUsers((prev) =>
        prev.map((user) =>
          user.id === payload.user_id
            ? { ...user, is_online: payload.is_online, last_seen: payload.last_seen }
            : user,
        ),
      )
    }

    const intervalId = setInterval(() => {
      updatePresence('online')
      loadUsers()
    }, 20000)

    const handleUnload = () => {
      const payload = new Blob(
        [JSON.stringify({ action: 'offline', token: authToken })],
        {
        type: 'application/json',
        },
      )
      navigator.sendBeacon(`${API_BASE}/users/presence/`, payload)
    }

    window.addEventListener('beforeunload', handleUnload)

    return () => {
      clearInterval(intervalId)
      window.removeEventListener('beforeunload', handleUnload)
      updatePresence('offline')
      if (presenceWsRef.current) {
        presenceWsRef.current.close()
      }
    }
  }, [authToken])

  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const handleAuth = async (event) => {
    event.preventDefault()
    setAuthError('')
    if (registerMode) {
      const response = await fetch(`${API_BASE}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
      })
      if (!response.ok) {
        const errorBody = await response.json().catch(() => null)
        const detail = errorBody ? JSON.stringify(errorBody) : 'Registration failed.'
        setAuthError(detail)
        return
      }
    }

    const loginResponse = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    })
    if (!loginResponse.ok) {
      const errorBody = await loginResponse.json().catch(() => null)
      const detail = errorBody ? JSON.stringify(errorBody) : 'Login failed.'
      setAuthError(detail)
      return
    }
    const data = await loginResponse.json()
    localStorage.setItem('chat_token', data.access)
    setAuthToken(data.access)
    initCurrentUser(data.access)
    await loadUsers(data.access)
    await loadGroups(data.access)
  }

  const handleLogout = () => {
    updatePresence('offline', authToken)
    localStorage.removeItem('chat_token')
    setAuthToken('')
    setUsers([])
    setGroups([])
    setPrivateMessages([])
    setGroupMessages([])
    if (wsRef.current) {
      wsRef.current.close()
    }
  }

  const fetchPrivateHistory = async () => {
    if (!privateTargetId) {
      return
    }
    const response = await fetch(
      `${API_BASE}/messages/private/history/${privateTargetId}/`,
      { headers: authHeaders },
    )
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setPrivateMessages(data)
  }

  const fetchGroupHistory = async () => {
    if (!groupId) {
      return
    }
    const response = await fetch(`${API_BASE}/groups/${groupId}/messages/`, {
      headers: authHeaders,
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setGroupMessages(data)
  }

  const sendPrivateMessage = async () => {
    if (!privateMessageText.trim()) {
      return
    }
    if (wsRef.current && wsStatus === 'connected' && activeWsType === 'private') {
      wsRef.current.send(JSON.stringify({ content: privateMessageText }))
      setPrivateMessageText('')
      return
    }
    const response = await fetch(`${API_BASE}/messages/private/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders },
      body: JSON.stringify({ receiver_id: privateTargetId, content: privateMessageText }),
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setPrivateMessages((prev) => [...prev, data])
    setPrivateMessageText('')
  }

  const sendGroupMessage = async () => {
    if (!groupMessageText.trim()) {
      return
    }
    if (wsRef.current && wsStatus === 'connected' && activeWsType === 'group') {
      wsRef.current.send(JSON.stringify({ content: groupMessageText }))
      setGroupMessageText('')
      return
    }
    const response = await fetch(`${API_BASE}/groups/${groupId}/messages/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders },
      body: JSON.stringify({ content: groupMessageText }),
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setGroupMessages((prev) => [...prev, data])
    setGroupMessageText('')
  }

  const connectWebSocket = () => {
    if (!authToken || !activeWsTarget) {
      return
    }
    if (wsRef.current) {
      wsRef.current.close()
    }
    const socket = new WebSocket(
      `${WS_BASE}/ws/chat/${activeWsType}/${activeWsTarget}/?token=${encodeURIComponent(
        authToken,
      )}`,
    )
    wsRef.current = socket
    setWsStatus('connecting')

    socket.onopen = () => setWsStatus('connected')
    socket.onclose = () => setWsStatus('disconnected')
    socket.onerror = () => setWsStatus('error')
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data)
      if (payload.type === 'private_message') {
        setPrivateMessages((prev) => [...prev, payload])
      }
      if (payload.type === 'group_message') {
        setGroupMessages((prev) => [...prev, payload])
      }
    }
  }

  const lookupStatus = async () => {
    if (!statusLookupId) {
      return
    }
    const response = await fetch(`${API_BASE}/users/${statusLookupId}/status/`, {
      headers: authHeaders,
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setStatusInfo(data)
  }

  const createGroup = async () => {
    if (!groupName.trim()) {
      return
    }
    const response = await fetch(`${API_BASE}/groups/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders },
      body: JSON.stringify({ name: groupName }),
    })
    if (!response.ok) {
      return
    }
    const data = await response.json()
    setGroupId(String(data.id))
    setGroupName('')
    setGroups((prev) => [...prev, data])
  }

  const updateGroupMembers = async (action) => {
    if (!groupId || !groupMemberId) {
      return
    }
    await fetch(`${API_BASE}/groups/${groupId}/members/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...authHeaders },
      body: JSON.stringify({ action, user_id: Number(groupMemberId) }),
    })
  }

  const userNameById = useMemo(() => {
    const map = new Map()
    users.forEach((user) => map.set(user.id, user.username))
    return map
  }, [users])

  const activeChatTitle = useMemo(() => {
    if (activeChatMode === 'group') {
      const group = groups.find((item) => String(item.id) === String(groupId))
      return group ? group.name : 'Select a group'
    }
    if (!privateTargetId) {
      return 'Select a contact'
    }
    return userNameById.get(Number(privateTargetId)) || `User ${privateTargetId}`
  }, [activeChatMode, groupId, groups, privateTargetId, userNameById])

  const activeMessages = activeChatMode === 'group' ? groupMessages : privateMessages

  const handleSelectUser = (userId) => {
    setActiveChatMode('private')
    setPrivateTargetId(String(userId))
  }

  const handleSelectGroup = (selectedGroupId) => {
    setActiveChatMode('group')
    setGroupId(String(selectedGroupId))
  }

  if (!authToken) {
    return (
      <div className="login-page">
        <div className="login-hero">
          <span className="brand">WhatsApp</span>
          <h1>Welcome to Chat</h1>
          <p className="subtitle">
            Private and group messaging, powered by your Django backend.
          </p>
          <div className="hero-card">
            <h2>Live features</h2>
            <ul>
              <li>Secure JWT login</li>
              <li>Real-time delivery</li>
              <li>Group management</li>
            </ul>
          </div>
        </div>
        <div className="login-card">
          <h2>{registerMode ? 'Create account' : 'Sign in'}</h2>
          <p className="meta">
            {registerMode
              ? 'Create a new account to start chatting.'
              : 'Use your username and password to continue.'}
          </p>
          {authError && <p className="form-error">{authError}</p>}
          <form className="stack" onSubmit={handleAuth}>
            <label>
              Username
              <input
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                placeholder="username"
              />
            </label>
            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                placeholder="password"
              />
            </label>
            {registerMode && (
              <label>
                Email
                <input
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  placeholder="email"
                />
              </label>
            )}
            <div className="row">
              <button type="submit">
                {registerMode ? 'Register + Login' : 'Login'}
              </button>
              <button
                className="ghost"
                type="button"
                onClick={() => setRegisterMode((value) => !value)}
              >
                {registerMode ? 'Use login' : 'Create account'}
              </button>
            </div>
          </form>
        </div>
      </div>
    )
  }

  return (
    <div className="wa-shell">
      <aside className="wa-sidebar">
        <div className="wa-sidebar-header">
          <div>
            <span className="brand">WhatsApp</span>
            <p className="meta">User {currentUserId ?? '...'}</p>
          </div>
          <button className="ghost" onClick={handleLogout}>
            Sign out
          </button>
        </div>
        <div className="wa-section">
          <div className="wa-section-title">
            <h2>Chats</h2>
            <button className="ghost" onClick={loadUsers}>
              Refresh
            </button>
          </div>
          <div className="wa-list">
            {users
              .filter((user) => user.id !== currentUserId)
              .map((user) => (
                <button
                  key={user.id}
                  className={`wa-list-item ${
                    activeChatMode === 'private' &&
                    String(privateTargetId) === String(user.id)
                      ? 'active'
                      : ''
                  }`}
                  onClick={() => handleSelectUser(user.id)}
                >
                  <div>
                    <strong>{user.username}</strong>
                    <span className="meta">#{user.id}</span>
                  </div>
                  <span className={`status-pill ${user.is_online ? 'online' : 'offline'}`}>
                    {user.is_online ? 'online' : 'offline'}
                  </span>
                </button>
              ))}
          </div>
        </div>
        <div className="wa-section">
          <div className="wa-section-title">
            <h2>Groups</h2>
            <button className="ghost" onClick={loadGroups}>
              Refresh
            </button>
          </div>
          <div className="wa-list">
            {groups.map((group) => (
              <button
                key={group.id}
                className={`wa-list-item ${
                  activeChatMode === 'group' &&
                  String(groupId) === String(group.id)
                    ? 'active'
                    : ''
                }`}
                onClick={() => handleSelectGroup(group.id)}
              >
                <div>
                  <strong>{group.name}</strong>
                  <span className="meta">#{group.id}</span>
                </div>
                <div className="member-stack">
                  {(group.members_details || []).slice(0, 3).map((member) => (
                    <span className="member-pill" key={`${group.id}-${member.id}`}>
                      {member.username}
                    </span>
                  ))}
                  <span className="meta">
                    {(group.members_details || []).length} members
                  </span>
                </div>
              </button>
            ))}
          </div>
          <div className="wa-actions">
            <input
              value={groupName}
              onChange={(event) => setGroupName(event.target.value)}
              placeholder="New group name"
            />
            <button onClick={createGroup}>Create</button>
          </div>
        </div>
      </aside>

      <main className="wa-main">
        <header className="wa-chat-header">
          <div>
            <h2>{activeChatTitle}</h2>
            <p className="meta">
              {activeChatMode === 'group'
                ? 'Group chat'
                : privateTargetId
                  ? 'Direct message'
                  : 'Choose a conversation'}
            </p>
          </div>
          <div className="wa-header-actions">
            <button className="ghost" onClick={fetchPrivateHistory}>
              Load private
            </button>
            <button className="ghost" onClick={fetchGroupHistory}>
              Load group
            </button>
          </div>
        </header>

        <section className="wa-chat-body">
          {activeMessages.length === 0 ? (
            <div className="wa-empty">No messages yet</div>
          ) : (
            activeMessages.map((message) => (
              <div
                key={`${message.id || message.created_at}-${message.content}`}
                className={`bubble ${
                  message.sender_id === currentUserId ||
                  message.sender === currentUserId
                    ? 'me'
                    : 'them'
                }`}
              >
                <p>{message.content}</p>
              </div>
            ))
          )}
        </section>

        <footer className="wa-chat-input">
          <input
            value={activeChatMode === 'group' ? groupMessageText : privateMessageText}
            onChange={(event) =>
              activeChatMode === 'group'
                ? setGroupMessageText(event.target.value)
                : setPrivateMessageText(event.target.value)
            }
            placeholder={
              activeChatMode === 'group'
                ? 'Message the group...'
                : 'Message the contact...'
            }
          />
          <button
            onClick={
              activeChatMode === 'group' ? sendGroupMessage : sendPrivateMessage
            }
          >
            Send
          </button>
        </footer>

        <section className="wa-tools">
          <div className="wa-tool">
            <h3>Status lookup</h3>
            <div className="row">
              <input
                value={statusLookupId}
                onChange={(event) => setStatusLookupId(event.target.value)}
                placeholder="User id"
              />
              <button className="ghost" onClick={lookupStatus}>
                Check status
              </button>
            </div>
            {statusInfo && (
              <p className="meta">
                {statusInfo.username} is{' '}
                {statusInfo.is_online ? 'online' : 'offline'}
              </p>
            )}
          </div>
          <div className="wa-tool">
            <h3>Group members</h3>
            <div className="row">
              <input
                value={groupId}
                onChange={(event) => setGroupId(event.target.value)}
                placeholder="Group id"
              />
              <input
                value={groupMemberId}
                onChange={(event) => setGroupMemberId(event.target.value)}
                placeholder="Member id"
              />
              <button className="ghost" onClick={() => updateGroupMembers('add')}>
                Add
              </button>
              <button className="ghost" onClick={() => updateGroupMembers('remove')}>
                Remove
              </button>
            </div>
          </div>
          <div className="wa-tool">
            <h3>WebSocket bridge</h3>
            <div className="row">
              <select
                value={activeWsType}
                onChange={(event) => setActiveWsType(event.target.value)}
              >
                <option value="private">Private</option>
                <option value="group">Group</option>
              </select>
              <input
                value={activeWsTarget}
                onChange={(event) => setActiveWsTarget(event.target.value)}
                placeholder={activeWsType === 'private' ? 'User id' : 'Group id'}
              />
              <button onClick={connectWebSocket}>Connect</button>
              <span className={`badge ${wsStatus === 'connected' ? 'good' : 'muted'}`}>
                {wsStatus}
              </span>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
