# Frontend Source Code

## First, create the directory structure:

```powershell
cd C:\Users\mormy\IdeaProjects\cw_web\frontend
"src", "src\api", "src\components", "src\pages", "src\store", "src\utils", "public" | ForEach-Object { New-Item -ItemType Directory -Force -Path $_ }
```

## Then copy these files:

### src/main.jsx
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### src/index.css
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
}

body {
  margin: 0;
  min-height: 100vh;
  background-color: #f3f4f6;
}

#root {
  min-height: 100vh;
}
```

### src/App.jsx
```jsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './store/authStore'
import Layout from './components/Layout'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Goals from './pages/Goals'
import GoalDetail from './pages/GoalDetail'
import Groups from './pages/Groups'
import GroupDetail from './pages/GroupDetail'
import Achievements from './pages/Achievements'

function ProtectedRoute({ children }) {
  const { token } = useAuthStore()
  return token ? children : <Navigate to="/login" />
}

function PublicRoute({ children }) {
  const { token } = useAuthStore()
  return !token ? children : <Navigate to="/dashboard" />
}

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
        <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
        
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<Navigate to="/dashboard" />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="goals" element={<Goals />} />
          <Route path="goals/:id" element={<GoalDetail />} />
          <Route path="groups" element={<Groups />} />
          <Route path="groups/:id" element={<GroupDetail />} />
          <Route path="achievements" element={<Achievements />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
```

### src/api/client.js
```js
import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const client = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = useAuthStore.getState().refreshToken
        const { data } = await axios.post('/api/auth/refresh', { refreshToken })
        useAuthStore.getState().setTokens(data.data.accessToken, data.data.refreshToken)
        originalRequest.headers.Authorization = `Bearer ${data.data.accessToken}`
        return client(originalRequest)
      } catch (refreshError) {
        useAuthStore.getState().logout()
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export default client
```

### src/api/auth.js
```js
import client from './client'

export const authAPI = {
  signup: async (email, password, displayName) => {
    const { data } = await client.post('/auth/signup', { email, password, displayName })
    return data.data
  },
  login: async (email, password) => {
    const { data } = await client.post('/auth/login', { email, password })
    return data.data
  },
  refresh: async (refreshToken) => {
    const { data } = await client.post('/auth/refresh', { refreshToken })
    return data.data
  },
}
```

### src/api/goals.js
```js
import client from './client'

export const goalsAPI = {
  getAll: async () => {
    const { data } = await client.get('/goals')
    return data.data
  },
  getById: async (id) => {
    const { data } = await client.get(`/goals/${id}`)
    return data.data
  },
  create: async (goalData) => {
    const { data } = await client.post('/goals', goalData)
    return data.data
  },
  update: async (id, goalData) => {
    const { data } = await client.put(`/goals/${id}`, goalData)
    return data.data
  },
  delete: async (id) => {
    await client.delete(`/goals/${id}`)
  },
  getProgress: async (goalId) => {
    const { data } = await client.get(`/progress/goal/${goalId}`)
    return data.data
  },
  logProgress: async (progressData) => {
    const { data } = await client.post('/progress', progressData)
    return data.data
  },
}
```

### src/api/groups.js
```js
import client from './client'

export const groupsAPI = {
  getAll: async (params) => {
    const { data } = await client.get('/groups', { params })
    return data.data
  },
  getById: async (id) => {
    const { data } = await client.get(`/groups/${id}`)
    return data.data
  },
  create: async (groupData) => {
    const { data } = await client.post('/groups', groupData)
    return data.data
  },
  update: async (id, groupData) => {
    const { data } = await client.put(`/groups/${id}`, groupData)
    return data.data
  },
  delete: async (id) => {
    await client.delete(`/groups/${id}`)
  },
  join: async (id) => {
    const { data } = await client.post(`/groups/${id}/join`)
    return data.data
  },
  leave: async (id) => {
    await client.post(`/groups/${id}/leave`)
  },
  getMembers: async (id) => {
    const { data } = await client.get(`/groups/${id}/members`)
    return data.data
  },
  getActivities: async (id, params) => {
    const { data } = await client.get(`/activities/group/${id}`, { params })
    return data.data
  },
}
```

### src/api/achievements.js
```js
import client from './client'

export const achievementsAPI = {
  getAll: async () => {
    const { data } = await client.get('/achievements')
    return data.data
  },
  getMy: async () => {
    const { data } = await client.get('/achievements/me')
    return data.data
  },
}
```

### src/store/authStore.js
```js
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      
      setTokens: (accessToken, refreshToken) => {
        set({ token: accessToken, refreshToken })
      },
      
      setUser: (user) => {
        set({ user })
      },
      
      login: (accessToken, refreshToken, user) => {
        set({ token: accessToken, refreshToken, user })
      },
      
      logout: () => {
        set({ token: null, refreshToken: null, user: null })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
```

### src/components/Layout.jsx
```jsx
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Home, Target, Users, Award, LogOut } from 'lucide-react'

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { to: '/dashboard', icon: Home, label: 'Dashboard' },
    { to: '/goals', icon: Target, label: 'Goals' },
    { to: '/groups', icon: Users, label: 'Groups' },
    { to: '/achievements', icon: Award, label: 'Achievements' },
  ]

  return (
    <div className="flex h-screen bg-gray-100">
      <aside className="w-64 bg-white shadow-lg">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-gray-800">Habit Tracker</h1>
          <p className="text-sm text-gray-600 mt-1">{user?.displayName}</p>
        </div>
        
        <nav className="mt-6">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center px-6 py-3 text-gray-700 hover:bg-gray-100 ${
                  isActive ? 'bg-gray-100 border-r-4 border-blue-500' : ''
                }`
              }
            >
              <Icon className="w-5 h-5 mr-3" />
              {label}
            </NavLink>
          ))}
        </nav>

        <button
          onClick={handleLogout}
          className="flex items-center px-6 py-3 mt-auto text-red-600 hover:bg-red-50 w-full"
        >
          <LogOut className="w-5 h-5 mr-3" />
          Logout
        </button>
      </aside>

      <main className="flex-1 overflow-y-auto p-8">
        <Outlet />
      </main>
    </div>
  )
}
```

Due to size, continuing in next message with pages...
