import api from './index'

export const authApi = {
  exchangeToken: (token: string) =>
    api.post('/auth/verify', { token }),

  verifyUser: () =>
    api.get('/auth/verify_user')
}