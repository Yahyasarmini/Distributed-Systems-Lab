<template>
    <div>
      <!-- Überschrift für die Produktliste -->
      <h2>Unsere Produkte</h2>
      
      <!-- Ladeanzeige, wenn die Produkte noch geladen werden -->
      <div v-if="loading" class="loading">
        Produkte werden geladen...
      </div>
      
      <!-- Fehlermeldung, falls ein Fehler beim Laden der Produkte auftritt -->
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <!-- Produktliste, wenn die Produkte erfolgreich geladen wurden -->
      <div v-else class="product-grid">
        <!-- Einzelne Produktkarte -->
        <div v-for="product in products" :key="product.id" class="product-card">
          <!-- Produktbild -->
          <img :src="product.imageUrl" :alt="product.name" class="product-image" />
          <!-- Produktname -->
          <h3>{{ product.name }}</h3>
          <!-- Produktbeschreibung -->
          <p class="product-description">{{ product.description }}</p>
          <!-- Produktpreis -->
          <p class="product-price">{{ formatPrice(product.price) }}</p>
          <!-- Aktionen für das Produkt -->
          <div class="product-actions">
            <!-- Button zum Hinzufügen des Produkts in den Warenkorb -->
            <button 
              @click="addToCart(product)" 
              :disabled="!product.inStock"
              class="add-to-cart-button"
            >
              {{ product.inStock ? 'In den Warenkorb' : 'Nicht verfügbar' }}
            </button>
            <!-- Link zu den Produktdetails -->
            <nuxt-link :to="`/product/${product.id}`" class="view-details">
              Details ansehen
            </nuxt-link>
          </div>
        </div>
      </div>
      
      <!-- Debug-Informationen, nur im Entwicklungsmodus sichtbar -->
      <div v-if="$config.debug" class="debug-info">
        <p>Debug-Modus aktiv</p>
        <p>API URL: {{ $config.apiBaseUrl }}</p>
        <p>Produkte geladen: {{ products.length }}</p>
      </div>
    </div>
  </template>
  
  <script>
  /**
   * ProductList Komponente
   * Diese Komponente demonstriert mehrere 12-Factor-Prinzipien:
   * - III. Config: Verwendet externalisierte Konfiguration ($config)
   * - VI. Processes: Stateless Komponente, speichert keine Daten lokal
   * - IX. Disposability: Implementiert Fehlerbehandlung für API-Aufrufe
   */
  export default {
    data() {
      return {
        products: [],
        loading: false,
        error: null
      }
    },
    async mounted() {
      await this.loadProducts()
    },
    methods: {
      async loadProducts() {
        try {
          this.loading = true
          this.products = await this.$api.getProducts()
        } catch (error) {
          this.error = 'Fehler beim Laden der Produkte'
          console.error(this.error, error)
        } finally {
          this.loading = false
        }
      },
      
      async addToCart(product) {
        try {
          await this.$api.addToCart(product)
          this.$emit('cart-updated')
          alert(`${product.name} wurde in den Warenkorb gelegt`)
        } catch (error) {
          console.error('Fehler beim Hinzufügen des Produkts zum Warenkorb:', error)
        }
      },
      
      formatPrice(price) {
        return new Intl.NumberFormat('de-DE', {
          style: 'currency',
          currency: this.$config.currency || 'EUR'
        }).format(price)
      }
    }
  }
  </script>
  
  <style scoped>
  .product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
  }
  
  .product-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
    display: flex;
    flex-direction: column;
  }
  
  .product-image {
    width: 100%;
    height: 180px;
    object-fit: cover;
    margin-bottom: 1rem;
    border-radius: 4px;
  }
  
  .product-description {
    color: #666;
    flex-grow: 1;
  }
  
  .product-price {
    font-weight: bold;
    font-size: 1.2rem;
    margin: 0.5rem 0;
  }
  
  .product-actions {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .add-to-cart-button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .add-to-cart-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  
  .view-details {
    text-align: center;
    color: #2c3e50;
    text-decoration: none;
  }
  
  .loading, .error {
    padding: 1rem;
    text-align: center;
  }
  
  .error {
    color: red;
  }
  
  .debug-info {
    margin-top: 2rem;
    padding: 1rem;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  </style>