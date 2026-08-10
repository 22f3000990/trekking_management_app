<template>
  <div class="container mt-5">
    <h2 class="mb-4">Staff Dashboard - My Assigned Treks</h2>
    <div class="row mb-4">

      <div class="col-md-4">
        <div class="card text-center p-3">
          <h5>Assigned Treks</h5>
          <h2>{{ myTreks.length }}</h2>
        </div>
      </div>



    </div>

    <div v-if="myTreks.length === 0" class="alert alert-info">No treks assigned yet.</div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="trek in myTreks" :key="trek.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ trek.name }}</h5>
            <p class="card-text">
              Status: {{ trek.status }}<br />
              Slots left: {{ trek.available_slots }}
            </p>

            <div class="mb-2">
              <select class="form-control mb-2" v-model="statusUpdates[trek.id]">
                <option value="">Change Status</option>
                <option value="Open">Open</option>
                <option value="Closed">Closed</option>
              </select>
              <input type="number" class="form-control mb-2" v-model="slotUpdates[trek.id]"
                placeholder="New slot count" />
              <button class="btn btn-primary btn-sm" @click="trekUpdateKro(trek.id)">Update Trek</button>
              <button v-if="trek.status === 'Completed'" class="btn btn-success btn-sm ms-2"
                @click="markComplete(trek.id)">
                change stuts
              </button>
              <button v-else class="btn btn-success btn-sm ms-2" @click="markComplete(trek.id)">Mark Completed</button>
            </div>
            <div v-if="trek.users.length > 0">

              <h6>Registered Users</h6>

              <ul>
                <li v-for="user in trek.users" :key="user.id">
                  {{ user.name }} - {{ user.email }}
                </li>
              </ul>

            </div>

            <div v-else>
              <small>No users registered</small>
            </div>

          </div>
        </div>
      </div>
    </div>

    <div v-if="msg" class="alert alert-success mt-3">{{ msg }}</div>
  </div>
<div class="mt-4">
    <h4>Completed Treks</h4>

    <div v-if="completedTreks.length === 0" class="alert alert-info">
        No completed treks yet.
    </div>

    <div class="row" v-else>
        <div
            class="col-md-4 mb-3"
            v-for="trek in completedTreks"
            :key="trek.id"
        >
            <div class="card">
                <div class="card-body">
                    <h5>{{ trek.name }}</h5>

                    <p>
                        Status:
                        <span class="text-success">
                            {{ trek.status }}
                        </span>
                    </p>

                    <p>
                        Registered Users:
                        {{ trek.registered_users }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>

</template>

<script setup>
  // import { ref, reactive, onMounted } from 'vue'
  import { ref, reactive, onMounted, computed } from 'vue'

  const myTreks = ref([])
  const statusUpdates = reactive({})
  const slotUpdates = reactive({})
  const msg = ref('')

  async function showMyTreks() {
    const response = await fetch('http://localhost:5000/api/staff/my-treks', { credentials: 'include' })
    myTreks.value = await response.json()
  }

  async function trekUpdateKro(trekId) {
    const body = {}
    if (statusUpdates[trekId]) body.status = statusUpdates[trekId]
    if (slotUpdates[trekId]) body.available_slots = parseInt(slotUpdates[trekId])

    const response = await fetch(`http://localhost:5000/api/staff/update-trek/${trekId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify(body)
    })
    const data = await response.json()
    msg.value = data.message || data.error
    showMyTreks()
  }

  const completedTreks = computed(() => {
    return myTreks.value.filter(
        trek => trek.status === 'Completed'
    )
})
  async function markComplete(trekId) {
    const response = await fetch(`http://localhost:5000/api/staff/complete-trek/${trekId}`, {
      method: 'POST',
      credentials: 'include'
    })
    const data = await response.json()
    msg.value = data.message || data.error
    showMyTreks()
  }

  onMounted(() => {
    showMyTreks()
  })
</script>