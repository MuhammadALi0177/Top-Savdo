<template>
  <div class="landing orders-landing">
    <!-- ==================== TOP NAVBAR ==================== -->
    <header class="navbar">
      <div class="navbar-inner">
        <div class="navbar-top-row">
          <div class="brand">
            <span class="brand__box">TS</span>
            <span class="brand__word">Top-Savdo <em>B2B</em></span>
          </div>

          <div class="nav-icons">
            <button class="btn btn-outline cart-nav-btn" @click="isCartOpen = true" title="Savat">
              <i class="ri-shopping-cart-2-line"></i>
              <span class="btn-text">Savat</span>
              <span class="cart-count" v-if="cart.length > 0">{{ cart.length }}</span>
            </button>
            <button class="btn btn-ghost" @click="handleLogout" title="Chiqish">
              <i class="ri-logout-box-r-line"></i>
            </button>
          </div>
        </div>

        <div class="nav-tabs">
          <button
            class="btn tab-btn"
            :class="activeTab === 'catalog' ? 'btn-primary' : 'btn-ghost'"
            @click="activeTab = 'catalog'"
          >
            <i class="ri-store-2-line"></i> <span class="btn-text">Katalog</span>
          </button>
          <button
            class="btn tab-btn"
            :class="activeTab === 'history' ? 'btn-primary' : 'btn-ghost'"
            @click="activeTab = 'history'"
          >
            <i class="ri-history-line"></i> <span class="btn-text">Savdo tarixi</span>
          </button>
          <button
            class="btn tab-btn"
            :class="activeTab === 'debts' ? 'btn-primary' : 'btn-ghost'"
            @click="activeTab = 'debts'"
          >
            <i class="ri-wallet-3-line"></i> <span class="btn-text">Qarzlar &amp; limitlar</span>
          </button>
        </div>
      </div>
    </header>

    <!-- ==================== HERO / STATISTIKA ==================== -->
    <section class="hero orders-hero">
      <div class="hero-inner orders-hero-inner">
        <div class="hero-text">
          <span class="hero-tag"><i class="ri-user-smile-line"></i> Magazinchi paneli</span>
          <h1>Xush kelibsiz! <span>Buyurtmalaringizni</span> boshqaring</h1>
          <p>
            Katalogdan mahsulot tanlab savatga qo'shing, savdo tarixingizni kuzating
            va dilerlar bo'yicha qarz-limitlaringizni bir joyda nazorat qiling.
          </p>

          <div class="stats-row">
            <div class="stat">
              <strong>{{ orders.length }}</strong>
              <span>jami buyurtma</span>
            </div>
            <div class="stat">
              <strong>{{ formatPrice(totalDebtSum) }}</strong>
              <span>umumiy qarz (so'm)</span>
            </div>
            <div class="stat">
              <strong>{{ uniqueDealerLimits.length }}</strong>
              <span>faol diler</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== KATALOG ==================== -->
    <section id="catalog-section" class="section" v-if="activeTab === 'catalog'">
      <div class="section-head">
        <div>
          <h2 class="section-title">Mahsulotlar katalogi</h2>
          <p class="section-sub">Kerakli mahsulotni tanlang va savatga qo'shing</p>
        </div>
      </div>

      <div v-if="products.length === 0" class="state-msg">
        <i class="ri-loader-4-line spin"></i> Mahsulotlar yuklanmoqda...
      </div>

      <div v-else class="product-grid">
        <div v-for="product in products" :key="product.id" class="product-card">
          <div class="product-image" @click="goToProductDetail(product.id)" style="cursor: pointer">
            <img v-if="product.image" :src="getProductImageUrl(product.image)" :alt="product.name" />
            <i v-else class="ri-image-2-line placeholder-icon"></i>
            <span class="stock-badge" :class="{ low: product.stock < 10 }">
              {{ product.stock > 0 ? `${product.stock} dona` : "Tugagan" }}
            </span>
          </div>
          <div class="product-body">
            <h4 :title="product.name" @click="goToProductDetail(product.id)" style="cursor: pointer">{{ product.name }}</h4>
            <button class="about-link" @click="goToProductDetail(product.id)">
              <i class="ri-information-line"></i> Haqida / Batafsil
            </button>
            <div class="price-row">
              <span class="price">{{ formatPrice(product.price) }} so'm</span>
            </div>

            <div class="card-footer-actions" v-if="product.stock > 0">
              <div class="qty-selector">
                <input type="number" v-model.number="quantities[product.id]" min="1" :max="product.stock" class="qty-input" />
              </div>
              <button @click="addToCart(product)" class="buy-btn">
                <i class="ri-add-circle-line"></i> Savatga
              </button>
            </div>
            <div v-else class="out-of-stock-alert">Mahsulot tugagan</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== SAVDO TARIXI ==================== -->
    <section id="history-section" class="section" v-if="activeTab === 'history'">
      <div class="section-head">
        <div>
          <h2 class="section-title">Savdo tarixi</h2>
          <p class="section-sub">Barcha xaridlaringiz ro'yxati</p>
        </div>
      </div>

      <div v-if="orders.length === 0" class="state-msg">
        <i class="ri-history-line"></i> Sizda hali savdo tarixi mavjud emas.
      </div>

      <div v-else class="order-history-list">
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-card-top">
            <div class="order-card-id">
              <span class="order-hash">#{{ order.id }}</span>
              <strong class="order-dealer-name">{{ order.dealer_company_name || 'Noma\'lum Diler' }}</strong>
            </div>
            <span class="status-pill" :class="order.status.toLowerCase()">{{ order.status_display || order.status }}</span>
          </div>

          <div class="order-card-date">
            <i class="ri-calendar-2-line"></i> {{ formatDate(order.created_at) }}
          </div>

          <!-- 🟢 Kuryer yo'lga chiqqach (SHIPPED) yoki yetkazib bergach (DELIVERED)
               mijozga kuryerning ismi va telefon raqami ko'rsatiladi -->
          <div
            v-if="['SHIPPED', 'DELIVERED'].includes(order.status) && order.courier_id"
            class="courier-info-box"
          >
            <div class="courier-info-icon">
              <i class="ri-e-bike-2-line"></i>
            </div>
            <div class="courier-info-text">
              <span class="courier-info-title">
                {{ order.status === 'SHIPPED' ? "Kuryer yo'lda" : "Kuryer yetkazib berdi" }}
              </span>
              <span class="courier-info-name">{{ order.courier_name }}</span>
            </div>
            <a v-if="order.courier_phone" :href="`tel:${order.courier_phone}`" class="courier-call-btn">
              <i class="ri-phone-fill"></i> {{ order.courier_phone }}
            </a>
          </div>

          <div class="order-card-amounts">
            <div class="amount-block">
              <span class="amount-label">Jami summa</span>
              <strong class="amount-value">{{ formatPrice(order.total_amount) }} so'm</strong>
            </div>
            <div class="amount-block">
              <span class="amount-label">To'langan</span>
              <strong class="amount-value text-success">{{ formatPrice(order.paid_amount) }} so'm</strong>
            </div>
            <div class="amount-block">
              <span class="amount-label">Nasiya (Qarz)</span>
              <strong class="amount-value" :class="{'text-danger': order.debt_amount > 0}">{{ formatPrice(order.debt_amount) }} so'm</strong>
            </div>
          </div>

          <div class="order-card-footer">
            <button
              v-if="order.status === 'PENDING'"
              @click="atkazQilish(order.id)"
              class="atkaz-btn">
              <i class="ri-close-circle-line"></i> Bekor qilish
            </button>
            <span v-else class="text-muted-light"><i class="ri-checkbox-circle-line"></i> Bajarilgan</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== QARZLAR & LIMITLAR ==================== -->
    <section id="debts-section" class="section" v-if="activeTab === 'debts'">
      <div class="section-head">
        <div>
          <h2 class="section-title">Qarzlar va limitlar</h2>
          <p class="section-sub">Dilerlar bo'yicha ajratilgan limit va joriy qarzingiz</p>
        </div>
      </div>

      <div v-if="uniqueDealerLimits.length === 0" class="state-msg">
        <i class="ri-wallet-3-line"></i> Sizga biror diler tomonidan limit ajratilmagan.
      </div>

      <div v-else class="debts-list">
        <div v-for="order in uniqueDealerLimits" :key="order.id" class="debt-card">
          <div class="debt-card-header">
            <strong class="debt-dealer-name"><i class="ri-building-4-line"></i> {{ order.dealer_company_name }}</strong>
            <span class="status-pill" :class="order.client_current_debt > 0 ? 'cancelled' : 'delivered'">
              {{ order.client_current_debt > 0 ? 'Qarz bor' : 'Qarz yo\'q' }}
            </span>
          </div>
          <div class="debt-card-body">
            <div class="amount-block">
              <span class="amount-label">Ajratilgan limit</span>
              <strong class="amount-value">{{ formatPrice(order.client_credit_limit) }} so'm</strong>
            </div>
            <div class="amount-block">
              <span class="amount-label">Joriy qarzimiz</span>
              <strong class="amount-value text-danger">{{ formatPrice(order.client_current_debt) }} so'm</strong>
            </div>
            <div class="amount-block">
              <span class="amount-label">Mavjud (bo'sh) limit</span>
              <strong class="amount-value text-success">{{ formatPrice(order.client_credit_limit - order.client_current_debt) }} so'm</strong>
            </div>
          </div>
          <div class="debt-progress-track">
            <div class="debt-progress-fill" :style="{ width: debtPercentage(order) + '%' }"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== SAVAT (CART) SIDEBAR ==================== -->
    <div class="cart-overlay" :class="{ 'active': isCartOpen }" @click.self="isCartOpen = false">
      <div class="cart-sidebar" :class="{ 'open': isCartOpen }">
        <div class="sidebar-header">
          <h3><i class="ri-shopping-cart-2-line"></i> Sizning savatingiz</h3>
          <button @click="isCartOpen = false" class="close-sidebar-btn"><i class="ri-close-line"></i></button>
        </div>
        <div v-if="cart.length === 0" class="empty-cart-msg"><p>Savatingiz hozircha bo'sh</p></div>
        <div v-else class="sidebar-content">
          <div class="cart-items-list">
            <div v-for="(item, index) in cart" :key="index" class="cart-item-card">
              <div class="item-details">
                <h5>{{ item.name }}</h5>
                <p class="item-price-calc">{{ formatPrice(item.price) }} so'm × {{ item.quantity }} dona</p>
                <p class="item-total">Jami: <span>{{ formatPrice(item.quantity * item.price) }}</span> so'm</p>
              </div>
              <button @click="removeFromCart(index)" class="delete-item-btn"><i class="ri-delete-bin-7-line"></i></button>
            </div>
          </div>
          <div class="sidebar-summary">
            <div class="summary-card">
              <div class="summary-row"><span>Umumiy summa:</span><strong class="total-price">{{ formatPrice(totalCartAmount) }} so'm</strong></div>
              <div class="pay-input-group">
                <label>Hozir to'lanadigan qism (so'm):</label>
                <input type="number" v-model.number="paidAmount" min="0" :max="totalCartAmount" />
              </div>
              <div class="summary-row debt-row"><span>Nasiya (Qarz):</span><span class="debt-price">{{ formatPrice(totalCartAmount - paidAmount) }} so'm</span></div>
            </div>
            <button @click="submitOrder" :disabled="submitting" class="checkout-btn">
              {{ submitting ? 'Yuborilmoqda...' : 'Buyurtmani tasdiqlash' }}
            </button>
          </div>
        </div>
        <div class="toast-messages">
          <div v-if="errorMsg" class="error-box">{{ errorMsg }}</div>
          <div v-if="successMsg" class="success-box">{{ successMsg }}</div>
        </div>
      </div>
    </div>
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
import { ref, onMounted, computed, watch } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api';

export default {
  setup() {
    const activeTab = ref('catalog');
    const products = ref([]);
    const quantities = ref({});
    const cart = ref([]);
    const paidAmount = ref(0);
    const submitting = ref(false);
    const errorMsg = ref('');
    const successMsg = ref('');
    const isCartOpen = ref(false);
    const orders = ref([]);
    const router = useRouter();
    const backendUrl = 'https://surprising-enchantment-production-5152.up.railway.app';

    const fetchOrderHistory = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await api.get('orders/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        orders.value = response.data || [];
      } catch (error) {
        console.error("Tarixni yuklashda xatolik:", error);
      }
    };

    // 🟢 BEKOR QILISH FUNKSIYASI (BACKEND ALOQASI BILAN)
    const atkazQilish = async (orderId) => {
      if (!confirm(`Haqiqatan ham #${orderId}-buyurtmani atkaz (bekor) qilmoqchimisiz?`)) return;

      try {
        const token = localStorage.getItem('token');
        await api.post(`orders/${orderId}/cancel/`, {}, {
          headers: { 'Authorization': `Token ${token}` }
        });

        alert("Buyurtmangiz muvaffaqiyatli bekor qilindi! ❌");
        fetchOrderHistory();
      } catch (error) {
        console.error("Atkaz qilishda xato:", error);
        alert("Buyurtmani bekor qilib bo'lmadi. Diler qabul qilib bo'lgan bo'lishi mumkin.");
      }
    };

    const uniqueDealerLimits = computed(() => {
      const dealers = {};
      orders.value.forEach(order => {
        if (order.dealer_company_name && !dealers[order.dealer_company_name]) {
          dealers[order.dealer_company_name] = {
            id: order.id,
            dealer_company_name: order.dealer_company_name,
            client_credit_limit: order.client_credit_limit || 0,
            client_current_debt: order.client_current_debt || 0
          };
        }
      });
      return Object.values(dealers);
    });

    const totalDebtSum = computed(() => {
      return uniqueDealerLimits.value.reduce((sum, d) => sum + (d.client_current_debt || 0), 0);
    });

    const debtPercentage = (order) => {
      if (!order.client_credit_limit || order.client_credit_limit <= 0) return 0;
      const pct = (order.client_current_debt / order.client_credit_limit) * 100;
      return Math.min(100, Math.max(0, pct));
    };

    const fetchProducts = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await api.get('products/', {
          headers: { 'Authorization': `Token ${token}` }
        });
        products.value = response.data;
        products.value.forEach(p => { quantities.value[p.id] = 1; });
      } catch (error) {
        errorMsg.value = "Katalogni yuklashda xatolik yuz berdi.";
      }
    };

    const getProductImageUrl = (imagePath) => {
      if (!imagePath) return '';
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) return imagePath;
      return `${backendUrl}${imagePath.startsWith('/') ? '' : '/'}${imagePath}`;
    };

    const addToCart = (product) => {
      const qty = quantities.value[product.id] || 1;
      if (qty > product.stock) { alert(`Omborda ${product.stock} dona bor!`); return; }
      const existingItem = cart.value.find(item => item.id === product.id);
      if (existingItem) {
        if (existingItem.quantity + qty > product.stock) { alert("Savat qoldiqdan oshib ketdi!"); return; }
        existingItem.quantity += qty;
      } else {
        cart.value.push({ id: product.id, name: product.name, price: product.price, dealer: product.dealer, quantity: qty });
      }
      isCartOpen.value = true;
    };

    // 🟢 Mahsulot ustiga (rasm/nom/"Batafsil") bosilganda detail sahifasiga o'tish
    const goToProductDetail = (productId) => {
      router.push(`/product/${productId}`);
    };

    const removeFromCart = (index) => { cart.value.splice(index, 1); };
    const totalCartAmount = computed(() => cart.value.reduce((sum, item) => sum + (item.quantity * item.price), 0));
    watch(totalCartAmount, (newTotal) => { paidAmount.value = newTotal; });

    const extractErrorMessage = (error) => {
      const data = error?.response?.data;
      if (!data) return "Server bilan aloqa yo'q yoki tarmoq xatosi yuz berdi.";

      if (typeof data === 'string') return data;
      if (data.non_field_errors?.length) return data.non_field_errors[0];
      if (data.detail) return data.detail;
      if (data.message) return data.message;

      const firstKey = Object.keys(data)[0];
      if (firstKey) {
        const val = data[firstKey];
        return Array.isArray(val) ? val[0] : String(val);
      }
      return "Buyurtmani yuborishda noma'lum xatolik yuz berdi.";
    };

    const submitOrder = async () => {
      if (cart.value.length === 0) return;
      submitting.value = true; errorMsg.value = ''; successMsg.value = '';
      try {
        const token = localStorage.getItem('token');
        const firstItem = cart.value[0];
        const orderPayload = {
          client: parseInt(localStorage.getItem('user_id')),
          dealer: firstItem.dealer,
          paid_amount: Number(paidAmount.value),
          items: cart.value.map(item => ({ product: item.id, quantity: item.quantity, price_at_order: item.price }))
        };
        await api.post('orders/', orderPayload, { headers: { 'Authorization': `Token ${token}` } });
        successMsg.value = "Buyurtma qabul qilindi!";
        cart.value = []; paidAmount.value = 0;
        setTimeout(() => { isCartOpen.value = false; successMsg.value = ''; }, 1500);
        fetchProducts();
        fetchOrderHistory();
      } catch (error) {
        errorMsg.value = extractErrorMessage(error);
      } finally { submitting.value = false; }
    };

    const handleLogout = () => { localStorage.clear(); router.push('/'); };
    const formatPrice = (val) => parseFloat(val).toLocaleString();
    const formatDate = (dateStr) => new Date(dateStr).toLocaleDateString('uz-UZ');

    onMounted(() => {
      fetchProducts();
      fetchOrderHistory();
    });

    return {
      activeTab, products, quantities, cart, paidAmount, submitting, errorMsg, successMsg,
      isCartOpen, totalCartAmount, orders, uniqueDealerLimits, totalDebtSum, debtPercentage,
      addToCart, removeFromCart, submitOrder, handleLogout, formatPrice,
      getProductImageUrl, formatDate, atkazQilish, goToProductDetail
    };
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

