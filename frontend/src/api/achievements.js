import client from './client'

export const achievementsAPI = {
  getAll: async () => {
    const { data } = await client.get('/achievements')
    return data.data
  },
  getMy: async () => {
    const { data } = await client.get('/achievements/me')
    return data.data
  },
}
