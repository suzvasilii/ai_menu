import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi, type BasketResponse } from '@/api/cart'

export interface CartItem {
  name: string
  image: string
  quantity: number
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const basketId = ref<number>(0)
  const isLoading = ref(false)
  const loadedForUserId = ref<number | null>(null)

  const totalItems = computed(() =>
    items.value.reduce((sum, item) => sum + item.quantity, 0)
  )

  function applyBasket(data: BasketResponse) {
    basketId.value = data.id
    items.value = (data.items ?? []).map(item => ({
      name: item.dish_name,
      image: item.image_url ?? '',
      quantity: item.quantity,
    }))
  }

  async function loadFromBackend(userId: number) {
    if (loadedForUserId.value === userId) return
    isLoading.value = true
    try {
      const data = await cartApi.get(userId)
      applyBasket(data)
      loadedForUserId.value = userId
    } catch (e) {
      console.error('Не удалось загрузить корзину:', e)
    } finally {
      isLoading.value = false
    }
  }

  async function addToCart(userId: number, product: { name: string; image?: string }) {
    try {
      const data = await cartApi.add({
        user_id: userId,
        items: [{ dish_name: product.name, quantity: 1 }],
      })
      applyBasket(data)
    } catch (e) {
      console.error('Не удалось добавить в корзину:', e)
    }
  }

  function reset() {
    items.value = []
    basketId.value = 0
    loadedForUserId.value = null
    isLoading.value = false
  }

  return {
    items,
    basketId,
    isLoading,
    loadedForUserId,
    totalItems,
    addToCart,
    loadFromBackend,
    reset,
  }
})