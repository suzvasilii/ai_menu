import api from './index'

export interface OrderItem {
    name: string
    quantity: number
}

export interface OrderCreate {
    customer_name?: string
    user_id: number
    comment?: string
    dishes: OrderItem[]
}

export interface Recommendation {
    name: string
    image_url: string
}

export const ordersApi = {
    create: async (order: OrderCreate): Promise<{ status: string; message: string }> => {
        const response = await api.post('/order/create_order', order)
        return response.data
    },

    getRecommendations: async (userId: number, dishName: string): Promise<Recommendation[]> => {
        const response = await api.get<Recommendation[]>('/order/rec', {
            params: { user_id: userId, dish_name: dishName },
        })
        return response.data
    },
}