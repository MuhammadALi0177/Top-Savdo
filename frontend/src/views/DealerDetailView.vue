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
      <i class="ri-loader-4-line spin"></i> Diler ma'lumotlari yuklanmoqda...
    </div>

    <div v-else-if="loadError" class="state-msg error">
      <i class="ri-error-warning-line"></i> {{ loadError }}
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
        <h2 class="section-title">{{ dealer.company_name || "Diler" }} mahsulotlari</h2>

        <div v-if="loadingProducts" class="state-msg"><i class="ri-loader-4-line spin"></i> Mahsulotlar yuklanmoqda...</div>
        <div v-else-if="products.length === 0" class="state-msg">Bu dilerda hozircha mahsulot yo'q.</div>

        <div v-else class="product-grid">
          <div v-for="product in products" :key="product.id" class="product-card" @click="goToProductDetail(product.id)">
            <div class="product-image">
              <img v-if="product.image" :src="getImageUrl(product.image)" :alt="product.name" />
              <i v-else class="ri-image-2-line placeholder-icon"></i>
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

.state-msg { text-align: center; padding: 80px 20px; color: #6b8578; font-size: 15px; }
.state-msg.error { color: #dc2626; }
.spin { animation: spin 1s linear infinite; display: inline-block; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

/* Dealer hero */
.dealer-hero { background: #fff; border-bottom: 1px solid #e5ede8; }
.dealer-hero-inner {
  max-width: 1180px; margin: 0 auto; padding: 34px 24px;
  display: flex; align-items: center; gap: 22px; flex-wrap: wrap;
}
.dealer-avatar-lg {
  width: 84px; height: 84px; border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff; display: flex; align-items: center; justify-content: center;
  font-size: 32px; font-weight: 700; flex-shrink: 0;
}
.dealer-hero-info { flex: 1; min-width: 220px; }
.name-row { display: flex; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 8px; }
.name-row h1 { font-size: 24px; color: #0a2f1d; margin: 0; }
.trust-badge {
  display: inline-flex; align-items: center; gap: 4px;
  font-size: 12px; font-weight: 700; color: #0369a1;
  background: #e0f2fe; padding: 4px 10px; border-radius: 20px;
}
.trust-badge i { color: #0284c7; }
.phone { font-size: 14px; color: #6b7280; display: flex; align-items: center; gap: 6px; margin: 0 0 6px; }
.member-since { font-size: 13px; color: #059669; font-weight: 600; display: flex; align-items: center; gap: 6px; margin: 0 0 10px; }
.products-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 12.5px; font-weight: 700; color: #15803d;
  background: #f0fdf4; padding: 5px 12px; border-radius: 20px;
}

/* Products */
.products-section { max-width: 1180px; margin: 0 auto; padding: 30px 24px 60px; }
.section-title { font-size: 20px; color: #0a2f1d; margin: 0 0 18px; }
.product-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(210px, 1fr)); gap: 18px;
}
.product-card {
  background: #fff; border-radius: 14px; overflow: hidden; cursor: pointer;
  box-shadow: 0 4px 14px rgba(10, 47, 29, 0.06);
  transition: transform .15s, box-shadow .15s;
}
.product-card:hover { transform: translateY(-3px); box-shadow: 0 8px 22px rgba(10, 47, 29, 0.12); }
.product-image { position: relative; height: 150px; background: #f4f8f6; display: flex; align-items: center; justify-content: center; }
.product-image img { width: 100%; height: 100%; object-fit: cover; }
.placeholder-icon { font-size: 40px; color: #cbd5e1; }
.stock-badge {
  position: absolute; top: 10px; right: 10px; background: rgba(255,255,255,0.95);
  color: #15803d; font-size: 11px; font-weight: 700; padding: 4px 9px; border-radius: 20px;
}
.stock-badge.low { color: #b45309; }
.product-body { padding: 14px 16px; }
.product-body h4 { font-size: 14.5px; color: #0a2f1d; margin: 0 0 8px; line-height: 1.3; }
.about-link { font-size: 11.5px; color: #059669; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; margin-bottom: 8px; }
.price-row { display: flex; align-items: center; }
.price { font-weight: 800; color: #059669; font-size: 14.5px; }

@media (max-width: 640px) {
  .dealer-hero-inner { flex-direction: column; align-items: flex-start; }
}
</style>