import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserData {
  id: number
  login: string
}

export const useUserStore = defineStore('user', () => {
  const user = ref<UserData | null>(null)

  const isAuthenticated = computed(() => !!user.value)
  const userLogin = computed(() => user.value?.login || '')
  const userId = computed(() => user.value?.id || -1)

  function setUser(data: UserData) {
    user.value = data
    localStorage.setItem('user', JSON.stringify(data))
  }

  function clearUser() {
    user.value = null
    localStorage.removeItem('user')
  }

  function restoreUser() {
    const stored = localStorage.getItem('user')
    if (stored) {
      try {
        user.value = JSON.parse(stored)
      } catch (e) {
        clearUser()
      }
    }
  }

  return {
    isAuthenticated,
    userLogin,
    userId,
    setUser,
    restoreUser,
    clearUser,
  }
})