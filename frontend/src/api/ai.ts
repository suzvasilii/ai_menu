import api from './index'

export const aiApi = {
  exchangeToken: (token: string) =>
    api.post('/auth/verify', { token }),
}