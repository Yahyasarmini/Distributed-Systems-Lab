// plugins/api.client.ts
export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiUrl

  const api = {
    async getProducts() {
      try {
        const response = await $fetch(`${baseURL}/items`)
        return response
      } catch (error) {
        console.error('Error fetching products:', error)
        throw error
      }
    },

    async createProduct(product: Record<string, any>) {
      try {
        const response = await $fetch(`${baseURL}/items`, {
          method: 'POST',
          body: product
        })
        return response
      } catch (error) {
        console.error('Error creating product:', error)
        throw error
      }
    },

    async deleteProduct(id: string) {
      try {
        await $fetch(`${baseURL}/items/${id}`, {
          method: 'DELETE'
        })
      } catch (error) {
        console.error('Error deleting product:', error)
        throw error
      }
    },

    async addToCart(product: Record<string, any>) {
      // Mock implementation - würde normalerweise an Backend gehen
      console.log('Adding to cart:', product)
      return Promise.resolve()
    }
  }

  return {
    provide: {
      api
    }
  }
})