import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: number
  login: string
}

export const useUserStore = defineStore('stores', () => {
  const user = ref<User>()

  function getUser() {
  }

  function setUser(){
  }

  return {
    getUser,
    setUser
  }
})