<template>
  <div class="detail-page">
    <header class="navbar">
      <div class="navbar-inner">
        <div class="brand" @click="goBack">
          <span class="brand__box">TS</span>
          <span class="brand__word">Top-Savdo <em>B2B</em></span>
        </div>
        <button class="btn btn-outline back-btn" @click="goBack">
          <i class="ri-arrow-left-line"></i> Orqaga
        </button>
      </div>
    </header>

    <div v-if="loading" class="state-msg">
      <div class="state-icon"><i class="ri-loader-4-line spin"></i></div>
      <p>Mahsulot yuklanmoqda...</p>
    </div>

    <div v-else-if="loadError" class="state-msg state-msg--error">
      <div class="state-icon state-icon--error"><i class="ri-error-warning-line"></i></div>
      <p>{{ loadError }}</p>
      <button class="btn btn-ghost" @click="goBack">Ortga qaytish</button>
    </div>

    <section v-else-if="product" class="detail-wrap">
      <nav class="crumbs" v-if="product.category_name || product.brand_name">
        <span>Katalog</span>
        <i class="ri-arrow-right-s-line"></i>
        <span v-if="product.category_name">{{ product.category_name }}</span>
        <template v-if="product.brand_name">
          <i class="ri-arrow-right-s-line"></i>
          <span>{{ product.brand_name }}</span>
        </template>
      </nav>

      <div class="detail-card">
        <div class="detail-image">
          <img v-if="product.image" :src="getImageUrl(product.image)" :alt="product.name" />
          <div v-else class="placeholder">
            <i class="ri-image-2-line"></i>
          </div>
          <span class="stock-badge" :class="{ 'stock-badge--low': product.stock <= 5, 'stock-badge--out': product.stock <= 0 }">
            <i class="ri-checkbox-blank-circle-fill"></i>
            {{ product.stock > 0 ? `${product.stock} dona mavjud` : "Tugagan" }}
          </span>
        </div>

        <div class="detail-info">
          <div class="detail-info__top">
            <p class="category" v-if="product.category_name || product.brand_name">
              {{ product.category_name }}
              <template v-if="product.brand_name"> · {{ product.brand_name }}</template>
            </p>

            <h1 class="product-name">{{ product.name }}</h1>

            <p v-if="product.dealer_company_name" class="dealer-tag">
              <i class="ri-store-2-line"></i> {{ product.dealer_company_name }}
            </p>

            <div class="about-block">
              <h3 class="about-title"><i class="ri-file-text-line"></i> Mahsulot haqida</h3>
              <p v-if="product.description" class="about-text">{{ product.description }}</p>
              <p v-else class="about-text about-empty">Bu mahsulot uchun diler hali batafsil ma'lumot kiritmagan.</p>
            </div>
          </div>

          <div class="detail-info__bottom">
            <div class="price-block">
              <span class="price-label">Narxi</span>
              <span class="price-value">{{ formatPrice(product.price) }} <em>so'm</em></span>
            </div>

            <div class="detail-actions">
              <button class="btn btn-primary buy-btn" @click="handleAction">
                <i class="ri-shopping-cart-2-line"></i> {{ actionLabel }}
              </button>
              <button class="btn btn-ghost" @click="goBack">Ortga qaytish</button>
            </div>
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
    const backendUrl = 'https://surprising-enchantment-production-5152.up.railway.app';

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
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

.detail-page {
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
  background: var(--paper);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---------- Navbar ---------- */
.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  background: linear-gradient(160deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  box-shadow: 0 4px 18px rgba(7, 27, 16, 0.2);
}
.navbar-inner {
  max-width: 1080px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-family: 'Manrope', sans-serif;
}
.brand__box {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  color: #06170e;
  font-weight: 800;
  font-size: 13px;
  box-shadow: 0 5px 14px rgba(16, 185, 129, 0.32);
}
.brand__word {
  color: #eafbf2;
  font-weight: 700;
  font-size: 16px;
}
.brand__word em {
  font-style: normal;
  color: #6ee7a8;
}

.btn {
  border: none;
  cursor: pointer;
  border-radius: 10px;
  font-weight: 600;
  padding: 10px 18px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.2s ease;
}
.btn-outline {
  background: rgba(255, 255, 255, 0.06);
  color: #eafbf2;
  border: 1px solid rgba(255, 255, 255, 0.22);
}
.btn-outline:hover {
  background: rgba(255, 255, 255, 0.14);
}
.btn-primary {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  box-shadow: 0 8px 20px rgba(5, 150, 105, 0.28);
}
.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 26px rgba(5, 150, 105, 0.36);
}
.btn-ghost {
  background: #eef4f0;
  color: var(--forest-900);
}
.btn-ghost:hover {
  background: #e2ede6;
}

