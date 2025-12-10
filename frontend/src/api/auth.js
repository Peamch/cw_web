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
