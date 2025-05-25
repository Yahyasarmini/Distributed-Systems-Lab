<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <NuxtLink to="/" class="nav-brand">
          {{ appName }}
        </NuxtLink>
        <div class="nav-links">
          <NuxtLink to="/" class="nav-link">Home</NuxtLink>
          <NuxtLink to="/items" class="nav-link">Items</NuxtLink>
        </div>
        <div class="env-badge" :class="envClass">
          {{ environment }}
        </div>
      </div>
    </nav>
    
    <main class="main-content">
      <NuxtPage />
    </main>
    
    <footer class="footer">
      <p>&copy; 2025 Distributed Systems Lab - Built with Nuxt.js</p>
    </footer>
  </div>
</template>

<script setup>
const config = useRuntimeConfig()
const appName = config.public.appName
const environment = config.public.environment

const envClass = computed(() => {
  switch (environment) {
    case 'production':
      return 'env-production'
    case 'development':
      return 'env-development'
    default:
      return 'env-staging'
  }
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #333;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.env-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: bold;
  text-transform: uppercase;
}

.env-development {
  background-color: #f39c12;
}

.env-production {
  background-color: #27ae60;
}

.env-staging {
  background-color: #3498db;
}

.main-content {
  flex: 1;
  padding: 2rem 0;
}

.footer {
  background-color: #34495e;
  color: white;
  text-align: center;
  padding: 1rem 0;
  margin-top: auto;
}

.footer p {
  margin: 0;
}
</style>