.orders-landing {
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
  background: linear-gradient(160deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  position: sticky;
  top: 0;
  z-index: 10;
  box-shadow: 0 4px 18px rgba(7, 27, 16, 0.2);
}
.navbar-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}
.navbar-top-row { display: contents; }
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
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
.brand__word em { font-style: normal; color: #6ee7a8; }

.nav-tabs { display: flex; gap: 8px; align-items: center; flex: 1 1 auto; }
.nav-icons { display: flex; gap: 10px; align-items: center; flex-shrink: 0; }

.btn {
  padding: 9px 16px;
  border-radius: 9px;
  font-weight: 600;
  font-size: 13.5px;
  text-decoration: none;
  cursor: pointer;
  border: none;
  font-family: inherit;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
  position: relative;
  flex-shrink: 0;
}
.btn-ghost {
  color: #d5ecdf;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.16);
}
.btn-ghost:hover { background: rgba(255, 255, 255, 0.15); color: #fff; }
.btn-primary {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.35);
}
.btn-primary:hover { box-shadow: 0 8px 20px rgba(5, 150, 105, 0.45); transform: translateY(-1px); }
.btn-outline {
  background: rgba(255, 255, 255, 0.95);
  color: var(--forest-900);
  border: 1px solid rgba(255, 255, 255, 0.5);
}
.btn-outline:hover { background: #fff; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }
.cart-count {
  background: #ef4444;
  color: white;
  border-radius: 20px;
  padding: 1px 7px;
  font-size: 11px;
  margin-left: 2px;
}

/* ---------- Hero ---------- */
.orders-hero {
  background:
    radial-gradient(circle at 90% 0%, rgba(34, 197, 94, 0.08), transparent 45%),
    linear-gradient(180deg, #ffffff 0%, #eef8f2 100%);
  border-bottom: 1px solid var(--line);
}
.orders-hero-inner { max-width: 1180px; margin: 0 auto; padding: 48px 24px 40px; }
.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(34, 197, 94, 0.1);
  color: var(--forest-700);
  font-size: 12.5px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 20px;
  margin-bottom: 18px;
}
.hero-text h1 {
  font-family: 'Manrope', sans-serif;
  font-size: 33px;
  line-height: 1.25;
  color: var(--ink-900);
  margin-bottom: 14px;
  font-weight: 800;
  letter-spacing: -0.3px;
}
.hero-text h1 span { color: var(--accent-600); }
.hero-text p {
  color: var(--ink-600);
  font-size: 14.5px;
  line-height: 1.7;
  max-width: 620px;
  margin-bottom: 28px;
}

.stats-row { display: flex; gap: 14px; flex-wrap: wrap; }
.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px 22px;
  min-width: 140px;
}
.stat strong { font-family: 'Manrope', sans-serif; font-size: 22px; color: var(--ink-900); font-weight: 800; }
.stat span { font-size: 12px; color: var(--ink-600); }

/* ---------- Sections ---------- */
.section { max-width: 1180px; margin: 0 auto; padding: 42px 24px; }
.section-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}
.section-title { font-family: 'Manrope', sans-serif; font-size: 22px; color: var(--forest-900); font-weight: 800; margin-bottom: 4px; }
.section-sub { color: var(--ink-600); font-size: 13.5px; }

