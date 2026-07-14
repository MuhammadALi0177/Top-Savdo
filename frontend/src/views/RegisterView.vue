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
        <h1>Biznesingiz uchun<br />yagona hamkor</h1>
        <p>Magazinchimisiz, dilermisiz yoki kuryer — Top-Savdo har bir rolga moslashgan o'zining ish maydonini beradi.</p>
      </div>

      <ul class="role-preview">
        <li>
          <span class="role-preview__icon"><i class="ri-store-2-line"></i></span>
          <div>
            <strong>Magazinchi</strong>
            <span>Buyurtma bering, yetkazib berishni kuzating</span>
          </div>
        </li>
        <li>
          <span class="role-preview__icon"><i class="ri-building-2-line"></i></span>
          <div>
            <strong>Diler</strong>
            <span>Mahsulotlaringizni B2B tarmoqqa chiqaring</span>
          </div>
        </li>
        <li>
          <span class="role-preview__icon"><i class="ri-truck-line"></i></span>
          <div>
            <strong>Kuryer</strong>
            <span>Marshrutlarni oling, yetkazib bering</span>
          </div>
        </li>
      </ul>

      <div class="brand-quote">
        <i class="ri-double-quotes-l"></i>
        Bir ro'yxatdan o'tish — butun savdo zanjiriga kirish.
      </div>
    </aside>

    <!-- Forma paneli -->
    <main class="form-pane">
      <div class="form-wrap">
        <div class="mobile-brand">
          <span class="brand-mark__box">TS</span>
          <span>Top-Savdo B2B</span>
        </div>

        <div class="form-head">
          <span class="eyebrow">Yangi akkaunt</span>
          <h2>Ro'yxatdan o'tish</h2>
          <p>Tizimda yangi profil yaratish uchun ma'lumotlarni to'ldiring</p>
        </div>

        <form @submit.prevent="handleRegister" novalidate>
          <div class="input-group">
            <label>Tizimdagi rolingiz</label>
            <div class="role-picker">
              <label
                v-for="opt in roleOptions"
                :key="opt.value"
                class="role-card"
                :class="{ 'role-card--active': role === opt.value }"
              >
                <input type="radio" v-model="role" :value="opt.value" name="role" />
                <i :class="opt.icon"></i>
                <span>{{ opt.label }}</span>
              </label>
            </div>
          </div>

          <div class="input-group">
            <label for="phone">Telefon raqam</label>
            <div class="input-shell">
              <i class="ri-smartphone-line"></i>
              <input
                id="phone"
                v-model="phone"
                type="text"
                placeholder="+998901234567"
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
                autocomplete="new-password"
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
            <div v-if="role === 'DEALER'" class="input-group dynamic-field">
              <label>Firma / Korxona nomi</label>
              <div class="input-shell">
                <i class="ri-building-line"></i>
                <input
                  v-model="companyName"
                  type="text"
                  placeholder="Masalan: Ideal Savdo MCHJ"
                  required
                />
              </div>
            </div>
          </transition>

          <transition name="fade">
            <div v-if="role === 'CLIENT'" class="dynamic-fields">
              <div class="input-group dynamic-field">
                <label>Do'kon nomi</label>
                <div class="input-shell">
                  <i class="ri-store-2-line"></i>
                  <input
                    v-model="storeName"
                    type="text"
                    placeholder="Masalan: Fayz Market"
                    required
                  />
                </div>
              </div>
              <div class="input-group dynamic-field">
                <label>Yetkazib berish manzili</label>
                <div class="input-shell input-shell--textarea">
                  <i class="ri-map-pin-line"></i>
                  <textarea
                    v-model="address"
                    placeholder="Viloyat, tuman, ko'cha va uy raqami"
                    required
                  ></textarea>
                </div>
              </div>
            </div>
          </transition>

          <transition name="fade">
            <div v-if="role === 'COURIER'" class="input-group dynamic-field">
              <label>Transport turi</label>
              <div class="transport-picker">
                <label
                  v-for="t in transportOptions"
                  :key="t.value"
                  class="transport-chip"
                  :class="{ 'transport-chip--active': transportType === t.value }"
                >
                  <input type="radio" v-model="transportType" :value="t.value" name="transport" />
                  <i :class="t.icon"></i>
                  <span>{{ t.label }}</span>
                </label>
              </div>
            </div>
          </transition>

          <transition name="fade">
            <div v-if="errorMessage" class="error-msg">
              <i class="ri-error-warning-line"></i>{{ errorMessage }}
            </div>
          </transition>
          <transition name="fade">
            <div v-if="successMessage" class="success-msg">
              <i class="ri-checkbox-circle-line"></i>{{ successMessage }}
            </div>
          </transition>

          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">Ro'yxatdan o'tish <i class="ri-arrow-right-line"></i></span>
            <span v-else class="loading-dots">Yuborilmoqda<i></i><i></i><i></i></span>
          </button>
        </form>

        <div class="auth-links">
          Akkountingiz bormi? <router-link to="/login">Kirish</router-link>
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
    const role = ref('CLIENT'); // Default holatda magazinchi bo'lib turadi
    const companyName = ref('');
    const storeName = ref('');
    const address = ref('');
    const transportType = ref('CAR');

    const loading = ref(false);
    const errorMessage = ref('');
    const successMessage = ref('');
    const showPassword = ref(false);
    const router = useRouter();

    const roleOptions = [
      { value: 'CLIENT', label: 'Magazinchi', icon: 'ri-store-2-line' },
      { value: 'DEALER', label: 'Diler', icon: 'ri-building-2-line' },
      { value: 'COURIER', label: 'Kuryer', icon: 'ri-truck-line' }
    ];

    const transportOptions = [
      { value: 'CAR', label: 'Mashina', icon: 'ri-car-line' },
      { value: 'MOTO', label: 'Skuter', icon: 'ri-motorbike-line' },
      { value: 'BIKE', label: 'Velosiped', icon: 'ri-bike-line' },
      { value: 'FOOT', label: 'Piyoda', icon: 'ri-walk-line' }
    ];

    const handleRegister = async () => {
      loading.value = true;
      errorMessage.value = '';
      successMessage.value = '';

      // Backend kutayotgan ma'lumotlar paketi
      const payload = {
        phone_number: phone.value,
        password: password.value,
        role: role.value,
      };

      // Rolga qarab qo'shimcha parametrlarni qo'shamiz
      if (role.value === 'DEALER') {
        payload.company_name = companyName.value;
      } else if (role.value === 'CLIENT') {
        payload.store_name = storeName.value;
        payload.address = address.value;
      } else if (role.value === 'COURIER') {
        payload.transport_type = transportType.value;
      }

      try {
        const response = await api.post('/signup/', payload);

        successMessage.value = response.data.message;

        // Ro'yxatdan o'tgach tokenni saqlab, to'g'ri tizimga kirgizamiz
        localStorage.setItem('token', response.data.token);
        localStorage.setItem('role', response.data.role);

        setTimeout(() => {
          if (response.data.role === 'DEALER') {
            router.push('/dealer');
          } else if (response.data.role === 'COURIER') {
            router.push('/courier');
          } else {
            router.push('/orders');
          }
        }, 1500);

      } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
          errorMessage.value = error.response.data.error;
        } else {
          errorMessage.value = "Ro'yxatdan o'tishda xatolik yuz berdi. Qayta urinib ko'ring.";
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      phone,
      password,
      role,
      roleOptions,
      transportOptions,
      companyName,
      storeName,
      address,
      transportType,
      loading,
      errorMessage,
      successMessage,
      showPassword,
      handleRegister
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
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.08fr);
  background: var(--paper);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---------- Brend paneli ---------- */
