# Frontend Pages Code (Part 3)

### src/pages/Groups.jsx
```jsx
import { useEffect, useState } from 'react'
import { groupsAPI } from '../api/groups'
import { Plus, Users, X } from 'lucide-react'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

export default function Groups() {
  const [groups, setGroups] = useState({ content: [] })
  const [showModal, setShowModal] = useState(false)
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    visibility: 'PUBLIC',
  })
  const navigate = useNavigate()

  useEffect(() => {
    loadGroups()
  }, [])

  const loadGroups = async () => {
    try {
      const data = await groupsAPI.getAll()
      setGroups(data)
    } catch (error) {
      toast.error('Failed to load groups')
    }
  }

  const handleCreate = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      await groupsAPI.create(formData)
      toast.success('Group created!')
      setShowModal(false)
      setFormData({ name: '', description: '', visibility: 'PUBLIC' })
      loadGroups()
    } catch (error) {
      toast.error('Failed to create group')
    } finally {
      setLoading(false)
    }
  }

  const handleJoin = async (groupId) => {
    try {
      await groupsAPI.join(groupId)
      toast.success('Joined group!')
      loadGroups()
    } catch (error) {
      toast.error(error.response?.data?.message || 'Failed to join group')
    }
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Groups</h1>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5 mr-2" />
          Create Group
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {groups.content?.map((group) => (
          <div
            key={group.id}
            className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
          >
            <div
              onClick={() => navigate(`/groups/${group.id}`)}
              className="cursor-pointer"
            >
              <div className="flex items-start justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{group.name}</h3>
                <span className={`px-2 py-1 rounded text-xs ${
                  group.visibility === 'PUBLIC' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {group.visibility}
                </span>
              </div>
              
              <p className="text-gray-600 text-sm mb-4 line-clamp-2">{group.description}</p>
            </div>
            
            <div className="flex items-center justify-between pt-4 border-t">
              <span className="text-gray-500 text-sm flex items-center">
                <Users className="w-4 h-4 mr-1" />
                Members
              </span>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  handleJoin(group.id)
                }}
                className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
              >
                Join
              </button>
            </div>
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Create New Group</h2>
              <button onClick={() => setShowModal(false)}>
                <X className="w-6 h-6" />
              </button>
            </div>

            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  rows="3"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Visibility</label>
                <select
                  value={formData.visibility}
                  onChange={(e) => setFormData({ ...formData, visibility: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="PUBLIC">Public</option>
                  <option value="PRIVATE">Private</option>
                </select>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Creating...' : 'Create Group'}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
```

### src/pages/GroupDetail.jsx
```jsx
import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { groupsAPI } from '../api/groups'
import { ArrowLeft, Users } from 'lucide-react'
import toast from 'react-hot-toast'

export default function GroupDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [group, setGroup] = useState(null)
  const [members, setMembers] = useState([])
  const [activities, setActivities] = useState({ content: [] })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [id])

  const loadData = async () => {
    try {
      const [groupData, membersData, activitiesData] = await Promise.all([
        groupsAPI.getById(id),
        groupsAPI.getMembers(id),
        groupsAPI.getActivities(id),
      ])
      setGroup(groupData)
      setMembers(membersData)
      setActivities(activitiesData)
    } catch (error) {
      toast.error('Failed to load group')
    } finally {
      setLoading(false)
    }
  }

  const handleLeave = async () => {
    if (window.confirm('Are you sure you want to leave this group?')) {
      try {
        await groupsAPI.leave(id)
        toast.success('Left group')
        navigate('/groups')
      } catch (error) {
        toast.error('Failed to leave group')
      }
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <button
        onClick={() => navigate('/groups')}
        className="flex items-center text-gray-600 hover:text-gray-900 mb-6"
      >
        <ArrowLeft className="w-5 h-5 mr-2" />
        Back to Groups
      </button>

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">{group.name}</h1>
            <p className="text-gray-600 mb-4">{group.description}</p>
            <span className={`px-3 py-1 rounded text-sm ${
              group.visibility === 'PUBLIC' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
            }`}>
              {group.visibility}
            </span>
          </div>
          <button
            onClick={handleLeave}
            className="px-4 py-2 border border-red-600 text-red-600 rounded-lg hover:bg-red-50"
          >
            Leave Group
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Activity Feed</h2>
            <div className="space-y-4">
              {activities.content?.map((activity) => (
                <div key={activity.id} className="border-b pb-4">
                  <p className="text-gray-800">{activity.type}</p>
                  <p className="text-sm text-gray-500">
                    {new Date(activity.createdAt).toLocaleDateString()}
                  </p>
                </div>
              ))}
              {activities.content?.length === 0 && (
                <p className="text-center text-gray-500 py-8">No activities yet</p>
              )}
            </div>
          </div>
        </div>

        <div>
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4 flex items-center">
              <Users className="w-5 h-5 mr-2" />
              Members ({members.length})
            </h2>
            <div className="space-y-3">
              {members.map((member) => (
                <div key={member.id} className="flex items-center justify-between">
                  <span className="text-gray-800">{member.userId}</span>
                  <span className="text-xs text-gray-500">{member.role}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### src/pages/Achievements.jsx
```jsx
import { useEffect, useState } from 'react'
import { achievementsAPI } from '../api/achievements'
import { Award, Lock } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Achievements() {
  const [achievements, setAchievements] = useState([])
  const [myAchievements, setMyAchievements] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [allAchievements, myAchievementsData] = await Promise.all([
        achievementsAPI.getAll(),
        achievementsAPI.getMy(),
      ])
      setAchievements(allAchievements)
      setMyAchievements(myAchievementsData)
    } catch (error) {
      toast.error('Failed to load achievements')
    } finally {
      setLoading(false)
    }
  }

  const isEarned = (achievementId) => {
    return myAchievements.some((a) => a.achievementId === achievementId)
  }

  if (loading) return <div>Loading...</div>

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Achievements</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {achievements.map((achievement) => {
          const earned = isEarned(achievement.id)
          return (
            <div
              key={achievement.id}
              className={`bg-white rounded-lg shadow p-6 ${
                earned ? 'border-2 border-yellow-400' : 'opacity-60'
              }`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center ${
                  earned ? 'bg-yellow-100' : 'bg-gray-100'
                }`}>
                  {earned ? (
                    <Award className="w-8 h-8 text-yellow-600" />
                  ) : (
                    <Lock className="w-8 h-8 text-gray-400" />
                  )}
                </div>
                {earned && (
                  <span className="px-3 py-1 bg-yellow-100 text-yellow-800 text-xs font-medium rounded-full">
                    Earned
                  </span>
                )}
              </div>

              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {achievement.name}
              </h3>
              <p className="text-gray-600 text-sm mb-4">{achievement.description}</p>

              <div className="text-xs text-gray-500">
                {achievement.ruleType}: {achievement.ruleValue}
              </div>
            </div>
          )
        })}
      </div>

      {achievements.length === 0 && (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <Award className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <p className="text-gray-600">No achievements available yet</p>
        </div>
      )}
    </div>
  )
}
```

## All pages complete!

Now run:
```powershell
cd C:\Users\mormy\IdeaProjects\cw_web\frontend
npm install
npm run dev
```

Frontend will be available at http://localhost:3000
