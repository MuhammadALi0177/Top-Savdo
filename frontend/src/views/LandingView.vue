<template>
  <div class="landing">
    <!-- ==================== TOP NAVBAR ==================== -->
    <header class="navbar">
      <div class="navbar-inner">
        <div class="brand">
          <i class="ri-building-2-fill"></i>
          <span>Top-Savdo <b>B2B</b></span>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="btn btn-ghost">Kirish</router-link>
          <router-link to="/signup" class="btn btn-primary">Ro'yxatdan o'tish</router-link>
        </div>
      </div>
    </header>

    <!-- ==================== HERO ==================== -->
    <section class="hero">
      <div class="hero-inner">
        <div class="hero-text">
          <span class="hero-tag"><i class="ri-shield-check-fill"></i> Ulgurji savdo platformasi</span>
          <h1>Ishonchli dilerlar bilan <span>ulgurji savdo</span> endi bir joyda</h1>
          <p>
            Ro'yxatdan o'tmasdan turib ham dilerlarimiz va ularning butun mahsulotlar
            katalogi bilan tanishing. Buyurtma berish uchun tizimga kirishingiz kifoya.
          </p>
          <div class="hero-actions">
            <router-link to="/signup" class="btn btn-primary lg">
              Bepul boshlash <i class="ri-arrow-right-line"></i>
            </router-link>
            <a href="#dealers-section" class="btn btn-outline lg">Dilerlarni ko'rish</a>
          </div>

          <div class="stats-row">
            <div class="stat">
              <strong>{{ dealers.length }}+</strong>
              <span>faol diler</span>
            </div>
            <div class="stat">
              <strong>{{ totalProductsCount }}+</strong>
              <span>mahsulot</span>
            </div>
            <div class="stat">
              <strong>24/7</strong>
              <span>buyurtma qabul</span>
            </div>
          </div>
        </div>

        <!-- Sof CSS/SVG bilan yasalgan B2B ombor-yetkazib berish illyustratsiyasi -->
        <div class="hero-art">
          <svg viewBox="0 0 420 360" xmlns="http://www.w3.org/2000/svg" class="hero-svg">
            <defs>
              <linearGradient id="boxGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#34d399"/>
                <stop offset="100%" stop-color="#059669"/>
              </linearGradient>
              <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#e6f4ec"/>
                <stop offset="100%" stop-color="#cfe9da"/>
              </linearGradient>
            </defs>

            <ellipse cx="210" cy="330" rx="180" ry="20" fill="url(#floorGrad)"/>

            <!-- Fon qutilar shtabeli -->
            <g opacity="0.55">
              <rect x="30" y="220" width="60" height="60" rx="6" fill="#a7f3d0"/>
              <rect x="95" y="240" width="55" height="40" rx="6" fill="#6ee7b7"/>
              <rect x="300" y="230" width="65" height="55" rx="6" fill="#a7f3d0"/>
            </g>

            <!-- Katta qadoq quti (markaz) -->
            <g>
              <rect x="140" y="150" width="130" height="110" rx="10" fill="url(#boxGrad)"/>
              <rect x="140" y="150" width="130" height="30" rx="10" fill="#047857" opacity="0.4"/>
              <path d="M140 195 L270 195" stroke="#065f46" stroke-width="4"/>
              <path d="M205 150 L205 260" stroke="#065f46" stroke-width="4"/>
            </g>

            <!-- Yetkazib berish yuk mashinasi -->
            <g transform="translate(20,255)">
              <rect x="0" y="0" width="90" height="45" rx="6" fill="#114e32"/>
              <rect x="90" y="14" width="42" height="31" rx="4" fill="#1f6e43"/>
              <rect x="98" y="20" width="16" height="14" rx="2" fill="#d1fae5"/>
              <circle cx="24" cy="52" r="11" fill="#0a2f1d"/>
              <circle cx="24" cy="52" r="4" fill="#d1fae5"/>
              <circle cx="105" cy="52" r="11" fill="#0a2f1d"/>
              <circle cx="105" cy="52" r="4" fill="#d1fae5"/>
            </g>

            <!-- O'sish grafigi kartochkasi -->
            <g transform="translate(275,60)">
              <rect x="0" y="0" width="110" height="80" rx="12" fill="#ffffff" stroke="#d1fae5" stroke-width="2"/>
              <polyline points="12,55 35,40 55,50 78,22 98,15" fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="98" cy="15" r="5" fill="#10b981"/>
              <text x="12" y="70" font-size="11" fill="#059669" font-weight="700">Savdo o'sishi</text>
            </g>

            <!-- Cheklovchi doira -->
            <circle cx="60" cy="90" r="26" fill="#ffffff" stroke="#a7f3d0" stroke-width="2"/>
            <path d="M48 90 l8 8 16 -16" fill="none" stroke="#059669" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
      </div>
    </section>

    <!-- ==================== DEALERS LIST ==================== -->
    <section id="dealers-section" class="section">
      <div class="section-head">
        <div>
          <h2 class="section-title">Bizning dilerlar</h2>
          <p class="section-sub">Diler ustiga bosing — uning ma'lumoti va mahsulotlarini ko'rasiz</p>
        </div>
        <button v-if="selectedDealer" class="btn btn-outline sm" @click="showAllProducts">
          <i class="ri-apps-2-line"></i> Barcha mahsulotlarni ko'rish
        </button>
      </div>

      <div v-if="loadingDealers" class="state-msg"><i class="ri-loader-4-line spin"></i> Dilerlar yuklanmoqda...</div>
      <div v-else-if="dealersError" class="state-msg error">{{ dealersError }}</div>
      <div v-else-if="dealers.length === 0" class="state-msg">Hozircha dilerlar mavjud emas.</div>

      <div v-else class="dealer-grid">
        <div
          v-for="dealer in dealers"
          :key="dealer.id"
          class="dealer-card"
          :class="{ active: selectedDealer && selectedDealer.id === dealer.id }"
          @click="goToDealerDetail(dealer.id)"
        >
          <div class="dealer-avatar">{{ initials(dealer.company_name) }}</div>
          <div class="dealer-info">
            <div class="dealer-name-row">
              <h3>{{ dealer.company_name || "Nomsiz firma" }}</h3>
              <span class="trust-badge" title="Tizimda faol va tekshirilgan diler">
                <i class="ri-shield-check-fill"></i> Ishonchli diler
              </span>
            </div>
            <p><i class="ri-phone-fill"></i> {{ dealer.phone_number }}</p>
            <p class="member-since"><i class="ri-history-line"></i> {{ memberSince(dealer.date_joined) }}</p>
            <span class="badge"><i class="ri-box-3-fill"></i> {{ dealer.products_count }} ta mahsulot</span>
          </div>
          <i class="ri-arrow-right-s-line arrow"></i>
        </div>
      </div>
    </section>

    <!-- ==================== PRODUCTS (har doim pastda ko'rinadi) ==================== -->
    <section id="products-section" class="section products-section">
      <div class="section-head">
        <div>
          <h2 class="section-title">
            <template v-if="selectedDealer">{{ selectedDealer.company_name || "Diler" }} mahsulotlari</template>
            <template v-else>Barcha mahsulotlar</template>
          </h2>
          <p class="section-sub">
            <template v-if="selectedDealer">Faqat shu diler taklif qilayotgan mahsulotlar</template>
            <template v-else>Barcha dilerlarning to'liq katalogi</template>
          </p>
        </div>
        <button v-if="selectedDealer" class="btn btn-outline sm" @click="showAllProducts">
          <i class="ri-close-line"></i> Filtrni tozalash
        </button>
      </div>

      <div v-if="loadingProducts" class="state-msg"><i class="ri-loader-4-line spin"></i> Mahsulotlar yuklanmoqda...</div>
      <div v-else-if="productsError" class="state-msg error">{{ productsError }}</div>
      <div v-else-if="products.length === 0" class="state-msg">Hozircha mahsulot topilmadi.</div>

      <div v-else class="product-grid">
        <div v-for="product in products" :key="product.id" class="product-card">
          <div class="product-image" @click="goToProductDetail(product.id)" style="cursor: pointer">
            <img v-if="product.image" :src="getImageUrl(product.image)" :alt="product.name" />
            <i v-else class="ri-image-2-line placeholder-icon"></i>
            <span class="stock-badge" :class="{ low: product.stock <= 5 }">
              {{ product.stock > 0 ? `${product.stock} dona` : "Tugagan" }}
            </span>
          </div>
          <div class="product-body">
            <p class="category">{{ product.category_name }}<template v-if="product.brand_name"> · {{ product.brand_name }}</template></p>
            <h4 @click="goToProductDetail(product.id)" style="cursor: pointer">{{ product.name }}</h4>
            <button class="about-link" @click="goToProductDetail(product.id)">
              <i class="ri-information-line"></i> Haqida / Batafsil
            </button>
            <p v-if="product.dealer_company_name" class="dealer-tag">
              <i class="ri-store-2-line"></i> {{ product.dealer_company_name }}
            </p>
            <div class="price-row">
              <span class="price">{{ formatPrice(product.price) }} so'm</span>
              <button class="buy-btn" @click="goToLogin">Sotib olish</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>

  <footer class="footer">
  <div class="footer-container">
    <div class="footer-column">
      <h3>Biz haqimizda</h3>
      <a href="#">Topshirish punktlari</a>
      <a href="#">Vakansiyalar</a>
    </div>
    <div class="footer-column">
      <h3>Foydalanuvchilarga</h3>
      <a href="#">Biz bilan bog'lanish</a>
      <a href="#">Savol-Javob</a>
    </div>
    <div class="footer-column">
      <h3>Tadbirkorlarga</h3>
      <a href="#">Bizda soting</a>
      <a href="#">Sotuvchi kabinetiga kirish</a>
      <a href="#">Topshirish punktini ochish</a>
    </div>
    <div class="footer-column">
      <h3>Ilovani yuklab olish</h3>
      <div class="social-links">
        <p>App Store</p>
        <p>Google Play</p>
      </div>
      <h3>Ijtimoiy tarmoqlar</h3>
      <div class="social-icons">
        <a href="#">Instagram</a>
        <a href="#">Telegram</a>
      </div>
    </div>
  </div>
  <hr>
  <div class="footer-bottom">
    <p>Maxfiylik kelishuvi | Foydalanuvchi kelishuvi | SHAXSIY MA'LUMOTLARNI QAYTA ISHLASH NIZOMI</p>
    <p>© 2026 Top-Savdo B2B. Barcha huquqlar himoyalangan.</p>
  </div>
</footer>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

export default {
  name: 'LandingView',
  setup() {
    const router = useRouter();
    const backendUrl = 'http://127.0.0.1:8000';

    const dealers = ref([]);
    const loadingDealers = ref(false);
    const dealersError = ref('');

    const selectedDealer = ref(null);
    const products = ref([]);
    const loadingProducts = ref(false);
    const productsError = ref('');

    const totalProductsCount = computed(() =>
      dealers.value.reduce((sum, d) => sum + (d.products_count || 0), 0)
    );

    const fetchDealers = async () => {
      loadingDealers.value = true;
      dealersError.value = '';
      try {
        const response = await api.get('/public/dealers/');
        dealers.value = response.data.results || response.data;
      } catch (error) {
        dealersError.value = "Dilerlarni yuklab bo'lmadi. Server bilan aloqa yo'q.";
      } finally {
        loadingDealers.value = false;
      }
    };

    const fetchProducts = async (dealerId = null) => {
      loadingProducts.value = true;
      productsError.value = '';
      try {
        const params = dealerId ? { dealer: dealerId } : {};
        const response = await api.get('/catalog/', { params });
        products.value = response.data.results || response.data;
      } catch (error) {
        productsError.value = "Mahsulotlarni yuklab bo'lmadi.";
      } finally {
        loadingProducts.value = false;
      }
    };

    const openDealer = (dealer) => {
      selectedDealer.value = dealer;
      fetchProducts(dealer.id);
      requestAnimationFrame(() => {
        document.getElementById('products-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    };

    const showAllProducts = () => {
      selectedDealer.value = null;
      fetchProducts(null);
    };

    const goToLogin = () => {
      router.push('/login');
    };

    // 🟢 Diler ustiga bosilganda uning "Batafsil" (detail) sahifasiga o'tish
    const goToDealerDetail = (dealerId) => {
      router.push(`/dealer/${dealerId}`);
    };

    // 🟢 Mahsulot ustiga (rasm/nom/"Batafsil") bosilganda detail sahifasiga o'tish
    const goToProductDetail = (productId) => {
      router.push(`/product/${productId}`);
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

    // 🟢 Diler "qachon beri ishlayapti" (necha oy/yil faoliyatda) — ishonch uchun
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

    onMounted(() => {
      fetchDealers();
      fetchProducts(null); // Boshida barcha mahsulotlar ko'rsatiladi
    });

    return {
      dealers,
      loadingDealers,
      dealersError,
      selectedDealer,
      products,
      loadingProducts,
      productsError,
      totalProductsCount,
      openDealer,
      showAllProducts,
      goToLogin,
      goToDealerDetail,
      goToProductDetail,
      getImageUrl,
      formatPrice,
      initials,
      memberSince
    };
  }
};
</script>

<style scoped>
.landing {
  min-height: 100vh;
  background: #f5f7fb;
}

/* ---------- Navbar ---------- */
.navbar {
  background: linear-gradient(135deg, #0a2f1d 0%, #114e32 50%, #1f6e43 100%);
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
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
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.brand i { font-size: 24px; color: #34d399; }
.nav-actions { display: flex; gap: 12px; }
.btn {
  padding: 9px 18px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  cursor: pointer;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.btn.sm { padding: 7px 14px; font-size: 13px; }
.btn.lg { padding: 13px 26px; font-size: 15px; }
.btn-ghost {
  color: #fff;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.35);
}
.btn-ghost:hover { background: rgba(255, 255, 255, 0.22); }
.btn-primary {
  background: linear-gradient(to right, #10b981, #059669);
  color: #fff;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.35);
}
.btn-primary:hover { box-shadow: 0 6px 18px rgba(5, 150, 105, 0.45); transform: translateY(-1px); }
.btn-outline {
  background: #fff;
  color: #114e32;
  border: 1px solid #d1e7dd;
}
.btn-outline:hover { border-color: #10b981; background: #f0fdf4; }

/* ---------- Hero ---------- */
.hero {
  background: linear-gradient(180deg, #ffffff 0%, #eef8f2 100%);
  border-bottom: 1px solid #e2f0e7;
}
.hero-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 64px 24px 56px;
  display: grid;
  grid-template-columns: 1.1fr 0.9fr;
  gap: 40px;
  align-items: center;
}
.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: #ecfdf5;
  color: #059669;
  font-size: 13px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
  margin-bottom: 18px;
}
.hero-text h1 {
  font-size: 38px;
  line-height: 1.25;
  color: #0a2f1d;
  margin-bottom: 18px;
  font-weight: 800;
}
.hero-text h1 span { color: #059669; }
.hero-text p {
  color: #556b60;
  font-size: 15.5px;
  line-height: 1.7;
  max-width: 520px;
  margin-bottom: 28px;
}
.hero-actions { display: flex; gap: 14px; margin-bottom: 40px; flex-wrap: wrap; }

.stats-row { display: flex; gap: 36px; }
.stat { display: flex; flex-direction: column; }
.stat strong { font-size: 24px; color: #0a2f1d; font-weight: 800; }
.stat span { font-size: 13px; color: #6b7280; }

.hero-art { display: flex; align-items: center; justify-content: center; }
.hero-svg { width: 100%; max-width: 420px; height: auto; filter: drop-shadow(0 12px 24px rgba(16, 185, 129, 0.18)); }

/* ---------- Sections ---------- */
.section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 48px 24px;
}
.products-section { padding-top: 12px; }
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 22px;
  flex-wrap: wrap;
}
.section-title {
  font-size: 22px;
  color: #114e32;
  font-weight: 800;
  margin-bottom: 4px;
}
.section-sub { color: #8a9a92; font-size: 13.5px; }

.state-msg {
  text-align: center;
  color: #6b7280;
  padding: 30px;
  font-size: 14px;
}
.state-msg.error { color: #dc2626; }
.spin { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ---------- Dealer grid ---------- */
.dealer-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 18px;
}
.dealer-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  border: 1px solid #eef2f0;
}
.dealer-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
}
.dealer-card.active { border-color: #10b981; box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15); }
.dealer-avatar {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: linear-gradient(135deg, #10b981, #059669);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  flex-shrink: 0;
}
.dealer-info { flex: 1; min-width: 0; }
.dealer-name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 4px;
}
.dealer-info h3 { font-size: 16px; color: #0a2f1d; margin: 0; }
.trust-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 10.5px;
  font-weight: 700;
  color: #0369a1;
  background: #e0f2fe;
  padding: 2px 8px;
  border-radius: 20px;
  white-space: nowrap;
}
.trust-badge i { color: #0284c7; }
.member-since {
  font-size: 12px;
  color: #059669 !important;
  font-weight: 600;
}
.dealer-info p { font-size: 13px; color: #6b7280; display: flex; align-items: center; gap: 6px; margin-bottom: 8px; }
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #ecfdf5;
  color: #059669;
  font-size: 12px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}
.arrow { font-size: 22px; color: #9ca3af; }

/* ---------- Product grid ---------- */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 20px;
}
.product-card {
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  border: 1px solid #eef2f0;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 26px rgba(0, 0, 0, 0.12);
}
.product-image {
  position: relative;
  height: 235px;
  background: #f6f6f6;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.product-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.product-card:hover .product-image img { transform: scale(1.06); }
.placeholder-icon { font-size: 40px; color: #cbd5e1; }
.stock-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(5, 150, 105, 0.92);
  color: #fff;
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 20px;
}
.stock-badge.low { background: rgba(220, 38, 38, 0.92); }
.product-body { padding: 14px 16px; }
.category { font-size: 11.5px; color: #9ca3af; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.3px; }
.product-body h4 { font-size: 15px; color: #0a2f1d; margin-bottom: 6px; line-height: 1.3; }
.about-link {
  background: none;
  border: none;
  padding: 0;
  margin: 0 0 8px;
  color: #059669;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.about-link:hover { text-decoration: underline; }
.dealer-tag {
  font-size: 12px;
  color: #059669;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 10px;
}
.price-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.price { font-weight: 800; color: #059669; font-size: 14.5px; }
.buy-btn {
  background: linear-gradient(to right, #10b981, #059669);
  color: #fff;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}
.buy-btn:hover { box-shadow: 0 4px 12px rgba(5, 150, 105, 0.4); transform: scale(1.03); }

.footer {
  background-color: #fcfcfc; /* Och fon rangi */
  padding: 40px 20px;
  font-family: sans-serif;
  border-top: 1px solid #e0e0e0;
}

.footer-container {
  display: flex;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 20px;
}

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.footer-column h3 {
  font-size: 16px;
  color: #000;
  margin-bottom: 5px;
}

.footer-column a {
  text-decoration: none;
  color: #666; /* Ochroq kulrang */
  font-size: 14px;
}

.footer-column a:hover {
  color: #004d40; /* Top-Savdo navbar rangi */
}

.footer-bottom {
  text-align: center;
  margin-top: 40px;
  font-size: 12px;
  color: #999;
}

hr {
  border: 0;
  border-top: 1px solid #eee;
  margin: 30px 0;
}

@media (max-width: 860px) {
  .hero-inner { grid-template-columns: 1fr; }
  .hero-art { order: -1; max-width: 320px; margin: 0 auto; }
}
@media (max-width: 560px) {
  .navbar-inner { flex-direction: column; gap: 12px; }
  .hero-text h1 { font-size: 28px; }
  .stats-row { gap: 22px; }
}
</style>