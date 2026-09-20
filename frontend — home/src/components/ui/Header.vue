<template>
  <header class="main_header">
    <div class="header_container">
      <h1 class="logo">{{ logoText }}</h1>

      <nav class="nav">
        <router-link
          v-for="link in navLinks"
          :key="link.name"
          :to="link.path"
          class="nav-link"
          active-class="active-link"
        >
          {{ link.name }}
        </router-link>

        <router-link
          to="/cart"
          class="nav-link cart-link"
          active-class="active-link"
        >
          Корзина
          <span v-if="cartStore.totalItems > 0" class="cart-badge">
            {{ cartStore.totalItems }}
          </span>
        </router-link>

        <button class="nav-link chat-btn" @click="isChatOpen = true">
          Спросить у официанта
        </button>
      </nav>

      <div class="user-area">
        <span class="user-name">Hi, {{ userStore.userLogin }}</span>
        <button class="logout-btn" @click="userStore.logout">Выйти</button>
      </div>
    </div>

    <OfficiantModal :is-open="isChatOpen" @close="isChatOpen = false" />
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useUserStore } from '@/stores/user'
import OfficiantModal from '@/components/modals/OfficiantModal.vue'

const userStore = useUserStore()
const cartStore = useCartStore()

const isChatOpen = ref(false)

interface NavLink {
  name: string
  path: string
}

const logoText: string = 'Домашняя кухня'

const navLinks: NavLink[] = [
  { name: 'Главная', path: '/' },
  { name: 'Заказать из меню', path: '/menu' },
  { name: 'Создать новое меню', path: '/new' },
]
</script>

<style scoped>
.main_header {
  background: #2c3e50;
  color: #fff;
  padding: 12px 0;
}

.header_container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 24px;
}

.logo {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
}

.nav {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  font-family: inherit;
  line-height: 1;
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  white-space: nowrap;
}

.nav-link:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.08);
}

.nav-link.active-link {
  color: #42b883;
  background: rgba(66, 184, 131, 0.12);
}

.chat-btn {
  color: #42b883;
  border-color: rgba(66, 184, 131, 0.5);
}

.chat-btn:hover {
  color: #fff;
  background: rgba(66, 184, 131, 0.2);
  border-color: rgba(66, 184, 131, 0.8);
}

.cart-link {
  position: relative;
}

.cart-badge {
  background: #42b883;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
  animation: bounce 0.3s ease;
}

@keyframes bounce {
  0% { transform: scale(0.5); }
  60% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

.user-area {
  display: flex;
  align-items: center;
  gap: 12px;
  white-space: nowrap;
}

.user-name {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
}

.logout-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: rgba(255, 255, 255, 0.85);
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 0.9rem;
  line-height: 1;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.logout-btn:hover {
  background: rgba(229, 62, 62, 0.15);
  border-color: rgba(229, 62, 62, 0.6);
  color: #fc8181;
}

@media (max-width: 768px) {
  .header_container {
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  .nav {
    justify-content: center;
  }

  .user-area {
    justify-content: center;
  }
}
</style>