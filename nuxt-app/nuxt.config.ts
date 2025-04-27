// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },

  // Allgemeine Konfigurationen

  modules: [
    '@nuxtjs/dotenv',
    '@nuxtjs/axios',
  ],

  plugins: [
    '~/plugins/api.js',
  ],


  // Runtime-Konfigurationen (client- und serverseitig verfügbar)
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:3001/api',
      appName: process.env.APP_NAME || 'Distributed Systems Lab - Shop App',
      debug: process.env.DEBUG === 'true'
    },
    private: {
      apiToken: process.env.API_TOKEN
    }
  },

  
});
