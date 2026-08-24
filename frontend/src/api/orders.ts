import axios from 'axios'

const BASE_URL = "http://localhost:8000"
const API_URL = `${BASE_URL}/api`


export interface OrderItem {
    name: string
    quantity: number
}

export interface OrderCreate {
    customer_name?: string
    comment?: string
    items: OrderItem[]
}

export const ordersApi = {
    create: async (order: OrderCreate): Promise<{ status: string; message: string }> => {
        const response = await axios.post(`${API_URL}/orders`, order)
        return response.data
    }
}