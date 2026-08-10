<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2 class="mb-4">Register</h2>
    <form @submit.prevent="freshEntry">
      <div class="mb-3">
        <label class="form-label">Name</label>
        <input type="text" class="form-control" v-model="name" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input type="email" class="form-control" v-model="email" required />
      </div>
      <div class="mb-3">
        <label class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" required />
      </div>
      <div v-if="errorMsg" class="alert alert-danger">{{ errorMsg }}</div>
      <div v-if="successMsg" class="alert alert-success">{{ successMsg }}</div>
      <button type="submit" class="btn btn-primary w-100">Register</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const successMsg = ref('')

async function freshEntry() {
    errorMsg.value = ''
    try {
        const response = await fetch('http://localhost:5000/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({ name: name.value , email: email.value, password: password.value})

        })
        const data = await response.json()
        if (!response.ok) {
            errorMsg.value = data.error || 'Resgisteration failed'
            return
        }
        successMsg.value = 'Welcome Trekker! you can login now '

    } catch (err){
        errorMsg.value = 'Could not connect to server'
    }
  
}
</script>