/* ---------- Holat xabarlari ---------- */
.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  text-align: center;
  padding: 110px 20px;
  color: var(--ink-600);
  font-size: 15px;
}
.state-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(34, 197, 94, 0.1);
  color: var(--forest-700);
  font-size: 26px;
}
.state-icon--error {
  background: #fef2f2;
  color: #dc2626;
}
.state-msg--error p {
  color: #b91c1c;
  font-weight: 500;
}
.spin {
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* ---------- Breadcrumb ---------- */
.detail-wrap {
  max-width: 1000px;
  margin: 0 auto;
  padding: 28px 20px 60px;
}
.crumbs {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12.5px;
  color: var(--ink-600);
  margin-bottom: 16px;
  text-transform: capitalize;
}
.crumbs i {
  font-size: 15px;
  color: #b7c6bd;
}

/* ---------- Karta ---------- */
.detail-card {
  background: #fff;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(10, 47, 29, 0.09);
  display: grid;
  grid-template-columns: 1fr 1fr;
  border: 1px solid var(--line);
}

.detail-image {
  position: relative;
  background: linear-gradient(155deg, #eef4f0 0%, #e4efe8 100%);
  min-height: 380px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.detail-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}
.detail-image:hover img {
  transform: scale(1.05);
}
.placeholder {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}
.placeholder i {
  font-size: 40px;
  color: #b7c6bd;
}

.stock-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.96);
  color: #15803d;
  font-size: 12px;
  font-weight: 700;
  padding: 7px 13px;
  border-radius: 999px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
.stock-badge i {
  font-size: 8px;
  color: #22c55e;
}
.stock-badge--low {
  color: #b45309;
}
.stock-badge--low i {
  color: #f59e0b;
}
.stock-badge--out {
  color: #b91c1c;
}
.stock-badge--out i {
  color: #ef4444;
}

.detail-info {
  padding: 34px 34px 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 26px;
}

.category {
  font-size: 12px;
  font-weight: 700;
  color: var(--accent-600);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin: 0 0 10px;
}

.product-name {
  font-family: 'Manrope', sans-serif;
  font-size: 27px;
  font-weight: 800;
  color: var(--ink-900);
  margin: 0 0 10px;
  line-height: 1.25;
}

.dealer-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--forest-700);
  background: rgba(34, 197, 94, 0.08);
  padding: 5px 12px;
  border-radius: 999px;
  margin: 0 0 20px;
}

.about-block {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 18px 20px;
}
.about-title {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--forest-900);
  margin: 0 0 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.about-title i {
  color: var(--accent-600);
}
.about-text {
  font-size: 14px;
  color: #3c5348;
  line-height: 1.65;
  margin: 0;
  white-space: pre-line;
}
.about-empty {
  color: #9aab9f;
  font-style: italic;
}

.detail-info__bottom {
  border-top: 1px solid var(--line);
  padding-top: 22px;
}

.price-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin-bottom: 20px;
}
.price-label {
  font-size: 12px;
  color: var(--ink-600);
}
.price-value {
  font-family: 'Manrope', sans-serif;
  font-size: 30px;
  font-weight: 800;
  color: var(--forest-900);
}
.price-value em {
  font-style: normal;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink-600);
  margin-left: 4px;
}

.detail-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.buy-btn {
  flex: 1;
  justify-content: center;
  min-width: 240px;
}

@media (max-width: 720px) {
  .detail-card {
    grid-template-columns: 1fr;
  }
  .detail-image {
    min-height: 260px;
  }
  .detail-info {
    padding: 26px 22px;
  }
  .product-name {
    font-size: 23px;
  }
}
</style>