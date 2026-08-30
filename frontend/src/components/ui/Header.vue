<template>
  <header class="main_header">
    <div class="header_container">
        <h1>{{ logoText }}</h1>
        <nav>
           <router-link 
          v-for="link in navLinks" 
          :key="link.name"
          :to="link.path" 
          class="nav-link"
          active-class="active-link"
        >
          {{ link.name }}
          </router-link>
           <router-link to="/cart" class="nav-link cart-link" active-class="active-link">
          🛒 Корзина
          <span v-if="cartStore.totalItems > 0" class="cart-badge">
            {{ cartStore.totalItems }}
          </span>
        </router-link>
        </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart.ts'

interface NavLink {
  name: string
  path: string
}

const logoText: string = "Домашняя кухня"

const handleClick = (linkName: string): void => {
  console.log(``)
}

const navLinks: NavLink[] = [
  { name: 'Главная', path: '/' },
  { name: 'Заказать из меню', path: '/menu' },
  { name: 'Создать новое меню', path: '/new' }
]

const cartStore = useCartStore()
</script>
<style scoped>

.main_header {
  background: #2c3e50;
  color: #fff;
  padding: 1rem 0;
}

.header_container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav {
  display: flex;
  gap: 32px;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ffffff;
}

.nav-link.active-link {
  color: #42b883;
}

.cart-link {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  transition: background 0.3s ease;
}

.cart-link:hover {
  background: rgba(255, 255, 255, 0.1);
}

.cart-link.active-link {
  background: rgba(66, 184, 131, 0.2);
  color: #42b883;
}

.cart-badge {
  background: #42b883;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 12px;
  min-width: 20px;
  text-align: center;
  animation: bounce 0.3s ease;
}

@keyframes bounce {
  0% { transform: scale(0.5); }
  60% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
  .header_container {
    flex-direction: column;
    gap: 16px;
  }
  
  nav {
    gap: 16px;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>