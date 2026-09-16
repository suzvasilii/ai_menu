import api from './index'

export interface Dish {
    id: number
    name: string
    category: string
    image_url: string
}

export const dishesApi = {
    getAll: async (): Promise<Dish[]> => {
        const response = await api.get('/dish/get')
        return response.data.map((dish: Dish) => ({
            ...dish,
            image_url: `http://happsrv.mooo.com:8000/${dish.image_url}`
        }))
    },

    create: async (name: string): Promise<Dish> => {
        const response = await api.post('/dish/create_by_name', { name })
        return response.data
    },

    delete: async (id: number): Promise<void> =>{
        await api.delete('/dish/del/${id}')
    },

    createByPhoto: async (file: File): Promise<void> => {
    const formData = new FormData()
    formData.append('file', file)
    await axios.post('/dish/create_by_photo', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    })
    },
}
