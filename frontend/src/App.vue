<template>
<Header />
<router-view />
  <AuthForm
    v-if="!userStore.isAuthenticated"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import Header from './components/ui/Header.vue'
import AuthForm from "@/components/forms/AuthForm.vue"
import {useUserStore} from "@/stores/user.ts"

const userStore = useUserStore()

</script>

