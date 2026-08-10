<template>
  <div>
    <div class="container text-end p-2" v-if="userRole">
      <button class="btn btn-outline-danger btn-sm" @click="logoutUser">Logout</button>
    </div>
    <div class="text-center mt-3" v-if="!userRole">
      <button class="btn btn-link" @click="showRegister = !showRegister">
        {{ showRegister ? 'Already have an account? Login' : 'New here? Register' }}
      </button>
    </div>
    <Register v-if="!userRole && showRegister" />
    <Login v-else-if = "!userRole" @loginSuccess="handleLoginSuccess" />

    <TrekkerDashboard v-if="userRole === 'trekker'" />
    <AdminDashboard v-if="userRole === 'admin'" />
    <StaffDashboard v-if = "userRole=== 'staff'" />
  </div>
</template>

<script setup>

import Login from './components/Login.vue'
import Register from './components/Register.vue'
import TrekkerDashboard from './components/TrekkerDashboard.vue'
import { ref, onMounted } from 'vue'
import AdminDashboard from './components/AdminDashboard.vue'
import StaffDashboard from './components/StaffDashboard.vue'
const showRegister = ref(false)
const userRole = ref('')

function handleLoginSuccess(role) {
  userRole.value = role
  localStorage.setItem('userRole', role)

}
async function logoutUser() {
  await fetch('http://localhost:5000/api/logout', {
    method: 'POST',
    credentials: 'include'
  })
  localStorage.removeItem('userRole')
  userRole.value = ''
}

onMounted (() => {
  const savedRole = localStorage.getItem('userRole')
  if (savedRole) {
    userRole.value = savedRole
        
  }
})
</script>