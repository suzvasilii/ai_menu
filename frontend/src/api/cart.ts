import api from './index'

interface BasketItem {
  dish_name: string
  quantity: number
  image_url?: string | null
}

interface BasketAddRequest {
  user_id: number
  items: BasketItem[]
}

interface BasketResponse {
  id: number
  user_id: number
  items: BasketItem[]
}

export const cartApi = {
  add: async (payload: BasketAddRequest): Promise<void> => {
    await api.post('/basket/add', payload)
  },

  get: async (userId: number): Promise<BasketResponse> => {
    const response = await api.get<BasketResponse>('/basket/get', {
      params: { user_id: userId }
    })
    return response.data
  },
}