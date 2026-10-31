<script setup>
import { computed, ref, onMounted } from 'vue'

const todos = ref([])
const newTitle = ref('')
const newTaskComplexity = ref('Medium')
const API_URL = 'http://localhost:8001'

const shieldDone = `<svg viewBox="0 0 18 20" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 1 L17 4 L17 11 Q17 17 9 19 Q1 17 1 11 L1 4 Z" fill="#3a7830" stroke="#5ab040" stroke-width="1.2"/>
                      <polyline points="5,10 8,13 13,7" stroke="#90e060" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>`
const shieldEmpty = ` <svg viewBox="0 0 18 20" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 1 L17 4 L17 11 Q17 17 9 19 Q1 17 1 11 L1 4 Z" fill="rgba(160,100,20,0.1)" stroke="#a07030" stroke-width="1.2"/>
                      <path d="M9 3 L15 5.5 L15 11 Q15 15.5 9 17.5 Q3 15.5 3 11 L3 5.5 Z" fill="none" stroke="rgba(160,100,20,0.3)" stroke-width="0.5"/>
                    </svg>`

const toastMessage = ref('')
const isToastVisible = ref(false)

// For a auth form
const formMode = ref('login')
const loginName = ref('')
const loginPassword = ref('')
const registerName = ref('')
const registerEmail = ref('')
const registerPassword = ref('')
const registerPasswordRepeat = ref('')
const formMessage = ref('')

const formTitle = computed(() =>
  formMode.value === 'login' ? 'Return to your quest' : 'Begin your adventure'
)

