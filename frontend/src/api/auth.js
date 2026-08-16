import apiClient from './client'

export const register = (payload) =>
  apiClient.post('/api/users/register/', payload).then((res) => res.data)

export const loginWithPassword = (identifier, password) =>
  apiClient
    .post('/api/users/login/password/', { identifier, password })
    .then((res) => res.data)

export const requestOtp = (phone) =>
  apiClient
    .post('/api/users/login/otp/request/', { phone })
    .then((res) => res.data)

export const verifyOtp = (phone, code) =>
  apiClient
    .post('/api/users/login/otp/verify/', { phone, code })
    .then((res) => res.data)

export const updateProfile = (payload) =>
  apiClient
    .patch('/api/users/profile/', payload)
    .then((res) => res.data)