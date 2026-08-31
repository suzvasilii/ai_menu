import axios from 'axios'
import type { UserData } from "@/stores/user.ts";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const API_URL = `${BACKEND_URL}/auth`

export const authApi = {
    reg: async (login: string): Promise<{ data: UserData }> => {
        const response = await axios.post(`${API_URL}/reg`, { login })
        return response.data
    },

    login: async (login: string): Promise<{ data: UserData }> => {
        const response = await axios.post(`${API_URL}/login`, { login })
        return response.data
    }
}