async function addTask() {
  toastMessage.value = 'By the light of the candle, a new deed has been recorded. 🪶📜'
  const res = await fetch(`${API_URL}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title: newTitle.value, complexity: newTaskComplexity.value, done: false })
  })
  newTitle.value = ''
  showToast()
  await loadTodos()
}

async function deleteTask(id) {
  try {
    const res = await fetch(`${API_URL}/todos/${id}`, {method: 'DELETE'})

    if (!res.ok) {
      throw new Error(`Delete failed: ${res.status}`)
    }

    toastMessage.value = "The magic dissipates. The task has vanished from the scroll. ⚱️"
    showToast()
    await loadTodos()
  } catch(error) {
    console.log(error)
    toastMessage.value = "Magic resists! The task clings to the parchment. 📜💥"
    showToast()
  }
}

async function toggleStatus(todo) {
  try {
    const res = await fetch(`${API_URL}/todos/${todo._id}`, {
      method: "PATCH",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !todo.done })
    })

    if (!res.ok) {
      throw new Error(`Status update failed: ${res.status}`)
    }

    toastMessage.value = "The ledger is updated. 🪶📜"
    showToast()
    await loadTodos()
  } catch(error) {
    console.log(error)
    toastMessage.value = "The runes refuse to shift. Could not update task status. 🔮🔒"
    showToast()
  }
}

function showToast() {
  isToastVisible.value = true
  setTimeout(() => {isToastVisible.value = false}, 5000)
}

async function loadTodos () {
  const res = await fetch(`${API_URL}/todos`)
  todos.value = await res.json()
}

function openForm() {
  const form = document.getElementById("auth-form")
  form.classList.add("visible");title
}

// Form functions
function switchMode(nextMode) {
  formMode.value = nextMode
  formMessage.value = ''
}

function submitLogin() {
  formMessage.value = `Login submitted for "${loginName.value}" — backend can be connected here.`
}

function submitRegister() {
  if (registerPassword.value !== registerPasswordRepeat.value) {
    formMessage.value = 'Passwords do not match.'
    return
  }

  formMessage.value = `Registration submitted for "${registerName.value}" — backend can be connected here.`
}

onMounted(loadTodos)
</script>

<template>
  <div class="app">

    <div class="wood-frame">
      <div class="parchment">

        <!-- HEADER SCENE -->
        <header class="header-scene">
          <!-- <div class="lantern">🏮</div> -->
          <button @click="openForm()" class="potion" style="top:8px;right:12px">🧪</button>
        </header>


        <!-- MAIN LAYOUT -->
        <main class="main-layout">
          <div class="quests-col">

            <!-- Add form -->
            <div class="add-form">
              <span class="quest-bullet-add">◈</span>
              <input class="add-input" @keyup.enter="addTask" v-model.trim="newTitle" placeholder="Write a new task..." maxlength="80">
              <select v-model="newTaskComplexity" name="complexity" id="complexity">
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </select>
              <button class="add-btn" @click="addTask">ADD</button>
            </div>

            <ul class="quest-list">
              <li v-for="todo in todos" :key="todo._id">
                <div class="quest-item">
                  <div class="check-shield" :title="todo.done ? 'Cancel' : 'Make'">
                    <div v-html="todo.done ? shieldDone : shieldEmpty" @click="toggleStatus(todo)"></div>
                  </div>
                  <span class="quest-label" :class="todo.done ? 'done' : ''">{{ todo.title }}</span>
                  <span class="quest-crystal">💎 {{ todo.crystals }}</span>
                  <button class="del-btn" @click="deleteTask(todo._id)" title="Delete">X</button>
                </div>
              </li>
            </ul>
          </div>

          <!-- SIDEBAR -->
          <div class="sidebar">
            <div class="side-panel">
              <div class="side-panel-title">МОЙ ПРОГРЕСС</div>
              <div class="progress-nums" id="progressNums">0 <span>/ 0</span></div>
              <div class="prog-bar-outer">
                <div class="prog-bar-inner" id="progressBar" style="width:0%"></div>
              </div>
              <div class="dragon-display">
                <span class="dragon-emoji" id="dragonEmoji">🥚</span>
                <span class="dragon-caption" id="dragonCaption">Выполняй квесты,<br>чтобы вылупить дракона!</span>
              </div>

              <div class="side-panel-title">МАГИЧЕСКИЕ КРИСТАЛЛЫ</div>
              <div class="crystal-big">
                <span class="crystal-icon-big">💎</span>
                <span class="crystal-count" id="crystalCount">0</span>
              </div>
            </div>

            <div class="side-panel">
              <div class="side-panel-title">НАГРАДЫ</div>
              <div class="reward-row">
                <span class="reward-icon">🍰</span>
                <span class="reward-name">Сладкий Ролл</span>
                <button class="reward-buy" id="btn-roll" onclick="buyReward('Сладкий Ролл 🍰',3)" disabled>💎 3</button>
              </div>
              <div class="reward-row">
                <span class="reward-icon">⚔️</span>
                <span class="reward-name">Лезвие Уверенности</span>
                <button class="reward-buy" id="btn-blade" onclick="buyReward('Лезвие Уверенности ⚔️',5)" disabled>💎 5</button>
              </div>
              <div class="reward-row">
                <span class="reward-icon">🐉</span>
                <span class="reward-name">Купить Дракона!</span>
                <button class="reward-buy" id="btn-dragon" onclick="buyReward('Дракон твой! 🐉',20)" disabled>💎 20</button>
              </div>
            </div>
          </div>
        </main>

        <!-- BOTTOM SCENE -->
        <footer class="bottom-scene">
          <!-- <div class="mouse-warrior">🐭</div> -->
          <div class="mouse-warrior">
            <img src="./assets/img/maus.png" class="maus" width="250" alt="">
          </div>
          <!-- <div class="bottom-center">
            <div class="collect-text">Собирай магические кристаллы для ценнейших наград!</div>
            <div class="reward-strip">
              <div class="reward-strip-item">🐉 Купить Дракона! <span class="reward-strip-cost">💎 20</span></div>
              <div class="reward-strip-item">🍰 Сладкий Ролл <span class="reward-strip-cost">💎 3</span></div>
              <div class="reward-strip-item">⚔️ Лезвие Уверенности <span class="reward-strip-cost">💎 +5</span></div>
            </div>
          </div> -->
          <div class="bottom-right">
            <img src="./assets/img/drachen.png" class="drachen" width="150" alt="">
          </div>
        </footer>
      </div>
    </div>

    <div class="toast" :class="{ show: isToastVisible}">{{ toastMessage }}</div>


    <div class="form-wrap">
      <div class="background-overlay"></div>

      <section class="auth-card" aria-label="Authentication">
        <div class="top-rune">◇</div>

        <header class="brand">
          <h2>Chronicles of Maus</h2>
          <div class="quest-ribbon">
            <span>❧</span>
            <strong>Epic Task Quest</strong>
            <span>❧</span>
          </div>
          <p>{{ formTitle }}</p>
        </header>

        <div class="tabs" role="tablist" aria-label="Authentication mode">
          <button type="button" class="tab" :class="{ active: formMode === 'login' }" @click="switchMode('login')">
            Log In
          </button>
          <button type="button" class="tab" :class="{ active: formMode === 'register' }" @click="switchMode('register')">
            Register
          </button>
        </div>

        <form v-if="formMode === 'login'" class="auth-form" @submit.prevent="submitLogin">
          <label class="field">
            <span class="field-icon">♟</span>
            <input v-model="loginName" type="text" placeholder="Email or Username" autocomplete="username" required />
          </label>

          <label class="field">
            <span class="field-icon">♜</span>
            <input v-model="loginPassword" type="password" placeholder="Password" autocomplete="current-password" required />
          </label>

          <button class="primary-button" type="submit">Log In</button>
          <button class="text-button" type="button">Forgot Password?</button>
        </form>

        <form v-else class="auth-form" @submit.prevent="submitRegister">
          <label class="field">
            <span class="field-icon">♟</span>
            <input v-model="registerName" type="text" placeholder="Username" autocomplete="username" required />
          </label>

          <label class="field">
            <span class="field-icon">✉</span>
            <input v-model="registerEmail" type="text" placeholder="Email" autocomplete="email" required />
          </label>

          <label class="field">
            <span class="field-icon">♜</span>
            <input v-model="registerPassword" type="password" placeholder="Password" autocomplete="new-password" required />
          </label>

          <label class="field">
            <span class="field-icon">♜</span>
            <input v-model="registerPasswordRepeat" type="password" placeholder="Repeat password" autocomplete="new-password" required />
          </label>

          <button class="primary-button" type="submit">Create Account</button>
        </form>

        <p v-if="formMessage" class="message">{{ formMessage }}</p>
        <div class="bottom-rune">◇</div>
      </section>
    </div>
  </div>
</template>

<style scoped>

</style>