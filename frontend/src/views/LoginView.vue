<template>
  <div class="auth-shell">
    <!-- Brend paneli -->
    <aside class="brand-pane">
      <div class="brand-pane__glow"></div>

      <div class="brand-mark">
        <span class="brand-mark__box">TS</span>
        <span class="brand-mark__word">Top-Savdo <em>B2B</em></span>
      </div>

      <div class="brand-copy">
        <h1>Ulgurji savdo — <br />bir tizimda birlashdi</h1>
        <p>Do'kon, diler va kuryerlar bitta platformada uchrashadi. Buyurtma berishdan yetkazishgacha — hammasi nazoratda.</p>
      </div>

      <svg class="network" viewBox="0 0 420 260" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <line x1="210" y1="130" x2="90" y2="55" class="network__line" />
        <line x1="210" y1="130" x2="330" y2="55" class="network__line" />
        <line x1="210" y1="130" x2="90" y2="205" class="network__line" />
        <line x1="210" y1="130" x2="330" y2="205" class="network__line" />
        <line x1="210" y1="130" x2="90" y2="55" class="network__line network__line--flow" />
        <line x1="210" y1="130" x2="330" y2="205" class="network__line network__line--flow network__line--flow-delay" />

        <g class="network__node network__node--hub">
          <circle cx="210" cy="130" r="26" />
          <text x="210" y="135" text-anchor="middle">TS</text>
        </g>
        <g class="network__node">
          <circle cx="90" cy="55" r="19" />
          <text x="90" y="60" text-anchor="middle" class="network__icon"></text>
        </g>
        <g class="network__node">
          <circle cx="330" cy="55" r="19" />
          <text x="330" y="60" text-anchor="middle" class="network__icon"></text>
        </g>
        <g class="network__node">
          <circle cx="90" cy="205" r="19" />
          <text x="90" y="210" text-anchor="middle" class="network__icon"></text>
        </g>
        <g class="network__node">
          <circle cx="330" cy="205" r="19" />
          <text x="330" y="210" text-anchor="middle" class="network__icon"></text>
        </g>

        <text x="90" y="30" text-anchor="middle" class="network__label">Diler</text>
        <text x="330" y="30" text-anchor="middle" class="network__label">Mijoz</text>
        <text x="90" y="240" text-anchor="middle" class="network__label">Kuryer</text>
        <text x="330" y="240" text-anchor="middle" class="network__label">Admin</text>
      </svg>

      <ul class="brand-features">
        <li><i class="ri-flashlight-line"></i> Tezkor buyurtma qabul qilish</li>
        <li><i class="ri-shield-check-line"></i> Har bir rol uchun xavfsiz kirish</li>
        <li><i class="ri-truck-line"></i> Yetkazib berishni real vaqtda kuzatish</li>
      </ul>
    </aside>

    <!-- Forma paneli -->
    <main class="form-pane">
      <div class="form-wrap">
        <div class="mobile-brand">
          <span class="brand-mark__box">TS</span>
          <span>Top-Savdo B2B</span>
        </div>

        <div class="form-head">
          <span class="eyebrow">Xush kelibsiz</span>
          <h2>Tizimga kirish</h2>
          <p>Davom etish uchun telefon raqamingiz va parolingizni kiriting</p>
        </div>

        <form @submit.prevent="handleLogin" novalidate>
          <div class="input-group">
            <label for="phone">Telefon raqam</label>
            <div class="input-shell">
              <i class="ri-smartphone-line"></i>
              <input
                id="phone"
                v-model="phone"
                type="text"
                placeholder="90-123-45-67"
                autocomplete="tel"
                required
              />
            </div>
          </div>

          <div class="input-group">
            <label for="password">Parol</label>
            <div class="input-shell">
              <i class="ri-lock-2-line"></i>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="******"
                autocomplete="current-password"
                required
              />
              <button
                type="button"
                class="peek-btn"
                @click="showPassword = !showPassword"
                :aria-label="showPassword ? 'Parolni yashirish' : 'Parolni ko\'rsatish'"
              >
                <i :class="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"></i>
              </button>
            </div>
          </div>

          <transition name="fade">
            <div v-if="errorMessage" class="error-msg">
              <i class="ri-error-warning-line"></i>{{ errorMessage }}
            </div>
          </transition>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Kirish <i class="ri-arrow-right-line"></i></span>
            <span v-else class="loading-dots">Kirilmoqda<i></i><i></i><i></i></span>
          </button>
        </form>

        <div class="auth-links">
          Akkountingiz yo'qmi? <router-link to="/signup">Yangi akkaunt ochish</router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

