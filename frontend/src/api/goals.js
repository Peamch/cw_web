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
