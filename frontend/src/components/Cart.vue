<template>
  <div class="cart-page">
    <h1 class="cart-title">🛒 Корзина</h1>
    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <p class="empty-emoji">😕</p>
      <p class="empty-text">Корзина пуста</p>
      <router-link to="/menu" class="btn-primary">
        Перейти в меню
      </router-link>
    </div>
    <div v-else class="cart-content">
      <div class="cart-items">
        <div 
          v-for="item in cartStore.items" 
          :key="item.id"
          class="cart-item"
        >
          <img :src="item.image" :alt="item.name" class="cart-item-image" />
          
          <div class="cart-item-info">
            <h3>{{ item.name }}</h3>
          </div>
          
          <div class="cart-item-actions">
            <button 
              @click="cartStore.decreaseQuantity(item.id)" 
              class="qty-btn"
            >
              −
            </button>
            <span class="qty-count">{{ item.quantity }}</span>
            <button 
              @click="addOneMore(item)" 
              class="qty-btn"
            >
              +
            </button>
            <button 
              @click="cartStore.removeFromCart(item.id)" 
              class="remove-btn"
            >
              ✕
            </button>
          </div>
        </div>
      </div>

      <div class="cart-summary">
        <h3>Итого</h3>
        <p>Товаров: <strong>{{ cartStore.totalItems }}</strong></p>
        <p><input
            v-model="userName"
            type="text"
            class="form-control"
            placeholder="Ваше имя (обязательно)"
            @keyup.enter="addOrder"
            required
        /></p>
        <div class="mb-3">
          <textarea class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder="Уточнения по заказу (необ.)" v-model="comment"></textarea>
        </div>
        <button class="checkout-btn" @click="addOrder" :disabled="isLoading">
          <span v-if="isLoading">⏳ Отправка...</span>
          <span v-else>Оформить заказ</span>
        </button>
        <button @click="cartStore.clearCart" class="clear-btn">
          Очистить корзину
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import { useCartStore } from '@/cart/cart'
import { ordersApi } from '@/api/orders'

import {router} from "@/router/router.ts";

const cartStore = useCartStore()

const userName = ref('')
const comment = ref('')
const isLoading = ref(false)

const addOrder = async () => {
  if (!userName.value.trim()) {
    alert("Обязательно напишите имя!")
    return
  }

  isLoading.value = true

  try {
    const newOrder = await ordersApi.create({
      customer_name: userName.value,
      comment: comment.value,
      items: cartStore.items.map(item => ({
        name: item.name,
        quantity: item.quantity
      }))
    })
    alert("Вы успешно оформили новый заказ!")
    cartStore.clearCart()
    userName.value = ''
    router.push('/menu')

  } catch (error: any) {
    alert("Не удалось сформировать заказ :(")
  } finally {
    isLoading.value = false
  }
}

const addOneMore = (item: { id: number; name: string;  image: string }) => {
  cartStore.addToCart({
    id: item.id,
    name: item.name,
    image: item.image
  })
}
</script>

<style scoped>
.cart-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.cart-title {
  font-size: 2rem;
  margin-bottom: 40px;
  color: #2c3e50;
}

.empty-cart {
  text-align: center;
  padding: 80px 0;
}

.empty-emoji {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 1.2rem;
  color: #4a5568;
  margin-bottom: 30px;
}

.btn-primary {
  display: inline-block;
  background: #42b883;
  color: #fff;
  padding: 12px 32px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s ease;
}

.btn-primary:hover {
  background: #33a06f;
}

/* Содержимое корзины */
.cart-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}

.cart-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.2s ease;
}

.cart-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
}

.cart-item-info {
  flex: 1;
}

.cart-item-info h3 {
  margin: 0 0 4px 0;
  font-size: 1.1rem;
  color: #2c3e50;
}

.cart-item-info p {
  margin: 0;
  color: #4a5568;
  font-size: 0.9rem;
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.qty-btn {
  background: #f5f7fa;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  width: 32px;
  height: 32px;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  color: #2c3e50;
}

.qty-btn:hover {
  background: #e2e8f0;
}

.qty-count {
  min-width: 24px;
  text-align: center;
  font-weight: 600;
  font-size: 1rem;
}

.remove-btn {
  background: none;
  border: none;
  color: #e53e3e;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0 8px;
  transition: transform 0.2s ease;
}

.remove-btn:hover {
  transform: scale(1.2);
}

.cart-item-total {
  font-weight: 700;
  color: #2c3e50;
  min-width: 80px;
  text-align: right;
  font-size: 1.1rem;
}

/* Итого (сайдбар) */
.cart-summary {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  height: fit-content;
  position: sticky;
  top: 20px;
}

.cart-summary h3 {
  margin: 0 0 16px 0;
  font-size: 1.3rem;
  color: #2c3e50;
}

.cart-summary p {
  margin: 8px 0;
  color: #4a5568;
}

.total-price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #42b883;
  margin: 16px 0 !important;
}

.checkout-btn {
  width: 100%;
  background: #42b883;
  color: #fff;
  border: none;
  padding: 14px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
  margin-top: 8px;
}

.checkout-btn:hover {
  background: #33a06f;
}

.clear-btn {
  width: 100%;
  background: transparent;
  color: #e53e3e;
  border: 1px solid #e53e3e;
  padding: 10px;
  border-radius: 8px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 8px;
}

.clear-btn:hover {
  background: #fff5f5;
}

.checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Адаптивность */
@media (max-width: 768px) {
  .cart-content {
    grid-template-columns: 1fr;
  }
  
  .cart-item {
    flex-wrap: wrap;
  }
  
  .cart-item-actions {
    margin-left: auto;
  }
}
</style>