.brand-pane {
  position: relative;
  overflow: hidden;
  padding: 56px 52px 44px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background:
    radial-gradient(circle at 85% 10%, rgba(34, 197, 94, 0.18), transparent 45%),
    linear-gradient(160deg, var(--forest-950) 0%, var(--forest-900) 48%, var(--forest-700) 100%);
  color: #eafbf2;
}

.brand-pane__glow {
  position: absolute;
  inset: auto -10% -25% auto;
  width: 380px;
  height: 380px;
  background: radial-gradient(circle, rgba(34, 197, 94, 0.24), transparent 70%);
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
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
}

.brand-mark__word {
  font-size: 17px;
  font-weight: 700;
}

.brand-mark__word em {
  font-style: normal;
  color: #6ee7a8;
}

.brand-copy {
  margin-top: 36px;
  position: relative;
  z-index: 1;
}

.brand-copy h1 {
  font-family: 'Manrope', sans-serif;
  font-size: clamp(26px, 2.8vw, 34px);
  line-height: 1.22;
  font-weight: 800;
  letter-spacing: -0.3px;
  margin-bottom: 14px;
}

.brand-copy p {
  font-size: 14.5px;
  line-height: 1.65;
  color: #bcd9c8;
  max-width: 380px;
}

.role-preview {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 30px 0;
  position: relative;
  z-index: 1;
}

