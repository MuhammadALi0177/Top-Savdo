<template>
  <div class="detail-page">
    <header class="navbar">
      <div class="navbar-inner">
        <div class="brand" @click="goBack" style="cursor: pointer">
          <i class="ri-shopping-bag-3-line"></i>
          <span>Top-Savdo <b>B2B</b></span>
        </div>
        <button class="btn btn-outline back-btn" @click="goBack">
          <i class="ri-arrow-left-line"></i> Orqaga
        </button>
      </div>
    </header>

    <div v-if="loading" class="state-msg">
      <i class="ri-loader-4-line spin"></i> Mahsulot yuklanmoqda...
    </div>

    <div v-else-if="loadError" class="state-msg error">
      <i class="ri-error-warning-line"></i> {{ loadError }}
    </div>

    <section v-else-if="product" class="detail-wrap">
      <div class="detail-card">
        <div class="detail-image">
          <img v-if="product.image" :src="getImageUrl(product.image)" :alt="product.name" />
          <i v-else class="ri-image-2-line placeholder-icon"></i>
          <span class="stock-badge" :class="{ low: product.stock <= 5 }">
            {{ product.stock > 0 ? `${product.stock} dona mavjud` : "Tugagan" }}
          </span>
        </div>

        <div class="detail-info">
          <p class="category" v-if="product.category_name || product.brand_name">
            {{ product.category_name }}
            <template v-if="product.brand_name"> · {{ product.brand_name }}</template>
          </p>

          <h1 class="product-name">{{ product.name }}</h1>

          <p v-if="product.dealer_company_name" class="dealer-tag">
            <i class="ri-store-2-line"></i> {{ product.dealer_company_name }}
          </p>

          <!-- 🟢 Nomi tagida "Haqida / Batafsil" bo'limi, undan keyin narxi -->
          <div class="about-block">
            <h3 class="about-title"><i class="ri-file-text-line"></i> Mahsulot haqida (Batafsil)</h3>
            <p v-if="product.description" class="about-text">{{ product.description }}</p>
            <p v-else class="about-text about-empty">Bu mahsulot uchun diler hali batafsil ma'lumot kiritmagan.</p>
          </div>

          <div class="price-block">
            <span class="price-label">Narxi</span>
            <span class="price-value">{{ formatPrice(product.price) }} so'm</span>
          </div>

          <div class="detail-actions">
            <button class="btn btn-primary buy-btn" @click="handleAction">
              <i class="ri-shopping-cart-2-line"></i> {{ actionLabel }}
            </button>
            <button class="btn btn-ghost" @click="goBack">Ortga qaytish</button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

export default {
  name: 'ProductDetailView',
  props: {
    id: { type: [String, Number], required: false }
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const backendUrl = 'http://127.0.0.1:8000';

    const product = ref(null);
    const loading = ref(true);
    const loadError = ref('');

    const productId = computed(() => props.id || route.params.id);
    const isAuthenticated = computed(() => !!localStorage.getItem('token'));
    const userRole = computed(() =>
      localStorage.getItem('role') ? localStorage.getItem('role').toUpperCase() : null
    );

    const actionLabel = computed(() => {
      if (isAuthenticated.value && userRole.value === 'CLIENT') return "Savatga qo'shish uchun buyurtmalarga o'tish";
      if (isAuthenticated.value) return 'Orqaga qaytish';
      return "Sotib olish uchun kirish";
    });

    const fetchProduct = async () => {
      loading.value = true;
      loadError.value = '';
      try {
        // 🟢 /catalog/<id>/ — hammaga ochiq (AllowAny) endpoint, shuning uchun
        // ham mehmon, ham tizimga kirgan foydalanuvchi shu orqali mahsulotni ko'ra oladi.
        const response = await api.get(`/catalog/${productId.value}/`);
        product.value = response.data;
      } catch (error) {
        loadError.value = "Mahsulotni yuklab bo'lmadi. U mavjud emas yoki o'chirilgan.";
      } finally {
        loading.value = false;
      }
    };

    const getImageUrl = (imagePath) => {
      if (!imagePath) return '';
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) return imagePath;
      return `${backendUrl}${imagePath.startsWith('/') ? '' : '/'}${imagePath}`;
    };

    const formatPrice = (value) => {
      const num = Number(value) || 0;
      return num.toLocaleString('ru-RU');
    };

    const goBack = () => {
      if (isAuthenticated.value) {
        if (userRole.value === 'CLIENT') router.push('/orders');
        else if (userRole.value === 'DEALER') router.push('/dealer');
        else if (userRole.value === 'ADMIN') router.push('/admin/users');
        else if (userRole.value === 'COURIER') router.push('/courier');
        else router.push('/');
      } else {
        router.push('/');
      }
    };

    const handleAction = () => {
      if (isAuthenticated.value && userRole.value === 'CLIENT') {
        router.push('/orders');
      } else if (isAuthenticated.value) {
        goBack();
      } else {
        router.push('/login');
      }
    };

    onMounted(fetchProduct);

    return {
      product, loading, loadError, actionLabel,
      getImageUrl, formatPrice, goBack, handleAction
    };
  }
};
</script>

