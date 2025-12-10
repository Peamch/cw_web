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
