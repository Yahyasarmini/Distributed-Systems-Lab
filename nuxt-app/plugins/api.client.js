// nuxt-app/plugins/api.client.js
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  // API helper functions
  const api = {
    // Items CRUD operations
    async getItems() {
      return await $fetch(`${config.public.apiUrl}/items`)
    },
    
    async getItem(id) {
      return await $fetch(`${config.public.apiUrl}/items/${id}`)
    },
    
    async createItem(item) {
      return await $fetch(`${config.public.apiUrl}/items`, {
        method: 'POST',
        body: item
      })
    },
    
    async updateItem(id, item) {
      return await $fetch(`${config.public.apiUrl}/items/${id}`, {
        method: 'PUT',
        body: item
      })
    },
    
    async deleteItem(id) {
      return await $fetch(`${config.public.apiUrl}/items/${id}`, {
        method: 'DELETE'
      })
    }
  }
  
  return {
    provide: {
      api
    }
  }
})