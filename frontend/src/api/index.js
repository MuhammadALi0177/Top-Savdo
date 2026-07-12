import axios from 'axios';

const api = axios.create({
  baseURL: 'https://surprising-enchantment-production-5152.up.railway.app/api/v1',
  headers: {
    // 'Content-Type': 'application/json',
  }
});

// So'rov yuborilishidan oldin har safar tokenni eng yangi holatini olish
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      // 'Bearer ' o'rniga 'Token ' deb yozamiz (bu juda muhim!)
      config.headers.Authorization = `Token ${token}`; 
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;