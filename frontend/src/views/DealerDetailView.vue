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
      <p>Diler ma'lumotlari yuklanmoqda...</p>
    </div>

    <div v-else-if="loadError" class="state-msg state-msg--error">
      <div class="state-icon state-icon--error"><i class="ri-error-warning-line"></i></div>
      <p>{{ loadError }}</p>
      <button class="btn btn-ghost" @click="goBack">Ortga qaytish</button>
    </div>

    <template v-else-if="dealer">
      <section class="dealer-hero">
        <div class="dealer-hero-inner">
          <div class="dealer-avatar-lg">{{ initials(dealer.company_name) }}</div>
          <div class="dealer-hero-info">
            <div class="name-row">
              <h1>{{ dealer.company_name || "Nomsiz firma" }}</h1>
              <span class="trust-badge">
                <i class="ri-shield-check-fill"></i> Ishonchli diler
              </span>
            </div>
            <p class="phone"><i class="ri-phone-fill"></i> {{ dealer.phone_number }}</p>
            <p class="member-since"><i class="ri-history-line"></i> {{ memberSince(dealer.date_joined) }}</p>
            <span class="products-badge"><i class="ri-box-3-fill"></i> {{ dealer.products_count }} ta mahsulot</span>
          </div>
        </div>
      </section>

      <section class="products-section">
        <div class="section-head">
          <h2 class="section-title">{{ dealer.company_name || "Diler" }} mahsulotlari</h2>
          <p class="section-sub">Ushbu diler taklif qilayotgan barcha mahsulotlar</p>
        </div>

        <div v-if="loadingProducts" class="state-msg state-msg--inline">
          <i class="ri-loader-4-line spin"></i> Mahsulotlar yuklanmoqda...
        </div>
        <div v-else-if="products.length === 0" class="state-msg state-msg--inline">
          <i class="ri-inbox-line"></i> Bu dilerda hozircha mahsulot yo'q.
        </div>

        <div v-else class="product-grid">
          <div v-for="product in products" :key="product.id" class="product-card" @click="goToProductDetail(product.id)">
            <div class="product-image">
              <img v-if="product.image" :src="getImageUrl(product.image)" :alt="product.name" />
              <div v-else class="placeholder"><i class="ri-image-2-line"></i></div>
              <span class="stock-badge" :class="{ low: product.stock <= 5 }">
                {{ product.stock > 0 ? `${product.stock} dona` : "Tugagan" }}
              </span>
            </div>
            <div class="product-body">
              <h4>{{ product.name }}</h4>
              <span class="about-link"><i class="ri-information-line"></i> Batafsil</span>
              <div class="price-row">
                <span class="price">{{ formatPrice(product.price) }} so'm</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../api';

