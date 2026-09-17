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

  async function increaseQuantity(userId: number, dishName: string) {
    const item = items.value.find(i => i.name === dishName)
    if (!item) return
    try {
      const data = await cartApi.updateItem({
        user_id: userId,
        dish_name: dishName,
        quantity: item.quantity + 1,
      })
      applyBasket(data)
    } catch (e) {
      console.error('Не удалось увеличить количество:', e)
    }
  }

  async function decreaseQuantity(userId: number, dishName: string) {
    const item = items.value.find(i => i.name === dishName)
    if (!item) return
    try {
      const data = await cartApi.updateItem({
        user_id: userId,
        dish_name: dishName,
        quantity: item.quantity - 1,
      })
      applyBasket(data)
    } catch (e) {
      console.error('Не удалось уменьшить количество:', e)
    }
  }

  async function removeFromCart(userId: number, dishName: string) {
    try {
      const data = await cartApi.removeItem({
        user_id: userId,
        dish_name: dishName,
      })
      applyBasket(data)
    } catch (e) {
      console.error('Не удалось удалить из корзины:', e)
    }
  }

  async function clearCart(userId: number) {
    try {
      const data = await cartApi.clear({ user_id: userId })
      applyBasket(data)
    } catch (e) {
      console.error('Не удалось очистить корзину:', e)
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
    increaseQuantity,
    decreaseQuantity,
    removeFromCart,
    clearCart,
    loadFromBackend,
    reset,
  }
})