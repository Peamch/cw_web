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
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-600 to-orange-600 bg-clip-text text-transparent mb-2">
          Achievements
        </h1>
        <p className="text-gray-600">Your badges and milestones</p>
      </div>

      {/* Progress bar */}
      <div className="bg-white rounded-2xl shadow-xl p-6 mb-8">
        <div className="flex items-center justify-between mb-3">
          <span className="text-sm font-semibold text-gray-700">Progress</span>
          <span className="text-sm font-bold text-blue-600">
            {myAchievements.length} / {achievements.length} Earned
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div 
            className="bg-gradient-to-r from-yellow-400 to-orange-400 h-4 rounded-full transition-all duration-500"
            style={{ width: `${achievements.length > 0 ? (myAchievements.length / achievements.length) * 100 : 0}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {achievements.map((achievement) => {
          const earned = isEarned(achievement.id)
          return (
            <div
              key={achievement.id}
              className={`relative bg-white rounded-2xl shadow-xl p-6 transition-all transform hover:scale-105 ${
                earned ? 'border-2 border-yellow-400 shadow-yellow-200' : 'opacity-70 grayscale'
              }`}
            >
              {earned && (
                <div className="absolute -top-3 -right-3">
                  <div className="bg-gradient-to-r from-yellow-400 to-orange-400 text-white px-4 py-1 rounded-full text-xs font-bold shadow-lg animate-pulse">
                    ✨ Earned!
                  </div>
                </div>
              )}

              <div className="flex items-center justify-center mb-6">
                <div className={`w-24 h-24 rounded-full flex items-center justify-center shadow-lg ${
                  earned 
                    ? 'bg-gradient-to-br from-yellow-400 to-orange-400' 
                    : 'bg-gray-200'
                }`}>
                  {earned ? (
                    <Award className="w-12 h-12 text-white" />
                  ) : (
                    <Lock className="w-12 h-12 text-gray-400" />
                  )}
                </div>
              </div>

              <div className="text-center">
                <h3 className="text-xl font-bold text-gray-900 mb-2">
                  {achievement.name}
                </h3>
                <p className="text-gray-600 text-sm mb-4">{achievement.description}</p>

                <div className="inline-flex items-center px-4 py-2 bg-gray-100 rounded-full text-xs font-semibold text-gray-700">
                  {achievement.ruleType}: {achievement.ruleValue}
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {achievements.length === 0 && (
        <div className="text-center py-16 bg-white rounded-2xl shadow-xl">
          <div className="inline-block p-4 bg-yellow-100 rounded-full mb-4">
            <Award className="w-16 h-16 text-yellow-600" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">No achievements yet</h3>
          <p className="text-gray-600">Start completing goals to earn badges!</p>
        </div>
      )}
    </div>
  )
}
