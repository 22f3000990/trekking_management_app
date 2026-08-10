<template>
  <div class="container mt-5">
    <h2 class="mb-4">Admin Dashboard</h2>

    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-center p-3">
          <h5>Total Treks</h5>
          <p class="fs-3">{{ stats.total_treks }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center p-3">
          <h5>Total Users</h5>
          <p class="fs-3">{{ stats.total_users }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center p-3">
          <h5>Total Staff</h5>
          <p class="fs-3">{{ stats.total_staff }}</p>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center p-3">
          <h5>Total Bookings</h5>
          <p class="fs-3">{{ stats.total_bookings }}</p>
        </div>
      </div>
    </div>

    <hr />
    
<hr>

    <h4>Add Staff</h4>
    <form @submit.prevent="staffAdd" class="mb-4" style="max-width: 400px;">
      <input type="text" class="form-control mb-2" v-model="staffName" placeholder="Name" required />
      <input type="email" class="form-control mb-2" v-model="staffEmail" placeholder="Email" required />
      <input type="password" class="form-control mb-2" v-model="staffPassword" placeholder="Password" required />
      <button type="submit" class="btn btn-primary">Add Staff</button>
      <div v-if="staffMsg" class="alert alert-info mt-2">{{ staffMsg }}</div>
    </form>

    <hr />

    <h4>Create Trek</h4>
    <form @submit.prevent="launchNewTrek" class="mb-4" style="max-width: 400px;">
      <input type="text" class="form-control mb-2" v-model="trekName" placeholder="Trek Name" required />
      <input type="text" class="form-control mb-2" v-model="trekLocation" placeholder="Location" required />
      <select class="form-control mb-2" v-model="trekDifficulty" required>
        <option value="">Select Difficulty</option>
        <option value="Easy">Easy</option>
        <option value="Moderate">Moderate</option>
        <option value="Hard">Hard</option>
      </select>
      <input type="number" class="form-control mb-2" v-model="trekDuration" placeholder="Duration (days)" required />
      <input type="number" class="form-control mb-2" v-model="trekSlots" placeholder="Available Slots" required />
      <input type="date" class="form-control mb-2" v-model="trekStart" placeholder="startdate" required />
      <input type="date" class="form-control mb-2" v-model="trekEnd" placeholder="end date" required />
      <button type="submit" class="btn btn-primary">
        {{ editingTrekId ? 'Update Trek' : 'Create Trek' }}
      </button>
      <div v-if="trekMsg" class="alert alert-info mt-2">{{ trekMsg }}</div>
    </form>

    <hr />

    <h4>All Bookings</h4>
    <table class="table">
      <thead>
        <tr>
          <th>Booking ID</th>
          <th>User</th>
          <th>Trek</th>
          <th>Status</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in allBookings" :key="booking.booking_id">
          <td>{{ booking.booking_id }}</td>
          <td>{{ booking.user_name }}</td>
          <td>{{ booking.trek_name }}</td>
          <td>{{ booking.status }}</td>
          <td>{{ booking.booking_date }}</td>
        </tr>
      </tbody>
    </table>

    <hr />
    <button class="btn btn-outline-primary mb-3" @click="triggerReport">
      Send Monthly Report (Email)
    </button>

    <hr />

    <h4>All Trekkers</h4>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in trekkersOnly" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.status }}</td>
          <td>
            <button class="btn btn-danger btn -sm" @click="blacklistUser(u.id)" v-if="u.status !== 'blacklisted'">
              Blacklist
            </button>
            <button class="btn btn-success btn-sm" @click="unblacklistUser(u.id)" v-if="u.status === 'blacklisted'">
              Unblacklist
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <hr />

    <h4>All Staff</h4>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in staffOnly" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.name }}</td>
          <td>{{ u.email }}</td>
          <td>{{ u.status }}</td>
          <td>
            <button class="btn btn-danger btn -sm" @click="blacklistUser(u.id)" v-if="u.status !== 'blacklisted'">
              Blacklist
            </button>
            <button class="btn btn-success btn-sm" @click="unblacklistUser(u.id)" v-if="u.status === 'blacklisted'">
              Unblacklist
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <hr />

    <h4>Assign Staff to Trek</h4>
    <form @submit.prevent="assignStaffKro" class="mb-4" style="max-width: 400px;">
      <input type="number" class="form-control mb-2" v-model="assignTrekId" placeholder="Trek ID" required />
      <input type="number" class="form-control mb-2" v-model="assignStaffId" placeholder="Staff ID" required />
      <button type="submit" class="btn btn-primary">Assign</button>
      <div v-if="assignMsg" class="alert alert-info mt-2">{{ assignMsg }}</div>
    </form>

    <hr />







    <h4>All Treks</h4>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Assigned Staff</th>
          <th>Status</th>
          <th> Start Date</th>
          <th>End Date</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="trek in allTreks" :key="trek.id">
          <td>{{ trek.id }}</td>
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <!-- <td>{{ trek.difficulty }}</td> -->
          <td>{{ trek.assigned_staff }}</td>
          <td>{{ trek.status }}</td>
          <td>{{ trek.start_date }}</td>
          <td>{{ trek.end_date }}</td>
          <td>
            <button class="btn btn-sm btn-warning me-1" @click="editTrek(trek)">
              Edit
            </button>

            <button class="btn btn-sm btn-danger" @click="deleteTrek(trek.id)">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="editingTrekId" class="modal d-block" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">

            <div class="modal-header">
                <h5 class="modal-title">Edit Trek</h5>
                <button type="button" class="btn-close"
                        @click="editingTrekId = null"></button>
            </div>

            <div class="modal-body">

                <input
                    type="text"
                    class="form-control mb-2"
                    v-model="trekName"
                    placeholder="Trek Name"
                />

                <input
                    type="text"
                    class="form-control mb-2"
                    v-model="trekLocation"
                    placeholder="Location"
                />

                <select
                    class="form-control mb-2"
                    v-model="trekDifficulty"
                >
                    <option value="">Select Difficulty</option>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                </select>

                <input
                    type="number"
                    class="form-control mb-2"
                    v-model="trekDuration"
                    placeholder="Duration"
                />

                <input
                    type="number"
                    class="form-control mb-2"
                    v-model="trekSlots"
                    placeholder="Available Slots"
                />

                <input
                    type="date"
                    class="form-control mb-2"
                    v-model="trekStart"
                />

                <input
                    type="date"
                    class="form-control mb-2"
                    v-model="trekEnd"
                />

            </div>

            <div class="modal-footer">

                <button
                    class="btn btn-secondary"
                    @click="editingTrekId = null"
                >
                    Cancel
                </button>

                <button
                    class="btn btn-primary"
                    @click="launchNewTrek"
                >
                    Update Trek
                </button>

            </div>

        </div>
    </div>
</div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'

  const stats = ref({ total_treks: 0, total_users: 0, total_staff: 0, total_bookings: 0 })
  const allTreks = ref([])

const searchUser = ref('')
const searchedUsers = ref([])
const searched = ref(false)

  const staffName = ref('')
  const staffEmail = ref('')
  const staffPassword = ref('')
  const staffMsg = ref('')

  const trekName = ref('')
  const trekLocation = ref('')
  const trekDifficulty = ref('')
  const trekDuration = ref('')
  const trekSlots = ref('')
  const trekStart = ref('')
  const trekEnd = ref('')
  const trekMsg = ref('')
  const editingTrekId = ref(null)

  const assignTrekId = ref('')
  const assignStaffId = ref('')
  const assignMsg = ref('')


  const allBookings = ref([])
  const allUsers = ref([])
  const trekkersOnly = computed(() => allUsers.value.filter(u => u.role === 'trekker'))
  const staffOnly = computed(() => allUsers.value.filter(u => u.role === 'staff'))

  async function sabKuchDikhao() {
    const statsRes = await fetch('http://localhost:5000/api/admin/dashboard', { credentials: 'include' })
    stats.value = await statsRes.json()

    const treksRes = await fetch('http://localhost:5000/api/admin/treks', { credentials: 'include' })
    allTreks.value = await treksRes.json()

    const bookingsRes = await fetch('http://localhost:5000/api/admin/all-bookings', { credentials: 'include' })
    allBookings.value = await bookingsRes.json()

    const usersRes = await fetch('http://localhost:5000/api/admin/search-users?q=', { credentials: 'include' })
    allUsers.value = await usersRes.json()

  }

  async function assignStaffKro() {
    const response = await fetch('http://localhost:5000/api/admin/assign-staff', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ trek_id: parseInt(assignTrekId.value), staff_id: parseInt(assignStaffId.value) })
    })
    const data = await response.json()
    assignMsg.value = data.message || data.error
    sabKuchDikhao()
  }

  
  async function blacklistUser(userId) {
    const response = await fetch('http://localhost:5000/api/admin/blacklist-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ user_id: userId })
    })
    const data = await response.json()
    alert(data.message || data.error)
    sabKuchDikhao()
  }

  async function unblacklistUser(userId) {
    const response = await fetch('http://localhost:5000/api/admin/unblacklist-user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ user_id: userId })
    })
    const data = await response.json()
    alert(data.message || data.error)
    sabKuchDikhao()
  }


  async function staffAdd() {
    staffMsg.value = ''
    const response = await fetch('http://localhost:5000/api/admin/add-staff', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ name: staffName.value, email: staffEmail.value, password: staffPassword.value })
    })
    const data = await response.json()
    staffMsg.value = data.message || data.error
    sabKuchDikhao()
  }

  async function launchNewTrek() {
    trekMsg.value = ''

    let url = 'http://localhost:5000/api/admin/create-trek'
    let method = 'POST'

    if (editingTrekId.value) {
      url = `http://localhost:5000/api/admin/update-trek/${editingTrekId.value}`
      method = 'PUT'
    }

    const response = await fetch(url, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',

      body: JSON.stringify({
        name: trekName.value,
        location: trekLocation.value,
        difficulty: trekDifficulty.value,
        duration: trekDuration.value,
        available_slots: trekSlots.value,
        start_date: trekStart.value,
        end_date: trekEnd.value
      })
    })

    const data = await response.json()

    trekMsg.value = data.message || data.error

    editingTrekId.value = null

    sabKuchDikhao()
  }

  async function triggerReport() {
    const response = await fetch('http://localhost:5000/api/admin/trigger-report', {
      method: 'POST',
      credentials: 'include'
    })
    const data = await response.json()
    alert(data.message || data.error)
  }

  function editTrek(trek) {
    trekName.value = trek.name
    trekLocation.value = trek.location
    trekDifficulty.value = trek.difficulty
    trekDuration.value = trek.duration
    trekSlots.value = trek.available_slots
    trekStart.value = trek.start_date
    trekEnd.value = trek.end_date

    editingTrekId.value = trek.id
}



  async function deleteTrek(id) {
    if (!confirm("Are you sure you want to delete this trek?")) return

    const response = await fetch(`http://localhost:5000/api/admin/delete-trek/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })

    const data = await response.json()
    alert(data.message || data.error)

    sabKuchDikhao()
  }



  onMounted(() => {
    sabKuchDikhao()
  })
</script>