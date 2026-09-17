import api from './index'

export interface Dish {
    id: number
    name: string
    category: string
    image_url: string
}

export interface DishCreatePayload {
    name: string
    category: string
    image_url?: string
}

export interface DishCreatePhotoPayload {
    file: File
    name: string
    category: string
}

export const dishesApi = {
    getAll: async (): Promise<Dish[]> => {
        const response = await api.get('/dish/get')
        return response.data.map((dish: Dish) => ({
            ...dish,
            image_url: `http://happsrv.mooo.com:8000/${dish.image_url}`
        }))
    },

    create: async (payload: DishCreatePayload): Promise<Dish> => {
        const response = await api.post('/dish/create_by_name', payload)
        return response.data
    },

    delete: async (id: number): Promise<void> => {
        await api.delete(`/dish/del/${id}`)
    },

    createByPhoto: async (payload: DishCreatePhotoPayload): Promise<void> => {
        const formData = new FormData()
        formData.append('file', payload.file)
        formData.append('name', payload.name)
        formData.append('category', payload.category)
        await api.post('/dish/create_by_photo', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        })
    },
}