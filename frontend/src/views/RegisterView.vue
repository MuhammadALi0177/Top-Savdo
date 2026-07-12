<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Top-Savdo B2B</h2>
      <p>Tizimda yangi profil yaratish uchun ma'lumotlarni kiriting</p>
      
      <form @submit.prevent="handleRegister">
        <div class="input-group">
          <label>Telefon raqam:</label>
          <input 
            v-model="phone" 
            type="text" 
            placeholder="+998901234567" 
            required 
          />
        </div>

        <div class="input-group">
          <label>Parol:</label>
          <input 
            v-model="password" 
            type="password" 
            placeholder="******" 
            required 
          />
        </div>

        <div class="input-group">
          <label>Tizimdagi rolingiz:</label>
          <select v-model="role" required>
            <option value="CLIENT">Magazinchi (Mijoz / Client)</option>
            <option value="DEALER">Diler (Sotuvchi/Yetkazib beruvchi)</option>
            <option value="COURIER">Kuryer (Yetkazib beruvchi)</option>
          </select>
        </div>

        <div v-if="role === 'DEALER'" class="input-group dynamic-field">
          <label>Firma / Korxona nomi:</label>
          <input 
            v-model="companyName" 
            type="text" 
            placeholder="Masalan: Ideal Savdo MCHJ" 
            required 
          />
        </div>

        <div v-if="role === 'CLIENT'" class="dynamic-fields">
          <div class="input-group dynamic-field">
            <label>Do'kon nomi:</label>
            <input 
              v-model="storeName" 
              type="text" 
              placeholder="Masalan: Fayz Market" 
              required 
            />
          </div>
          <div class="input-group dynamic-field">
            <label>Yetkazib berish manzili:</label>
            <textarea 
              v-model="address" 
              placeholder="Viloyat, tuman, ko'cha va uy raqami" 
              required
            ></textarea>
          </div>
        </div>

        <div v-if="role === 'COURIER'" class="input-group dynamic-field">
          <label>Transport turi:</label>
          <select v-model="transportType" required>
            <option value="CAR">Mashina</option>
            <option value="MOTO">Motoroller / Skuter</option>
            <option value="BIKE">Velosiped</option>
            <option value="FOOT">Piyoda</option>
          </select>
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Ro\'yxatdan o\'tilmoqda...' : 'Ro\'yxatdan o\'tish' }}
        </button>
      </form>

      <div class="auth-links">
        Akkountingiz bormi? <router-link to="/login">Kirish</router-link>
      </div>

      <div v-if="errorMessage" class="error-msg">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="success-msg">
        {{ successMessage }}
      </div>
    </div>
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
    const router = useRouter();

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
      companyName,
      storeName,
      address,
      loading,
      errorMessage,
      successMessage,
      handleRegister
    };
  }
};
</script>

<style scoped>
/* LoginView bilan bir xil chiroyli to'q yashil dizayn */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0a2f1d 0%, #114e32 50%, #1f6e43 100%);
  padding: 40px 20px;
}

.register-box {
  background: rgba(255, 255, 255, 0.96);
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 450px;
  text-align: center;
  backdrop-filter: blur(10px);
}

h2 {
  color: #0a2f1d;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
}

p {
  color: #556b60;
  font-size: 14px;
  margin-bottom: 25px;
  line-height: 1.5;
}

.input-group {
  margin-bottom: 18px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 600;
  color: #114e32;
  font-size: 14px;
}

.input-group input, .input-group select, .input-group textarea {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
  background-color: #f8faf9;
  font-family: inherit;
}

.input-group input:focus, .input-group select:focus, .input-group textarea:focus {
  border-color: #10b981;
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
}

.dynamic-field {
  animation: fadeIn 0.4s ease;
}

button {
  width: 100%;
  padding: 14px;
  background: linear-gradient(to right, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
}

button:hover {
  background: linear-gradient(to right, #059669, #10b981);
}

.auth-links {
  margin-top: 20px;
  font-size: 14px;
  color: #64748b;
}

.auth-links a {
  color: #10b981;
  text-decoration: none;
  font-weight: 600;
}

.error-msg {
  color: #dc2626;
  background-color: #fef2f2;
  padding: 12px;
  border-radius: 8px;
  margin-top: 15px;
  font-size: 14px;
}

.success-msg {
  color: #059669;
  background-color: #ecfdf5;
  padding: 12px;
  border-radius: 8px;
  margin-top: 15px;
  font-size: 14px;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>