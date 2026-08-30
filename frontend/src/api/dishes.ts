import axios from 'axios'

const BASE_URL = "http://localhost:8000"
const API_URL = `${BASE_URL}/dish`

export interface Dish {
    id: number
    name: string
    image_url: string
}

export const dishesApi = {
    getAll: async (): Promise<Dish[]> => {
        const response = await axios.get(`${API_URL}/get`)
        return response.data.map((dish: Dish) => ({
            ...dish,
            image_url: `${BASE_URL}${dish.image_url}`
        }))
    },

    create: async (name: string): Promise<Dish> => {
        const response = await axios.post(`${API_URL}/create_by_name`, { name })
        return response.data
    },

    delete: async (id: number): Promise<void> =>{
        await axios.delete(`${API_URL}/del/${id}`)
    },

    createByPhoto: async (file: File): Promise<void> => {
    const formData = new FormData()
    formData.append('file', file)
    await axios.post(`${API_URL}/create_by_photo`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    },
}
