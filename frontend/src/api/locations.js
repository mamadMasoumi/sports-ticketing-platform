import apiClient from './client'

export const getCities = () =>
  apiClient.get('/api/locations/cities/').then((res) => res.data)

export const getVenues = (cityId) => {
  const params = cityId ? { city_id: cityId } : {}
  return apiClient.get('/api/locations/venues/', { params }).then((res) => res.data)
}