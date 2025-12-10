import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import { Home, Target, Users, Award, LogOut, Sparkles } from 'lucide-react'

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { to: '/dashboard', icon: Home, label: 'Dashboard', gradient: 'from-blue-500 to-purple-500' },
    { to: '/goals', icon: Target, label: 'Goals', gradient: 'from-green-500 to-teal-500' },
    { to: '/groups', icon: Users, label: 'Groups', gradient: 'from-orange-500 to-pink-500' },
    { to: '/achievements', icon: Award, label: 'Achievements', gradient: 'from-yellow-500 to-orange-500' },
  ]

  return (
    <div className="flex h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <aside className="w-72 bg-white shadow-2xl border-r border-gray-200">
        <div className="p-6 bg-gradient-to-r from-blue-600 to-purple-600">
          <div className="flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white">Habit Tracker</h1>
          </div>
          <div className="flex items-center mt-4 p-3 bg-white/10 rounded-lg backdrop-blur-sm">
            <div className="w-10 h-10 bg-white/30 rounded-full flex items-center justify-center text-white font-bold">
              {user?.displayName?.[0]?.toUpperCase() || 'U'}
            </div>
            <div className="ml-3">
              <p className="text-sm font-semibold text-white">{user?.displayName}</p>
              <p className="text-xs text-blue-100">{user?.email}</p>
            </div>
          </div>
        </div>
        
        <nav className="mt-6 px-4">
          {navItems.map(({ to, icon: Icon, label, gradient }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 mb-2 rounded-xl transition-all duration-200 group ${
                  isActive 
                    ? `bg-gradient-to-r ${gradient} text-white shadow-lg transform scale-105` 
                    : 'text-gray-700 hover:bg-gray-100'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`w-5 h-5 mr-3 ${isActive ? 'text-white' : 'text-gray-500 group-hover:text-gray-700'}`} />
                  <span className="font-medium">{label}</span>
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-6 left-4 right-4">
          <button
            onClick={handleLogout}
            className="flex items-center w-full px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl transition-all duration-200 group"
          >
            <LogOut className="w-5 h-5 mr-3 group-hover:transform group-hover:-translate-x-1 transition-transform" />
            <span className="font-medium">Logout</span>
          </button>
        </div>
      </aside>

      <main className="flex-1 overflow-y-auto">
        <div className="max-w-7xl mx-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  )
}
