import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
  persist(
    (set) => ({
      token: null,
      refreshToken: null,
      user: null,
      
      setTokens: (accessToken, refreshToken) => {
        set({ token: accessToken, refreshToken })
      },
      
      setUser: (user) => {
        set({ user })
      },
      
      login: (accessToken, refreshToken, user) => {
        set({ token: accessToken, refreshToken, user })
      },
      
      logout: () => {
        set({ token: null, refreshToken: null, user: null })
      },
    }),
    {
      name: 'auth-storage',
    }
  )
)
