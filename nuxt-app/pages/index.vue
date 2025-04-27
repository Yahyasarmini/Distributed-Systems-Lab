<template>
    <div class="container">
      <h1>Shopping List Manager</h1>
  
      <!-- Success and error messages -->
      <div v-if="messages.length">
        <div v-for="(msg, index) in messages" :key="index" :class="`alert ${msg.type}`">
          {{ msg.text }}
        </div>
      </div>
  
      <!-- Shopping list table -->
      <h2>All Shopping Items</h2>
      <table>
        <thead>
          <tr>
            <th>Item Name</th>
            <th>Quantity</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.amount }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        items: [],
        messages: []
      };
    },
    async asyncData({ $axios }) {
      try {
        const items = await $axios.$get('/api/shopping_items');
        return { items };
      } catch (error) {
        return { items: [], messages: [{ type: 'error', text: 'Failed to load items.' }] };
      }
    }
  };
  </script>
  
  <style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .alert {
    padding: 10px;
    margin-bottom: 10px;
  }
  
  .alert.error {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  .alert.success {
    background-color: #d4edda;
    color: #155724;
  }
  </style>