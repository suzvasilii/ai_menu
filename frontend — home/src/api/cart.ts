import api from './index'

export interface BasketItemPayload {
  dish_name: string
  quantity: number
}

export interface BasketAddPayload {
  user_id: number
  items: BasketItemPayload[]
}

export interface BasketRemovePayload {
  user_id: number
  dish_name: string
}

export interface BasketUpdatePayload {
  user_id: number
  dish_name: string
  quantity: number
}

export interface BasketClearPayload {
  user_id: number
}

export interface BasketItemResponse {
  dish_name: string
  quantity: number
  image_url?: string | null
}

export interface BasketResponse {
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

  removeItem: async (payload: BasketRemovePayload): Promise<BasketResponse> => {
    const { data } = await api.post<BasketResponse>('/basket/remove', payload)
    return data
  },

  updateItem: async (payload: BasketUpdatePayload): Promise<BasketResponse> => {
    const { data } = await api.post<BasketResponse>('/basket/update', payload)
    return data
  },

  clear: async (payload: BasketClearPayload): Promise<BasketResponse> => {
    const { data } = await api.post<BasketResponse>('/basket/clear', payload)
    return data
  },
}