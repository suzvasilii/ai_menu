import api from './index'

interface BasketItemPayload {
  dish_name: string
  quantity: number
}

interface BasketAddPayload {
  user_id: number
  items: BasketItemPayload[]
}

interface BasketItemResponse {
  dish_name: string
  quantity: number
  image_url?: string | null
}

interface BasketResponse {
  id: number
  user_id: number
  items: BasketItemResponse[]
}

export const cartApi = {
  add: async (payload: BasketAddPayload): Promise<BasketResponse> => {
    const { data } = await api.post<BasketResponse>('/basket/add', payload)
    return data
  },

  get: async (userId: number): Promise<BasketResponse> => {
    const { data } = await api.get<BasketResponse>('/basket/get', {
      params: { user_id: userId },
    })
    return data
  },
}