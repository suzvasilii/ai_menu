<template>
  <div class="auth-modal-overlay">
    <div class="auth-modal">
      <h2>{{ isLogin ? 'Sing in' : 'Sign up' }}</h2>

      <form @submit.prevent="handleSubmit">
        <input
          v-model="login"
          type="text"
          placeholder="Login"
          required
        />
        <button type="submit" :disabled="isLoading">
          {{ isLoading ? 'Loading...' : isLogin ? 'Log in' : 'Reg' }}
        </button>

        <p class="switch-mode" @click="toggleMode">
          {{ isLogin ? 'Do not have an account? Register!' : 'Already have an account? Log in!' }}
        </p>
      </form>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authApi } from '@/api/auth'
import { useUserStore } from "@/stores/user.ts";

const userStore = useUserStore()
const emit = defineEmits(['auth-success'])

const login = ref('')
const isLogin = ref(true)
const isLoading = ref(false)
const error = ref('')

const toggleMode = () => {
  isLogin.value = !isLogin.value
  error.value = ''
}

const handleSubmit = async () => {
  isLoading.value = true
  error.value = ''
  try {
    let response
    if (isLogin.value) {
      response = await authApi.login(login.value)
    } else {
      response = await authApi.reg(login.value)
    }
    userStore.setUser(response.data)
    console.log('Ответ от бэка:', response.data)
    userStore.setUser(response.data)
    console.log('После setUser:', userStore.isAuthenticated)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error, try later.'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.auth-modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 360px;
  position: relative;
}
.auth-modal h2 {
  margin-top: 0;
}
.auth-modal input {
  width: 100%;
  padding: 8px;
  margin-bottom: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.auth-modal button[type="submit"] {
  width: 100%;
  padding: 10px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.switch-mode {
  margin-top: 12px;
  cursor: pointer;
  color: #007bff;
  text-align: center;
}
.error {
  color: red;
  font-size: 14px;
  text-align: center;
}
</style>