export default {
  setup() {
    const phone = ref('');
    const password = ref('');
    const loading = ref(false);
    const errorMessage = ref('');
    const showPassword = ref(false);
    const router = useRouter();

    const handleLogin = async () => {
      loading.value = true;
      errorMessage.value = '';

      try {
        // Django backendga login ma'lumotlarini yuboramiz
        const response = await api.post('/login/', {
          phone_number: phone.value,
          password: password.value
        });

        // 1. Backenddan kelgan maxfiy Tokenni saqlaymiz
        localStorage.setItem('token', response.data.token);

        // 2. Rolni olib, katta harflarga o'tkazib saqlaymiz ( Chalkashmaslik uchun )
        const userRole = response.data.role ? response.data.role.toUpperCase() : 'CLIENT';
        localStorage.setItem('role', userRole);

        // 3. Foydalanuvchi ID sini saqlaymiz
        localStorage.setItem('user_id', response.data.user_id);

        // --- TO'G'IRLANGAN ENG MUHIM QISMI ---
        // Roliga qarab foydalanuvchini o'z sahifasiga yo'naltiramiz:
       if (userRole === 'ADMIN') {
          router.push('/admin/users'); // Admin o'zining paneliga o'tadi 🎉
        } else if (userRole === 'DEALER') {
          router.push('/dealer');
        } else if (userRole === 'COURIER') {
          router.push('/courier'); // Kuryer o'z paneliga o'tadi
        } else {
          router.push('/orders'); // Magazinchi o'z joyiga o'tadi
        }

      } catch (error) {
        if (error.response && error.response.data) {
          errorMessage.value = "Telefon raqam yoki parol xato!";
        } else {
          errorMessage.value = "Server bilan aloqa uzildi. Qayta urinib ko'ring.";
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      phone,
      password,
      loading,
      errorMessage,
      showPassword,
      handleLogin
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

.auth-shell {
  --forest-950: #071b10;
  --forest-900: #0a2f1d;
  --forest-700: #145c38;
  --forest-500: #1f6e43;
  --accent-500: #22c55e;
  --accent-600: #16a34a;
  --paper: #f7f9f7;
  --ink-900: #0f2419;
  --ink-600: #536b60;
  --line: #e3e8e4;

  min-height: 100vh;
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 1fr);
  background: var(--paper);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---------- Brend paneli ---------- */
.brand-pane {
  position: relative;
  overflow: hidden;
  padding: 56px 56px 44px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background:
    radial-gradient(circle at 15% 15%, rgba(34, 197, 94, 0.16), transparent 45%),
    linear-gradient(160deg, var(--forest-950) 0%, var(--forest-900) 48%, var(--forest-700) 100%);
  color: #eafbf2;
}

.brand-pane__glow {
  position: absolute;
  inset: -20% -10% auto auto;
  width: 420px;
  height: 420px;
  background: radial-gradient(circle, rgba(34, 197, 94, 0.28), transparent 70%);
  filter: blur(10px);
  pointer-events: none;
}

.brand-mark {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Manrope', sans-serif;
  position: relative;
  z-index: 1;
}

.brand-mark__box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 11px;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  color: #06170e;
  font-weight: 800;
  font-size: 15px;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
}

.brand-mark__word {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.2px;
}

.brand-mark__word em {
  font-style: normal;
  color: #6ee7a8;
}

.brand-copy {
  margin-top: 40px;
  position: relative;
  z-index: 1;
}

.brand-copy h1 {
  font-family: 'Manrope', sans-serif;
  font-size: clamp(28px, 3vw, 36px);
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.3px;
  margin-bottom: 16px;
}

.brand-copy p {
  font-size: 15px;
  line-height: 1.65;
  color: #bcd9c8;
  max-width: 400px;
}

.network {
  width: 100%;
  max-width: 380px;
  margin: 26px auto;
  position: relative;
  z-index: 1;
}

.network__line {
  stroke: rgba(110, 231, 168, 0.28);
  stroke-width: 1.5;
}

.network__line--flow {
  stroke: #6ee7a8;
  stroke-width: 2;
  stroke-dasharray: 6 10;
  animation: dash-flow 3.2s linear infinite;
}

.network__line--flow-delay {
  animation-delay: 1.4s;
}

@keyframes dash-flow {
  to { stroke-dashoffset: -160; }
}

.network__node circle {
  fill: rgba(255, 255, 255, 0.06);
  stroke: rgba(110, 231, 168, 0.55);
  stroke-width: 1.4;
}

.network__node--hub circle {
  fill: var(--accent-500);
  stroke: none;
}

.network__node--hub text {
  fill: #06170e;
  font-family: 'Manrope', sans-serif;
  font-weight: 800;
  font-size: 12px;
}

.network__label {
  fill: #bcd9c8;
  font-size: 11px;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

.brand-features {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 14px;
  position: relative;
  z-index: 1;
}

.brand-features li {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  color: #d5ecdf;
}

.brand-features i {
  color: #6ee7a8;
  font-size: 16px;
}

/* ---------- Forma paneli ---------- */
.form-pane {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
}

.form-wrap {
  width: 100%;
  max-width: 380px;
}

.mobile-brand {
  display: none;
  align-items: center;
  gap: 10px;
  font-family: 'Manrope', sans-serif;
  font-weight: 700;
  color: var(--forest-900);
  margin-bottom: 28px;
}

.form-head {
  margin-bottom: 30px;
}

.eyebrow {
  display: inline-block;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--accent-600);
  margin-bottom: 8px;
}

.form-head h2 {
  font-family: 'Manrope', sans-serif;
  font-size: 26px;
  font-weight: 800;
  color: var(--ink-900);
  margin-bottom: 8px;
}

.form-head p {
  font-size: 14px;
  color: var(--ink-600);
  line-height: 1.5;
}

.input-group {
  margin-bottom: 18px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 7px;
  font-weight: 600;
  color: var(--forest-900);
  font-size: 13px;
}

.input-shell {
  display: flex;
  align-items: center;
  gap: 10px;
  border: 1.5px solid var(--line);
  border-radius: 10px;
  background: #fff;
  padding: 0 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.input-shell i {
  color: #9db3a8;
  font-size: 17px;
}

.input-shell input {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 0;
  font-size: 14.5px;
  font-family: inherit;
  color: var(--ink-900);
  background: transparent;
}

.input-shell:focus-within {
  border-color: var(--accent-500);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.14);
}

.peek-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #9db3a8;
  padding: 4px;
  display: flex;
  font-size: 16px;
}

.peek-btn:hover {
  color: var(--forest-700);
}

.submit-btn {
  width: 100%;
  padding: 13px;
  margin-top: 6px;
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  font-family: 'Manrope', sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s ease;
  box-shadow: 0 8px 20px rgba(5, 150, 105, 0.28);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(5, 150, 105, 0.36);
}

.submit-btn:disabled {
  background: #cbd5c9;
  color: #6b7d74;
  box-shadow: none;
  cursor: not-allowed;
}

.loading-dots {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.loading-dots i {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: #06170e;
  display: inline-block;
  animation: bounce 1s infinite ease-in-out;
}

.loading-dots i:nth-child(2) { animation-delay: 0.15s; }
.loading-dots i:nth-child(3) { animation-delay: 0.3s; }

@keyframes bounce {
  0%, 80%, 100% { opacity: 0.3; transform: translateY(0); }
  40% { opacity: 1; transform: translateY(-3px); }
}

.error-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  padding: 11px 14px;
  border-radius: 9px;
  margin-bottom: 16px;
  font-size: 13.5px;
  font-weight: 500;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.auth-links {
  margin-top: 26px;
  font-size: 13.5px;
  color: var(--ink-600);
  text-align: center;
}

.auth-links a {
  color: var(--accent-600);
  text-decoration: none;
  font-weight: 700;
}

.auth-links a:hover {
  text-decoration: underline;
}

/* ---------- Responsive ---------- */
@media (max-width: 900px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }
  .brand-pane {
    display: none;
  }
  .mobile-brand {
    display: flex;
  }
  .form-pane {
    padding: 32px 20px;
  }
}
</style>