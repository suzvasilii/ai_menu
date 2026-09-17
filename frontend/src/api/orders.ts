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

export const ordersApi = {
    create: async (order: OrderCreate): Promise<{ status: string; message: string }> => {
        const response = await api.post('/order/create_order', order)
        return response.data
    }
}