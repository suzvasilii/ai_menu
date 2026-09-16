import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi } from '@/api/cart.ts'

export interface CartItem {
  name: string
  image: string
  quantity: number
}

export const useCartStore = defineStore('cart.ts', () => {
  const items = ref<CartItem[]>([])
  const isLoading = ref(false)
  const isLoaded = ref(false)

  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  function addToCart(product: { name: string; image?: string }) {
    const existing = items.value.find(item => item.name === product.name)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({
        name: product.name,
        image: product.image ?? '',
        quantity: 1
      })
    }
  }

  function removeFromCart(name: string) {
    const index = items.value.findIndex(item => item.name === name)
    if (index !== -1) items.value.splice(index, 1)
  }

  function decreaseQuantity(name: string) {
    const item = items.value.find(item => item.name === name)
    if (!item) return
    if (item.quantity > 1) item.quantity--
    else removeFromCart(name)
  }

  function clearCart() {
    items.value = []
  }

  async function loadFromBackend(userId: number) {
    if (isLoaded.value) return
    isLoading.value = true
    try {
      const data = await cartApi.get(userId)
      items.value = (data.items ?? []).map(item => ({
        name: item.dish_name,
        image: item.image_url ?? '',
        quantity: item.quantity
      }))
      isLoaded.value = true
    } catch (e) {
      console.error('Не удалось загрузить корзину:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function saveToBackend(userId: number) {
    try {
      await cartApi.add({
        user_id: userId,
        items: items.value.map(item => ({
          dish_name: item.name,
          quantity: item.quantity
        }))
      })
    } catch (e) {
      console.error('Не удалось сохранить корзину:', e)
    }
  }

  function reset() {
    items.value = []
    isLoaded.value = false
    isLoading.value = false
  }

  return {
    items,
    isLoading,
    isLoaded,
    totalItems,
    addToCart,
    removeFromCart,
    decreaseQuantity,
    clearCart,
    loadFromBackend,
    saveToBackend,
    reset,
  }
})