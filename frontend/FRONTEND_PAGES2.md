# Frontend Pages Code (Part 2)

### src/pages/Goals.jsx
```jsx
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
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Goals</h1>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5 mr-2" />
          New Goal
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {goals.map((goal) => (
          <div
            key={goal.id}
            onClick={() => navigate(`/goals/${goal.id}`)}
            className="bg-white rounded-lg shadow p-6 cursor-pointer hover:shadow-lg transition-shadow"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{goal.title}</h3>
            <p className="text-gray-600 text-sm mb-4">{goal.description}</p>
            <div className="flex justify-between items-center text-sm">
              <span className="text-gray-500">{goal.frequency}</span>
              <span className={`px-2 py-1 rounded ${
                goal.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 
                goal.status === 'COMPLETED' ? 'bg-blue-100 text-blue-800' : 
                'bg-gray-100 text-gray-800'
              }`}>
                {goal.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Create New Goal</h2>
              <button onClick={() => setShowModal(false)} className="text-gray-500 hover:text-gray-700">
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  rows="3"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Frequency</label>
                <select
                  value={formData.frequency}
                  onChange={(e) => setFormData({ ...formData, frequency: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="DAILY">Daily</option>
                  <option value="WEEKLY">Weekly</option>
                  <option value="MONTHLY">Monthly</option>
                </select>
              </div>

              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={formData.isPublic}
                  onChange={(e) => setFormData({ ...formData, isPublic: e.target.checked })}
                  className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
                <label className="ml-2 block text-sm text-gray-700">Make this goal public</label>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Goal'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
```

### src/pages/GoalDetail.jsx
```jsx
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { goalsAPI } from '../api/goals'
import { ArrowLeft, Plus, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function GoalDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [goal, setGoal] = useState(null)
  const [progress, setProgress] = useState([])
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(true)
  const [progressForm, setProgressForm] = useState({
    value: 1,
    note: '',
  })

  useEffect(() => {
    loadData()
  }, [id])

  const loadData = async () => {
    try {
      const [goalData, progressData] = await Promise.all([
        goalsAPI.getById(id),
        goalsAPI.getProgress(id),
      ])
      setGoal(goalData)
      setProgress(progressData)
    } catch (error) {
      toast.error('Failed to load goal')
    } finally {
      setLoading(false)
    }
  }

  const handleLogProgress = async (e) => {
    e.preventDefault()
    try {
      await goalsAPI.logProgress({ goalId: id, ...progressForm })
      toast.success('Progress logged!')
      setShowModal(false)
      setProgressForm({ value: 1, note: '' })
      loadData()
    } catch (error) {
      toast.error('Failed to log progress')
    }
  }

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this goal?')) {
      try {
        await goalsAPI.delete(id)
        toast.success('Goal deleted')
        navigate('/goals')
      } catch (error) {
        toast.error('Failed to delete goal')
      }
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <button
        onClick={() => navigate('/goals')}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-5 h-5 mr-2" />
        Back to Goals
      </button>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{goal.title}</h1>
            <p className="text-gray-600">{goal.description}</p>
          </div>
          <button
            onClick={handleDelete}
            className="text-red-600 hover:text-red-800"
          >
            <Trash2 className="w-5 h-5" />
          </button>
        </div>

        <div className="flex gap-4 text-sm">
          <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded">
            {goal.frequency}
          </span>
          <span className={`px-3 py-1 rounded ${
            goal.status === 'ACTIVE' ? 'bg-green-100 text-green-800' : 
            'bg-gray-100 text-gray-800'
          }`}>
            {goal.status}
          </span>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">Progress History</h2>
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-5 h-5 mr-2" />
            Log Progress
          </button>
        </div>

        <div className="space-y-4">
          {progress.map((log) => (
            <div key={log.id} className="flex justify-between items-center border-b pb-4">
              <div>
                <p className="font-medium">{log.note || 'Progress logged'}</p>
                <p className="text-sm text-gray-500">
                  {format(new Date(log.date), 'MMM dd, yyyy')}
                </p>
              </div>
              <span className="text-lg font-semibold text-blue-600">
                {log.value}
              </span>
            </div>
          ))}
          {progress.length === 0 && (
            <p className="text-center text-gray-500 py-8">No progress logged yet</p>
          )}
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-6">Log Progress</h2>
            <form onSubmit={handleLogProgress} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Value</label>
                <input
                  type="number"
                  step="0.1"
                  value={progressForm.value}
                  onChange={(e) => setProgressForm({ ...progressForm, value: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Note (optional)</label>
                <textarea
                  value={progressForm.note}
                  onChange={(e) => setProgressForm({ ...progressForm, note: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  rows="3"
                />
              </div>
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-2 px-4 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Log Progress
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
```

Continuing with Groups and Achievements pages...
