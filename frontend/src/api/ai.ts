import api from './index'

export interface RetryRequest {
  dish_name: string
  attempts: string[]
}

export interface DishResponse {
  data_url: string
}

export interface DishesResponse {
  images: DishResponse[]
  dish_name: string
  category: string
  selected_image?: string
}

export interface ClassifiedResponse {
  dish_name: string
  category: string
}

export interface OfficiantResponse {
  answer: string
}

export const aiApi = {
  askOfficiant: async (question: string): Promise<OfficiantResponse> => {
    const response = await api.get<OfficiantResponse>(`/ai/officiant/${question}`)
    return response.data
  },

  getDishPhoto: async (dish_name: string): Promise<DishesResponse> => {
    const response = await api.get<DishesResponse>(`/ai/get_name/${dish_name}`)
    return response.data
  },

  retryGetDishPhoto: async (request: RetryRequest): Promise<DishesResponse> => {
    const response = await api.post<DishesResponse>('/ai/retry_get_name', request)
    return response.data
  },

  classifyByPhoto: async (photo: File): Promise<ClassifiedResponse> => {
    const formData = new FormData()
    formData.append('photo', photo)
    const response = await api.post<ClassifiedResponse>('/ai/classify_photo', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
}