.role-preview li {
  display: flex;
  align-items: center;
  gap: 14px;
}

.role-preview__icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(110, 231, 168, 0.12);
  border: 1px solid rgba(110, 231, 168, 0.28);
  color: #6ee7a8;
  font-size: 18px;
}

.role-preview strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #eafbf2;
  margin-bottom: 2px;
}

.role-preview span {
  font-size: 12.5px;
  color: #a9c9ba;
}

.brand-quote {
  position: relative;
  z-index: 1;
  font-size: 13.5px;
  color: #d5ecdf;
  border-top: 1px solid rgba(255, 255, 255, 0.12);
  padding-top: 20px;
  line-height: 1.5;
  font-style: italic;
}

.brand-quote i {
  color: #6ee7a8;
  margin-right: 6px;
  font-style: normal;
}

/* ---------- Forma paneli ---------- */
.form-pane {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 32px;
  overflow-y: auto;
}

.form-wrap {
  width: 100%;
  max-width: 420px;
  padding: 12px 0;
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
  margin-bottom: 26px;
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
  font-size: 25px;
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
  margin-bottom: 16px;
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

.input-shell input,
.input-shell textarea {
  flex: 1;
  border: none;
  outline: none;
  padding: 12px 0;
  font-size: 14.5px;
  font-family: inherit;
  color: var(--ink-900);
  background: transparent;
  resize: none;
}

.input-shell--textarea {
  align-items: flex-start;
}
.input-shell--textarea i {
  margin-top: 12px;
}
.input-shell--textarea textarea {
  min-height: 64px;
  padding-top: 12px;
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

/* Rol tanlash kartalari */
.role-picker {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.role-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 6px;
  border: 1.5px solid var(--line);
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  transition: all 0.2s ease;
  background: #fff;
}

.role-card input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.role-card i {
  font-size: 20px;
  color: #9db3a8;
  transition: color 0.2s ease;
}

.role-card span {
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-600);
}

.role-card--active {
  border-color: var(--accent-500);
  background: rgba(34, 197, 94, 0.07);
  box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.1);
}

.role-card--active i,
.role-card--active span {
  color: var(--forest-700);
}

/* Transport chiplari */
.transport-picker {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.transport-chip {
  position: relative;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 9px 14px;
  border: 1.5px solid var(--line);
  border-radius: 999px;
  cursor: pointer;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--ink-600);
  background: #fff;
  transition: all 0.2s ease;
}

.transport-chip input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.transport-chip i {
  font-size: 15px;
  color: #9db3a8;
}

.transport-chip--active {
  border-color: var(--accent-500);
  background: rgba(34, 197, 94, 0.08);
  color: var(--forest-700);
}

.transport-chip--active i {
  color: var(--forest-700);
}

.dynamic-field,
.dynamic-fields {
  animation: fadeIn 0.3s ease;
}

.submit-btn {
  width: 100%;
  padding: 13px;
  margin-top: 8px;
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

.error-msg,
.success-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 11px 14px;
  border-radius: 9px;
  margin-bottom: 16px;
  font-size: 13.5px;
  font-weight: 500;
}

.error-msg {
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
}

.success-msg {
  color: #15803d;
  background-color: #ecfdf5;
  border: 1px solid #bbf0d3;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.auth-links {
  margin-top: 22px;
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

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
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

@media (max-width: 420px) {
  .role-picker {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }
  .role-card {
    padding: 10px 4px;
  }
  .role-card span {
    font-size: 10.5px;
  }
}
</style>