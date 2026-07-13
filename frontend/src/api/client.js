import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
})

export default api

export async function getStats() {
  const { data } = await api.get('/stats')
  return data
}

export async function getItems(page = 1) {
  const { data } = await api.get('/items', { params: { page } })
  return data
}

export async function createItem(payload) {
  const { data } = await api.post('/items', payload)
  return data
}

export async function updateItem(id, payload) {
  const { data } = await api.put(`/items/${id}`, payload)
  return data
}

export async function deleteItem(id) {
  await api.delete(`/items/${id}`)
}

export async function getShops(page = 1) {
  const { data } = await api.get('/shops', { params: { page } })
  return data
}

export async function getShopChoices() {
  const { data } = await api.get('/shops/choices')
  return data
}

export async function getShop(id) {
  const { data } = await api.get(`/shops/${id}`)
  return data
}

export async function getShopWarrantyItems(id) {
  const { data } = await api.get(`/shops/${id}/warranty-items`)
  return data
}

export async function createShop(payload) {
  const { data } = await api.post('/shops', payload)
  return data
}

export async function updateShop(id, payload) {
  const { data } = await api.put(`/shops/${id}`, payload)
  return data
}

export async function deleteShop(id, linkedItems = false) {
  await api.delete(`/shops/${id}`, { params: { linked_items: linkedItems } })
}

export async function searchItemsAndShops(query) {
  const { data } = await api.get('/search', { params: { query } })
  return data
}

export async function getDatabaseInfo() {
  const { data } = await api.get('/database/info')
  return data
}

export async function purgeDatabase(option) {
  const { data } = await api.post('/database/purge', { option })
  return data
}

export async function restoreDatabase(file) {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post('/database/restore', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export function exportDatabaseUrl() {
  const base = import.meta.env.VITE_API_URL || '/api'
  return `${base}/database/export`
}
