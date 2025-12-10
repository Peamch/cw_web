import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { goalsAPI } from '../api/goals'
import { Plus, Target, TrendingUp } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [goals, setGoals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadGoals()
  }, [])

  const loadGoals = async () => {
    try {
      const data = await goalsAPI.getAll()
      setGoals(data)
    } catch (error) {
      toast.error('Failed to load goals')
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'ACTIVE': return 'bg-green-100 text-green-800'
      case 'COMPLETED': return 'bg-blue-100 text-blue-800'
      case 'PAUSED': return 'bg-gray-100 text-gray-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
          Dashboard
        </h1>
        <p className="text-gray-600">Welcome back! Here's your progress overview</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Total Goals</p>
              <p className="text-3xl font-bold mt-1">{goals.length}</p>
            </div>
            <Target className="w-12 h-12 opacity-30" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Active Goals</p>
              <p className="text-3xl font-bold mt-1">{goals.filter(g => g.status === 'ACTIVE').length}</p>
            </div>
            <TrendingUp className="w-12 h-12 opacity-30" />
          </div>
        </div>
        
        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-xl">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Completed</p>
              <p className="text-3xl font-bold mt-1">{goals.filter(g => g.status === 'COMPLETED').length}</p>
            </div>
            <div className="text-3xl opacity-30">🎉</div>
          </div>
        </div>
      </div>

      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Your Goals</h2>
        <Link
          to="/goals"
          className="flex items-center px-5 py-2.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
        >
          <Plus className="w-5 h-5 mr-2" />
          New Goal
        </Link>
      </div>

      {goals.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl shadow-xl border-2 border-dashed border-gray-300">
          <div className="inline-block p-4 bg-blue-100 rounded-full mb-4">
            <Target className="w-16 h-16 text-blue-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No goals yet</h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Start your journey by creating your first goal. Build habits that last!
          </p>
          <Link
            to="/goals"
            className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            <Plus className="w-5 h-5 mr-2" />
            Create Your First Goal
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {goals.map((goal) => (
            <Link
              key={goal.id}
              to={`/goals/${goal.id}`}
              className="group bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all transform hover:scale-105 border border-gray-100"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                    {goal.title}
                  </h3>
                </div>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(goal.status)}`}>
                  {goal.status}
                </span>
              </div>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{goal.description}</p>
              
              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <span className="text-gray-500 text-sm flex items-center font-medium">
                  <TrendingUp className="w-4 h-4 mr-1.5 text-green-500" />
                  {goal.frequency}
                </span>
                <span className="text-blue-600 font-semibold text-sm group-hover:translate-x-1 transition-transform inline-flex items-center">
                  View
                  <svg className="w-4 h-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
