// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  // External configuration (12-Factor App)
  runtimeConfig: {
    // Private keys (server-only)
    apiSecret: process.env.API_SECRET || 'default-secret',
    
    // Public keys (available client-side)
    public: {
      apiUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8080',
      appName: process.env.NUXT_PUBLIC_APP_NAME || 'Item Management System',
      environment: process.env.NODE_ENV || 'development'
    }
  },

  // Server configuration
  nitro: {
    preset: 'node-server',
  },

  // Enable SSR (Server-Side Rendering) as required
  ssr: true,

  // App configuration
  app: {
    head: {
      title: 'Item Management System',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Distributed Systems Lab - Item Management' }
      ]
    }
  }
})