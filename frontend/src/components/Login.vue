<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2 class="mb-4">Login</h2>
    <form @submit.prevent="missionLogin">
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" class="form-control" v-model="email" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" required />
      </div>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const emit = defineEmits(['loginSuccess'])

const email = ref('')
const password = ref('')
const errorMsg = ref('')

async function missionLogin() {
  errorMsg.value = ''
  try {
    const response = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await response.json()
    if (!response.ok) {
      errorMsg.value = data.error || 'Login failed'
      return
    }
    alert(`Login successful! Role: ${data.role}`)
    emit('loginSuccess', data.role)
    
  } catch (err) {
    errorMsg.value = 'Could not connect to server'
  }
}
</script>