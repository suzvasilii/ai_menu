<template>
  <div id="app">
    <template v-if="userStore.isAuthenticated">
      <Header />
      <router-view />
    </template>
    <AuthModal v-else />

    <GreetingModal
      :is-open="isGreetingOpen"
      @close="isGreetingOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue'
import { useUserStore } from './stores/user'
import { useCartStore } from './stores/cart'
import { authApi } from './api/auth'
import AuthModal from './components/forms/AuthForm.vue'
import Header from './components/ui/Header.vue'
import GreetingModal from "@/components/modals/GreetingModal.vue";

const userStore = useUserStore()
const cartStore = useCartStore()

const isGreetingOpen = ref(false)

watch(
  () => userStore.userId,
  async (id) => {
    if (id) {
      await cartStore.loadFromBackend(id)
    } else {
      cartStore.reset()
    }
  },
  { immediate: true }
)

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  const token = params.get('token')
  if (token) {
    try {
      const response = await authApi.exchangeToken(token)
      const accessToken = response.data.access_token
      userStore.setToken(accessToken)
      window.history.replaceState({}, document.title, '/')
      isGreetingOpen.value = true
    } catch (error) {
      console.error(error)
    }
  }
  await userStore.checkAuth()
})
</script>