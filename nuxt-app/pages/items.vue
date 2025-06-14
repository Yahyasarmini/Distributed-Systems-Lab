<template>
  <div class="container">
    <h1>Items Management</h1>
    
    <!-- Connection Status -->
    <div v-if="connectionError" class="connection-error">
      <h3>Verbindungsproblem</h3>
      <p>{{ connectionError }}</p>
      <button @click="testConnection">Verbindung testen</button>
      <p><strong>API URL:</strong> {{ apiUrl }}</p>
    </div>
    
    <!-- Add Item Form -->
    <div class="form-section">
      <h2>Add New Item</h2>
      <form @submit.prevent="createItem">
        <input 
          v-model="newItem.name" 
          placeholder="Item Name" 
          required
        />
        <input 
          v-model.number="newItem.quantity" 
          type="number" 
          placeholder="Quantity" 
          required
        />
        <button type="submit" :disabled="loading">
          {{ loading ? 'Wird hinzugefügt...' : 'Add Item' }}
        </button>
      </form>
    </div>

    <!-- Items List -->
    <div class="items-section">
      <h2>Items List</h2>
      <div v-if="loading">Loading...</div>
      <div v-else-if="error" class="error">
        {{ error }}
        <button @click="fetchItems" class="retry-btn">Retry</button>
      </div>
      <div v-else-if="items.length === 0">No items found</div>
      <div v-else class="items-grid">
        <div v-for="item in items" :key="item.id" class="item-card">
          <div v-if="editingId === item.id" class="edit-form">
            <input v-model="editItem.name" />
            <input v-model.number="editItem.quantity" type="number" />
            <button @click="updateItem(item.id)">Save</button>
            <button @click="cancelEdit">Cancel</button>
          </div>
          <div v-else>
            <h3>{{ item.name }}</h3>
            <p>Quantity: {{ item.quantity }}</p>
            <div class="actions">
              <button @click="startEdit(item)">Edit</button>
              <button @click="deleteItem(item.id)" class="delete">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// Get API URL from runtime config
const config = useRuntimeConfig()
const apiUrl = config.public.apiUrl || 'http://localhost:8080'

// State
const items = ref([])
const loading = ref(false)
const error = ref('')
const connectionError = ref('')
const newItem = ref({ name: '', quantity: 0 })
const editItem = ref({ name: '', quantity: 0 })
const editingId = ref(null)

// Test API connection
const testConnection = async () => {
  try {
    connectionError.value = ''
    console.log('Testing connection to:', apiUrl)
    
    const response = await $fetch(`${apiUrl}/health`, {
      timeout: 5000
    })
    console.log('Health check response:', response)
    connectionError.value = ''
  } catch (err) {
    console.error('Connection test failed:', err)
    connectionError.value = `Cannot connect to backend at ${apiUrl}. Error: ${err.message}`
  }
}

// Fetch all items
const fetchItems = async () => {
  loading.value = true
  error.value = ''
  try {
    console.log('Fetching items from:', `${apiUrl}/items`)
    const response = await $fetch(`${apiUrl}/items`, {
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    console.log('Items response:', response)
    items.value = response
  } catch (err) {
    console.error('Error fetching items:', err)
    error.value = `Failed to fetch items: ${err.message}`
    
    // Test connection if fetch fails
    if (err.message.includes('fetch')) {
      await testConnection()
    }
  } finally {
    loading.value = false
  }
}

// Create new item
const createItem = async () => {
  if (!newItem.value.name.trim()) {
    error.value = 'Item name is required'
    return
  }
  
  loading.value = true
  error.value = ''
  
  try {
    console.log('Creating item:', newItem.value)
    console.log('POST URL:', `${apiUrl}/items`)
    
    const response = await $fetch(`${apiUrl}/items`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: newItem.value,
      timeout: 10000
    })
    
    console.log('Create response:', response)
    items.value.push(response)
    newItem.value = { name: '', quantity: 0 }
    error.value = ''
  } catch (err) {
    console.error('Error creating item:', err)
    error.value = `Failed to create item: ${err.message}`
    
    // Detail-logging für besseres Debugging
    if (err.data) {
      console.error('Error details:', err.data)
    }
  } finally {
    loading.value = false
  }
}

// Start editing
const startEdit = (item) => {
  editingId.value = item.id
  editItem.value = { ...item }
}

// Cancel editing
const cancelEdit = () => {
  editingId.value = null
  editItem.value = { name: '', quantity: 0 }
}

// Update item
const updateItem = async (id) => {
  try {
    const response = await $fetch(`${apiUrl}/items/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: editItem.value
    })
    const index = items.value.findIndex(item => item.id === id)
    if (index !== -1) {
      items.value[index] = response
    }
    cancelEdit()
  } catch (err) {
    error.value = `Failed to update item: ${err.message}`
    console.error(err)
  }
}

// Delete item
const deleteItem = async (id) => {
  if (!confirm('Are you sure you want to delete this item?')) return
  
  try {
    await $fetch(`${apiUrl}/items/${id}`, {
      method: 'DELETE'
    })
    items.value = items.value.filter(item => item.id !== id)
  } catch (err) {
    error.value = `Failed to delete item: ${err.message}`
    console.error(err)
  }
}

// Load items on mount
onMounted(async () => {
  console.log('Component mounted, API URL:', apiUrl)
  await testConnection()
  await fetchItems()
})
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.connection-error {
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.connection-error h3 {
  margin-top: 0;
  color: #856404;
}

.form-section {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

form {
  display: flex;
  gap: 10px;
  align-items: center;
}

input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

button {
  padding: 8px 16px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background: #0056b3;
}

button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

button.delete {
  background: #dc3545;
}

button.delete:hover {
  background: #c82333;
}

button.retry-btn {
  background: #28a745;
  margin-left: 10px;
}

button.retry-btn:hover {
  background: #218838;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.item-card {
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.error {
  color: #dc3545;
  padding: 10px;
  background: #f8d7da;
  border-radius: 4px;
  margin: 10px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>