<style scoped>
.detail-page { min-height: 100vh; background: #f5f7fb; }

.navbar {
  background: linear-gradient(135deg, #0a2f1d 0%, #114e32 50%, #1f6e43 100%);
  position: sticky; top: 0; z-index: 10;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
.navbar-inner {
  max-width: 1180px; margin: 0 auto; padding: 16px 24px;
  display: flex; justify-content: space-between; align-items: center;
}
.brand { display: flex; align-items: center; gap: 8px; color: #fff; font-weight: 700; font-size: 18px; }
.brand i { font-size: 22px; color: #34d399; }

.btn { border: none; cursor: pointer; border-radius: 10px; font-weight: 600; padding: 10px 18px; display: inline-flex; align-items: center; gap: 6px; font-size: 14px; transition: all .2s; }
.btn-outline { background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.4); }
.btn-outline:hover { background: rgba(255,255,255,0.12); }
.btn-primary { background: linear-gradient(to right, #10b981, #059669); color: #fff; box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3); }
.btn-primary:hover { box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4); }
.btn-ghost { background: #eef4f0; color: #0a2f1d; }
.btn-ghost:hover { background: #e2ede6; }

.state-msg { text-align: center; padding: 80px 20px; color: #6b8578; font-size: 15px; }
.state-msg.error { color: #dc2626; }
.spin { animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

.detail-wrap { max-width: 980px; margin: 0 auto; padding: 32px 20px 60px; }
.detail-card {
  background: #fff; border-radius: 20px; overflow: hidden;
  box-shadow: 0 10px 30px rgba(10, 47, 29, 0.08);
  display: grid; grid-template-columns: 1fr 1fr;
}
.detail-image {
  position: relative; background: #f4f8f6; min-height: 320px;
  display: flex; align-items: center; justify-content: center;
}
.detail-image img { width: 100%; height: 100%; object-fit: cover; }
.placeholder-icon { font-size: 64px; color: #cbd5e1; }
.stock-badge {
  position: absolute; top: 14px; right: 14px; background: rgba(255,255,255,0.95);
  color: #15803d; font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 20px;
}
.stock-badge.low { color: #b45309; }

.detail-info { padding: 32px 30px; display: flex; flex-direction: column; }
.category { font-size: 12px; color: #6b8578; text-transform: uppercase; letter-spacing: .4px; margin: 0 0 8px; }
.product-name { font-size: 26px; color: #0a2f1d; margin: 0 0 8px; line-height: 1.25; }
.dealer-tag { font-size: 13px; color: #10b981; display: flex; align-items: center; gap: 6px; margin: 0 0 18px; }

/* 🟢 "Haqida / Batafsil" bo'limi — nomi tagida, narxidan yuqorida */
.about-block {
  background: #f4f8f6; border-radius: 14px; padding: 16px 18px; margin-bottom: 20px;
}
.about-title { font-size: 14px; color: #0a2f1d; margin: 0 0 8px; display: flex; align-items: center; gap: 6px; }
.about-text { font-size: 14px; color: #35503f; line-height: 1.6; margin: 0; white-space: pre-line; }
.about-empty { color: #94a3b8; font-style: italic; }

.price-block { display: flex; flex-direction: column; gap: 2px; margin-bottom: 24px; }
.price-label { font-size: 12px; color: #6b8578; }
.price-value { font-size: 28px; font-weight: 800; color: #059669; }

.detail-actions { display: flex; gap: 10px; flex-wrap: wrap; margin-top: auto; }
.buy-btn { flex: 1; justify-content: center; min-width: 220px; }

@media (max-width: 720px) {
  .detail-card { grid-template-columns: 1fr; }
  .detail-image { min-height: 240px; }
}
</style>