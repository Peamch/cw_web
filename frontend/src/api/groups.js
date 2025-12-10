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
