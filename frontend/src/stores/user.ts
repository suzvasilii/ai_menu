import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const username = ref<string | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

  const userLogin = computed(() => username.value || 'Guest')
  const hasToken = computed(() => !!localStorage.getItem('access_token'))

  const checkAuth = async () => {
    isLoading.value = true

    const token = localStorage.getItem('access_token')
    if (!token) {
      isAuthenticated.value = false
      isLoading.value = false
      return
    }
    try {
      const response = await authApi.verifyUser()
      username.value = response.data.username
      isAuthenticated.value = true
    } catch (error) {
      localStorage.removeItem('access_token')
      isAuthenticated.value = false
      username.value = null
    } finally {
      isLoading.value = false
    }
  }
  const setToken = (token: string) => {
    localStorage.setItem('access_token', token)
    isAuthenticated.value = true
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    isAuthenticated.value = false
    username.value = null
    window.location.href = '/'
  }

  const setUsername = (name: string) => {
    username.value = name
  }

  return {
    username,
    isAuthenticated,
    isLoading,
    userLogin,
    hasToken,
    checkAuth,
    setToken,
    setUsername,
    logout,
  }
})