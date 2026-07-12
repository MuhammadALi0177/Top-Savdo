<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Top-Savdo B2B</h2>
      <p>Tizimga kirish uchun telefon raqamingiz va parolingizni kiriting</p>
      
      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <label>Telefon raqam:</label>
          <input 
            v-model="phone" 
            type="text" 
            placeholder="90-123-45-67" 
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

        <button type="submit" :disabled="loading">
          {{ loading ? 'Kirilmoqda...' : 'Kirish' }}
        </button>
      </form>

      <div class="auth-links">
        Akkountingiz yo'qmi? <router-link to="/signup">Yangi akkaunt ochish</router-link>
      </div>

      <div v-if="errorMessage" class="error-msg">
        {{ errorMessage }}
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
    const loading = ref(false);
    const errorMessage = ref('');
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
      handleLogin
    };
  }
};
</script>

<style scoped>
/* Orqa fonga chuqur va boy to'q yashil gradient beramiz */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #0a2f1d 0%, #114e32 50%, #1f6e43 100%);
  padding: 20px;
}

/* Oq rangli asosiy login bloki (Oyna) */
.login-box {
  background: rgba(255, 255, 255, 0.96);
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 420px;
  text-align: center;
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease;
}

.login-box:hover {
  transform: translateY(-5px);
}

/* Sarlavha dizayni (Yashil ranglar ohangida) */
h2 {
  color: #0a2f1d;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
  letter-spacing: 1px;
}

/* Kichik tushuntirish matni */
p {
  color: #556b60;
  font-size: 14px;
  margin-bottom: 30px;
  line-height: 1.5;
}

/* Input bloki */
.input-group {
  margin-bottom: 22px;
  text-align: left;
}

.input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #114e32;
  font-size: 14px;
}

.input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  outline: none;
  background-color: #f8faf9;
}

/* Inputga bosilgandagi chiroyli yashil nur effekti */
.input-group input:focus {
  border-color: #10b981;
  background-color: #fff;
  box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.15);
}

/* Professional yashil gradientli tugma */
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
  transition: all 0.3s ease;
  box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3);
}

button:hover {
  background: linear-gradient(to right, #059669, #10b981);
  box-shadow: 0 6px 22px rgba(5, 150, 105, 0.4);
  transform: scale(1.01);
}

button:disabled {
  background: #cbd5e1;
  box-shadow: none;
  cursor: not-allowed;
}

/* Xatolik chiqqandagi ogohlantirish dizayni */
.error-msg {
  color: #dc2626;
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  padding: 12px;
  border-radius: 8px;
  margin-top: 20px;
  font-size: 14px;
  font-weight: 500;
}
.auth-links {
  margin-top: 25px;
  font-size: 14px;
  color: #556b60; /* Matn rangi to'q yashilroq ohangda */
}

.auth-links a {
  color: #10b981; /* Chiroyli och yashil rang */
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.auth-links a:hover {
  color: #059669; /* Sichqoncha borganda bir oz to'qlashadi */
  text-decoration: underline; /* Tagiga chiziladi */
}
</style>