.state-msg {
  text-align: center;
  color: var(--ink-600);
  padding: 50px;
  font-size: 14px;
  background: #fff;
  border-radius: 16px;
  border: 1px solid var(--line);
}
.spin { display: inline-block; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ---------- Product grid (Katalog) ---------- */
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 20px; }
.product-card {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid var(--line);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.product-card:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(10, 47, 29, 0.1); }
.product-image {
  position: relative;
  height: 210px;
  background: linear-gradient(155deg, #eef4f0 0%, #e4efe8 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.product-image img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.product-card:hover .product-image img { transform: scale(1.06); }
.placeholder-icon { font-size: 40px; color: #b7c6bd; }
.stock-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255, 255, 255, 0.95);
  color: #15803d;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}
.stock-badge.low { color: #b91c1c; }
.product-body { padding: 16px 16px 18px; }
.product-body h4 {
  font-size: 14.5px;
  font-weight: 700;
  color: var(--ink-900);
  margin: 0 0 8px;
  line-height: 1.3;
  height: 38px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.about-link {
  background: none;
  border: none;
  padding: 0;
  margin: 0 0 10px;
  color: var(--accent-600);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.about-link:hover { text-decoration: underline; }
.price-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 12px; }
.price { font-family: 'Manrope', sans-serif; font-weight: 800; color: var(--forest-900); font-size: 16px; }

.card-footer-actions { display: flex; gap: 8px; }
.qty-selector { background: var(--paper); border-radius: 8px; border: 1px solid var(--line); }
.qty-input { width: 45px; height: 36px; border: none; background: transparent; text-align: center; outline: none; font-weight: 700; font-family: inherit; color: var(--ink-900); }
.buy-btn {
  flex: 1;
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.buy-btn:hover { box-shadow: 0 6px 16px rgba(5, 150, 105, 0.38); transform: translateY(-1px); }
.out-of-stock-alert { background: var(--paper); color: #94a3b8; font-size: 12px; text-align: center; padding: 9px; border-radius: 8px; font-weight: 600; }

/* ---------- Savdo tarixi ---------- */
.order-history-list { display: flex; flex-direction: column; gap: 14px; }
.order-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px 22px;
  border: 1px solid var(--line);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.order-card:hover { transform: translateY(-2px); box-shadow: 0 12px 26px rgba(10, 47, 29, 0.08); }
.order-card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; flex-wrap: wrap; gap: 8px; }
.order-card-id { display: flex; align-items: center; gap: 10px; }
.order-hash { font-size: 12px; color: var(--ink-600); font-weight: 700; }
.order-dealer-name { color: var(--ink-900); font-size: 15px; font-weight: 700; }
.order-card-date { font-size: 12px; color: var(--ink-600); margin-bottom: 16px; display: flex; align-items: center; gap: 6px; }

/* Kuryer ma'lumoti */
.courier-info-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(34, 197, 94, 0.06);
  border: 1px solid rgba(34, 197, 94, 0.22);
  border-radius: 12px;
  padding: 11px 14px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.courier-info-icon {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--forest-700);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.courier-info-text { display: flex; flex-direction: column; flex: 1; min-width: 120px; }
.courier-info-title { font-size: 11px; font-weight: 700; color: var(--accent-600); text-transform: uppercase; letter-spacing: 0.3px; }
.courier-info-name { font-size: 14px; color: var(--ink-900); font-weight: 700; }
.courier-call-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--forest-900);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 10px;
  text-decoration: none;
  white-space: nowrap;
  transition: background 0.2s;
}
.courier-call-btn:hover { background: var(--forest-700); }

.order-card-amounts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  background: var(--paper);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 14px;
}
.amount-block { display: flex; flex-direction: column; gap: 4px; }
.amount-label { font-size: 11px; color: var(--ink-600); }
.amount-value { font-size: 14px; font-weight: 700; color: var(--ink-900); }

.order-card-footer { display: flex; justify-content: flex-end; }

.atkaz-btn {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  padding: 7px 13px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 12px;
  font-family: inherit;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s;
}
.atkaz-btn:hover { background: #dc2626; color: white; border-color: #dc2626; }
.text-muted-light { color: #94a3b8; font-size: 13px; font-style: italic; display: inline-flex; align-items: center; gap: 4px; }

.status-pill { padding: 5px 12px; border-radius: 20px; font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.4px; }
.status-pill.delivered { background: #e2fbe8; color: #15803d; }
.status-pill.pending { background: #fef3c7; color: #b45309; }
.status-pill.cancelled { background: #fee2e2; color: #b91c1c; }
.status-pill.canceled { background: #fee2e2; color: #b91c1c; }

.text-success { color: var(--accent-600) !important; }
.text-danger { color: #dc2626 !important; }

/* ---------- Qarzlar & limitlar ---------- */
.debts-list { display: flex; flex-direction: column; gap: 14px; }
.debt-card {
  background: #fff;
  border-radius: 16px;
  padding: 20px 22px;
  border: 1px solid var(--line);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.debt-card:hover { transform: translateY(-2px); box-shadow: 0 12px 26px rgba(10, 47, 29, 0.08); }
.debt-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; flex-wrap: wrap; gap: 8px; }
.debt-dealer-name { color: var(--ink-900); font-size: 15px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.debt-card-body {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 10px;
  background: var(--paper);
  border-radius: 12px;
  padding: 14px 16px;
  margin-bottom: 14px;
}
.debt-progress-track { height: 8px; background: var(--paper); border: 1px solid var(--line); border-radius: 20px; overflow: hidden; }
.debt-progress-fill { height: 100%; background: linear-gradient(to right, #f87171, #dc2626); border-radius: 20px; transition: width 0.4s ease; }

/* ---------- Savat (Cart) sidebar ---------- */
.cart-overlay {
  position: fixed; inset: 0; width: 100%;
  height: 100vh; height: 100dvh;
  background: rgba(7, 27, 16, 0.5);
  backdrop-filter: blur(3px);
  z-index: 1000;
  opacity: 0; visibility: hidden; pointer-events: none;
  transition: opacity 0.3s, visibility 0.3s;
}
.cart-overlay.active { opacity: 1; visibility: visible; pointer-events: auto; }
.cart-sidebar {
  position: fixed; top: 0; right: 0;
  width: 420px; max-width: 100vw;
  height: 100vh; height: 100dvh;
  background: white;
  z-index: 1001;
  display: flex; flex-direction: column;
  min-height: 0;
  transform: translateX(100%);
  transition: transform 0.3s ease;
  box-shadow: -8px 0 30px rgba(7, 27, 16, 0.18);
  overflow: hidden;
}
.cart-sidebar.open { transform: translateX(0); }
.sidebar-header { flex-shrink: 0; padding: 20px; border-bottom: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; }
.sidebar-header h3 { margin: 0; color: var(--forest-900); font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
.close-sidebar-btn { background: transparent; border: none; font-size: 20px; cursor: pointer; color: var(--ink-600); padding: 4px; line-height: 1; }
.sidebar-content { flex: 1 1 auto; min-height: 0; display: flex; flex-direction: column; overflow: hidden; background: var(--paper); }
.cart-items-list { flex: 1 1 auto; min-height: 0; overflow-y: auto; -webkit-overflow-scrolling: touch; padding: 16px; display: flex; flex-direction: column; gap: 10px; }
.cart-item-card { display: flex; justify-content: space-between; align-items: center; gap: 10px; background: white; padding: 12px; border-radius: 12px; border: 1px solid var(--line); }
.item-details h5 { margin: 0 0 4px 0; color: var(--ink-900); font-size: 13px; font-weight: 700; }
.item-price-calc { margin: 0; font-size: 11px; color: var(--ink-600); }
.item-total { margin: 4px 0 0 0; font-size: 12px; color: var(--ink-900); }
.item-total span { font-weight: 700; }
.delete-item-btn { flex-shrink: 0; background: #fef2f2; color: #ef4444; border: none; width: 30px; height: 30px; border-radius: 8px; cursor: pointer; }
.delete-item-btn:hover { background: #fee2e2; }
.sidebar-summary { flex-shrink: 0; padding: 20px; background: white; border-top: 1px solid var(--line); max-height: 60vh; overflow-y: auto; }
.summary-card { background: var(--paper); padding: 16px; border-radius: 14px; border: 1px solid var(--line); }
.summary-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 13px; color: var(--ink-900); }
.total-price { font-size: 15px; font-weight: 800; }
.pay-input-group { margin: 10px 0; }
.pay-input-group label { font-size: 12px; color: var(--ink-600); }
.pay-input-group input {
  width: 100%; padding: 11px 12px; border-radius: 9px; border: 1.5px solid var(--line);
  box-sizing: border-box; margin-top: 6px; outline: none; font-family: inherit; font-size: 14px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.pay-input-group input:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.14); }
.debt-row { background: #fef2f2; color: #b91c1c; padding: 8px 10px; border-radius: 8px; margin-top: 4px; font-weight: 600; }
.checkout-btn {
  width: 100%;
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  padding: 13px;
  border-radius: 11px;
  font-weight: 700;
  font-family: 'Manrope', sans-serif;
  font-size: 14.5px;
  cursor: pointer;
  margin-top: 14px;
  box-shadow: 0 8px 20px rgba(5, 150, 105, 0.28);
  transition: all 0.25s ease;
}
.checkout-btn:hover { box-shadow: 0 10px 24px rgba(5, 150, 105, 0.36); transform: translateY(-1px); }
.checkout-btn:disabled { background: #cbd5c9; color: #6b7d74; box-shadow: none; cursor: not-allowed; transform: none; }
.toast-messages { padding: 10px 20px; background: white; }
.error-box { background: #fef2f2; color: #dc2626; padding: 10px; border-radius: 8px; font-size: 13px; border: 1px solid #fecaca; }
.success-box { background: #ecfdf5; color: #15803d; padding: 10px; border-radius: 8px; font-size: 13px; border: 1px solid #bbf0d3; }
.empty-cart-msg { text-align: center; color: #94a3b8; font-style: italic; padding: 40px 20px; }

/* ---------- Footer ---------- */
.footer {
  background-color: var(--forest-950);
  padding: 48px 20px 30px;
  font-family: 'Inter', sans-serif;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}
.footer-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  gap: 28px;
}
.footer-column { display: flex; flex-direction: column; gap: 12px; }
.footer-column h3 { font-size: 15px; color: #eafbf2; margin-bottom: 5px; font-weight: 700; font-family: 'Manrope', sans-serif; }
.footer-column a { text-decoration: none; color: #a9c9ba; font-size: 13.5px; }
.footer-column a:hover { color: #6ee7a8; }
.footer-bottom { text-align: center; margin-top: 40px; font-size: 12px; color: #6f8579; }
hr { border: 0; border-top: 1px solid rgba(255, 255, 255, 0.08); margin: 34px 0; }

/* =========================================================================
   RESPONSIV (Planshet va Telefon) MOSLASHUV
   ========================================================================= */
@media (max-width: 900px) {
  .navbar-inner { padding: 14px 16px; }
  .orders-hero-inner { padding: 34px 16px 30px; }
  .section { padding: 30px 16px; }
  .hero-text h1 { font-size: 26px; }
  .stats-row { gap: 12px; }
  .stat { padding: 12px 16px; min-width: auto; flex: 1 1 30%; }
  .product-grid { grid-template-columns: repeat(auto-fill, minmax(170px, 1fr)); gap: 14px; }
  .product-image { height: 170px; }
  .cart-sidebar { width: 100%; }
}

@media (max-width: 640px) {
  .navbar-inner { flex-direction: column; align-items: stretch; gap: 10px; }
  .brand { justify-content: center; }
  .nav-tabs, .nav-icons {
    flex-wrap: nowrap;
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 2px;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .nav-tabs::-webkit-scrollbar, .nav-icons::-webkit-scrollbar { display: none; }

  .orders-hero-inner { padding: 26px 16px 24px; }
  .hero-text h1 { font-size: 21px; }
  .hero-text p { font-size: 13.5px; }
  .stats-row { gap: 8px; }
  .stat strong { font-size: 18px; }

  .section { padding: 24px 14px; }
  .section-title { font-size: 18px; }

  .product-grid { grid-template-columns: repeat(2, 1fr); gap: 10px; }
  .product-image { height: 130px; }
  .product-body { padding: 12px; }
  .card-footer-actions { flex-direction: column; align-items: stretch; }
  .qty-selector { align-self: center; }

  .order-card, .debt-card { padding: 16px; }
  .order-card-amounts, .debt-card-body { grid-template-columns: repeat(2, 1fr); }

  .footer-container { gap: 26px; }
  .footer-column { flex: 1 1 45%; }
}

@media (max-width: 420px) {
  .product-grid { grid-template-columns: 1fr 1fr; gap: 8px; }
  .hero-text h1 { font-size: 19px; }
  .btn { padding: 8px 12px; font-size: 12.5px; }
  .order-card-amounts, .debt-card-body { grid-template-columns: 1fr; }
  .footer-column { flex: 1 1 100%; }
  .pay-input-group input,
  .qty-input { font-size: 16px; } /* iOS'da avtomatik zoom bo'lmasligi uchun */
}
</style>