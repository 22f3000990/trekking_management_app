<template>
  <button class="btn btn-outline-primary mb-3" @click="exportMyBookings">
  Export Booking History (CSV)

  </button>

  <button class="btn btn-outline-success mb-3 ms-2" @click="downloadExport">
   Download My Bookings CSV
  </button>
  <div class="container mt-5">
    <h2 class="mb-4">Available Treks</h2>

    <div v-if="treks.length === 0" class="alert alert-info">No open treks right now.</div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="trek in treks" :key="trek.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ trek.name }}</h5>
            <p class="card-text">
                Location: {{ trek.location }}<br />
                Difficulty: {{ trek.difficulty }}<br />
                Duration: {{ trek.duration }} days<br />
                Slots left: {{ trek.available_slots }}<br />
                Dates: {{ trek.start_date }} to {{ trek.end_date }}
            </p>
            <button class="btn btn-success" @click="trekPeChalo(trek.id)">
              Book This Trek
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
    <div v-if="errorMsg" class="alert alert-danger mt-3">{{ errorMsg }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const treks = ref([])
const message = ref('')
const errorMsg = ref('')

async function exploreTreks() {
  try {
    const response = await fetch('http://localhost:5000/api/trekker/treks', {
      credentials: 'include'
    })
    const data = await response.json()
    treks.value = data
  } catch (err) {
    errorMsg.value = 'Could not load treks'
  }
}

async function trekPeChalo(trekId) {
  message.value = ''
  errorMsg.value = ''
  try {
    const response = await fetch(`http://localhost:5000/api/trekker/book/${trekId}`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await response.json()
    if (!response.ok) {
      errorMsg.value = data.error
      return
    }
    message.value = data.message
    exploreTreks()  
  } catch (err) {
    errorMsg.value = 'Could not book trek'
  }
}

async function exportMyBookings() {
  const response = await fetch('http://localhost:5000/api/trekker/export-bookings', {
    method: 'POST',
    credentials: 'include'
  })
  const data = await response.json()
  alert(data.message)
}

function downloadExport() {
  window.open('http://localhost:5000/api/trekker/download-export', '_blank')
}

onMounted(() => {
  exploreTreks()
})
</script>