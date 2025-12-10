import { useEffect, useState } from 'react'
import { goalsAPI } from '../api/goals'
import { Plus, X } from 'lucide-react'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

export default function Goals() {
  const [goals, setGoals] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    frequency: 'DAILY',
    isPublic: false,
  })
  const navigate = useNavigate()

  useEffect(() => {
    loadGoals()
  }, [])

  const loadGoals = async () => {
    try {
      const data = await goalsAPI.getAll()
      setGoals(data)
    } catch (error) {
      toast.error('Failed to load goals')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await goalsAPI.create(formData)
      toast.success('Goal created!')
      setShowModal(false)
      setFormData({ title: '', description: '', frequency: 'DAILY', isPublic: false })
      loadGoals()
    } catch (error) {
      toast.error('Failed to create goal')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-8">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent mb-2">
              My Goals
            </h1>
            <p className="text-gray-600">Manage and track your habits</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center px-5 py-2.5 bg-gradient-to-r from-green-600 to-teal-600 text-white rounded-xl hover:from-green-700 hover:to-teal-700 shadow-lg hover:shadow-xl transition-all transform hover:scale-105"
          >
            <Plus className="w-5 h-5 mr-2" />
            New Goal
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {goals.map((goal) => (
          <div
            key={goal.id}
            onClick={() => navigate(`/goals/${goal.id}`)}
            className="group bg-white rounded-2xl shadow-lg p-6 cursor-pointer hover:shadow-2xl transition-all transform hover:scale-105 border border-gray-100"
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <h3 className="text-lg font-bold text-gray-900 group-hover:text-green-600 transition-colors mb-2">
                  {goal.title}
                </h3>
                <p className="text-gray-600 text-sm line-clamp-2">{goal.description}</p>
              </div>
            </div>
            
            <div className="flex justify-between items-center pt-4 border-t border-gray-100 mt-4">
              <div className="flex items-center space-x-2">
                <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-semibold rounded-full">
                  {goal.frequency}
                </span>
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                  goal.status === 'ACTIVE' ? 'bg-blue-100 text-blue-700' : 
                  goal.status === 'COMPLETED' ? 'bg-purple-100 text-purple-700' : 
                  'bg-gray-100 text-gray-700'
                }`}>
                  {goal.status}
                </span>
              </div>
              <span className="text-green-600 font-semibold text-sm group-hover:translate-x-1 transition-transform">→</span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-gradient-to-r from-green-600 to-teal-600 p-6 rounded-t-2xl">
              <div className="flex justify-between items-center">
                <h2 className="text-2xl font-bold text-white">Create New Goal</h2>
                <button 
                  onClick={() => setShowModal(false)} 
                  className="text-white hover:bg-white/20 rounded-full p-2 transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
            </div>
            
            <div className="p-6">

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
                  placeholder="e.g., Morning Meditation"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
                  rows="3"
                  placeholder="Describe your goal..."
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Frequency</label>
                <select
                  value={formData.frequency}
                  onChange={(e) => setFormData({ ...formData, frequency: e.target.value })}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:border-green-500 transition-colors"
                >
                  <option value="DAILY">📅 Daily</option>
                  <option value="WEEKLY">📆 Weekly</option>
                  <option value="MONTHLY">🗓️ Monthly</option>
                </select>
              </div>

              <div className="flex items-center p-4 bg-gray-50 rounded-xl">
                <input
                  type="checkbox"
                  checked={formData.isPublic}
                  onChange={(e) => setFormData({ ...formData, isPublic: e.target.checked })}
                  className="h-5 w-5 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label className="ml-3 block text-sm font-medium text-gray-700">
                  🌍 Make this goal public
                </label>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 px-4 bg-gradient-to-r from-green-600 to-teal-600 text-white rounded-xl font-semibold hover:from-green-700 hover:to-teal-700 focus:outline-none focus:ring-4 focus:ring-green-300 disabled:opacity-50 transition-all transform hover:scale-[1.02]"
              >
                {loading ? 'Creating...' : 'Create Goal'}
              </button>
            </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