export default {
  name: 'DealerDetailView',
  props: {
    id: { type: [String, Number], required: false }
  },
  setup(props) {
    const route = useRoute();
    const router = useRouter();
    const backendUrl = 'https://surprising-enchantment-production-5152.up.railway.app';

    const dealer = ref(null);
    const products = ref([]);
    const loading = ref(true);
    const loadingProducts = ref(false);
    const loadError = ref('');

    const dealerId = computed(() => props.id || route.params.id);

    const fetchDealer = async () => {
      loading.value = true;
      loadError.value = '';
      try {
        // 🟢 /public/dealers/<id>/ — hammaga ochiq (AllowAny) endpoint
        const response = await api.get(`/public/dealers/${dealerId.value}/`);
        dealer.value = response.data;
      } catch (error) {
        loadError.value = "Diler ma'lumotini yuklab bo'lmadi. U mavjud emas yoki o'chirilgan.";
      } finally {
        loading.value = false;
      }
    };

    const fetchDealerProducts = async () => {
      loadingProducts.value = true;
      try {
        const response = await api.get('/catalog/', { params: { dealer: dealerId.value } });
        products.value = response.data.results || response.data;
      } catch (error) {
        products.value = [];
      } finally {
        loadingProducts.value = false;
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

    const initials = (name) => {
      if (!name) return '?';
      return name.trim().charAt(0).toUpperCase();
    };

    // 🟢 Diler "qachon beri ishlayapti" (necha oy/yil faoliyatda)
    const memberSince = (dateStr) => {
      if (!dateStr) return "Faoliyatda";
      const joined = new Date(dateStr);
      const now = new Date();
      let months = (now.getFullYear() - joined.getFullYear()) * 12 + (now.getMonth() - joined.getMonth());
      if (months < 1) return "Yangi qo'shildi";
      if (months < 12) return `${months} oydan beri faoliyatda`;
      const years = Math.floor(months / 12);
      return `${years} yildan beri faoliyatda`;
    };

    const isAuthenticated = computed(() => !!localStorage.getItem('token'));
    const userRole = computed(() =>
      localStorage.getItem('role') ? localStorage.getItem('role').toUpperCase() : null
    );

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

    const goToProductDetail = (productId) => {
      router.push(`/product/${productId}`);
    };

    onMounted(() => {
      fetchDealer();
      fetchDealerProducts();
    });

    return {
      dealer, products, loading, loadingProducts, loadError,
      getImageUrl, formatPrice, initials, memberSince, goBack, goToProductDetail
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
  max-width: 1180px;
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
.brand__word { color: #eafbf2; font-weight: 700; font-size: 16px; }
.brand__word em { font-style: normal; color: #6ee7a8; }

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
.btn-outline:hover { background: rgba(255, 255, 255, 0.14); }
.btn-ghost { background: #eef4f0; color: var(--forest-900); }
.btn-ghost:hover { background: #e2ede6; }

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
.state-msg--inline {
  flex-direction: row;
  justify-content: center;
  padding: 40px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid var(--line);
  gap: 8px;
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
.state-icon--error { background: #fef2f2; color: #dc2626; }
.state-msg--error p { color: #b91c1c; font-weight: 500; }
.spin { animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* ---------- Dealer hero ---------- */
.dealer-hero {
  background:
    radial-gradient(circle at 90% 0%, rgba(34, 197, 94, 0.06), transparent 45%),
    #fff;
  border-bottom: 1px solid var(--line);
}
.dealer-hero-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 38px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.dealer-avatar-lg {
  width: 88px;
  height: 88px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  color: #06170e;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 800;
  font-family: 'Manrope', sans-serif;
  flex-shrink: 0;
  box-shadow: 0 10px 24px rgba(5, 150, 105, 0.22);
}
.dealer-hero-info { flex: 1; min-width: 220px; }
.name-row { display: flex; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 10px; }
.name-row h1 {
  font-family: 'Manrope', sans-serif;
  font-size: 26px;
  color: var(--ink-900);
  margin: 0;
  font-weight: 800;
}
.trust-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 700;
  color: #0369a1;
  background: #e0f2fe;
  padding: 4px 10px;
  border-radius: 20px;
}
.trust-badge i { color: #0284c7; }
.phone { font-size: 14px; color: var(--ink-600); display: flex; align-items: center; gap: 6px; margin: 0 0 6px; }
.member-since { font-size: 13px; color: var(--accent-600); font-weight: 600; display: flex; align-items: center; gap: 6px; margin: 0 0 12px; }
.products-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  font-weight: 700;
  color: var(--forest-700);
  background: rgba(34, 197, 94, 0.1);
  padding: 5px 12px;
  border-radius: 20px;
}

/* ---------- Products ---------- */
.products-section { max-width: 1180px; margin: 0 auto; padding: 36px 24px 60px; }
.section-head { margin-bottom: 22px; }
.section-title {
  font-family: 'Manrope', sans-serif;
  font-size: 21px;
  color: var(--forest-900);
  font-weight: 800;
  margin: 0 0 4px;
}
.section-sub { color: var(--ink-600); font-size: 13.5px; }

.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 18px; }
.product-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  border: 1px solid var(--line);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.product-card:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(10, 47, 29, 0.1); }
.product-image {
  position: relative;
  height: 160px;
  background: linear-gradient(155deg, #eef4f0 0%, #e4efe8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.product-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.product-card:hover .product-image img { transform: scale(1.06); }
.placeholder { width: 60px; height: 60px; border-radius: 50%; background: rgba(255, 255, 255, 0.7); display: flex; align-items: center; justify-content: center; }
.placeholder i { font-size: 28px; color: #b7c6bd; }
.stock-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.95);
  color: #15803d;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 9px;
  border-radius: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}
.stock-badge.low { color: #b91c1c; }
.product-body { padding: 14px 16px 16px; }
.product-body h4 { font-size: 14.5px; font-weight: 700; color: var(--ink-900); margin: 0 0 8px; line-height: 1.3; }
.about-link { font-size: 11.5px; color: var(--accent-600); font-weight: 600; display: inline-flex; align-items: center; gap: 4px; margin-bottom: 8px; }
.price-row { display: flex; align-items: center; }
.price { font-family: 'Manrope', sans-serif; font-weight: 800; color: var(--forest-900); font-size: 14.5px; }

@media (max-width: 640px) {
  .dealer-hero-inner { flex-direction: column; align-items: flex-start; }
  .name-row h1 { font-size: 22px; }
}
</style>