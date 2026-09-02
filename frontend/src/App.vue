<template>
  <div id="app">
    <template v-if="userStore.isAuthenticated">
      <Header />
      <router-view />
      </template>
    <AuthModal v-else />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'
import { authApi } from './api/auth'
import AuthModal from './components/forms/AuthForm.vue'
import Header from './components/ui/Header.vue'

const userStore = useUserStore()

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('token')
  if (token) {
    try {
      const response = await authApi.exchangeToken(token)
      const accessToken = response.data.access_token
      userStore.setToken(accessToken)
      window.history.replaceState({}, document.title, '/')
    } catch (error) {
      console.error(error)
    }
  }
  await userStore.checkAuth()
})
</script>