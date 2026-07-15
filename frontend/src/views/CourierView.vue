<template>
  <div class="dashboard-wrapper">
    <aside class="sidebar-menu">
      <div class="sidebar-brand">
        <span class="logo-icon"><i class="ri-truck-line"></i></span>
        <h3>Top-Savdo B2B</h3>
      </div>
      <div class="user-brief-info">
        <div class="user-avatar"><i class="ri-motorbike-line"></i></div>
        <div class="user-meta">
          <span class="user-role">Kuryer Boshqaruv Paneli</span>
        </div>
      </div>

      <div class="availability-card">
        <div class="availability-text">
          <span class="a-label">Ish holati</span>
          <span
            class="a-value"
            :class="isAvailable ? 'text-success' : 'text-danger'"
          >
            {{ isAvailable ? "Bo'sh (Tayyor)" : "Band" }}
          </span>
        </div>
        <label class="switch">
          <input
            type="checkbox"
            v-model="isAvailable"
            @change="toggleAvailability"
            :disabled="togglingAvailability"
          />
          <span class="slider"></span>
        </label>
      </div>

      <nav class="nav-links">
        <button
          :class="{ active: activeTab === 'available' }"
          @click="activeTab = 'available'"
        >
          <i class="ri-file-list-3-line"></i> Yangi Buyurtmalar
          <span v-if="availableOrders.length" class="badge-count">{{
            availableOrders.length
          }}</span>
        </button>
        <button
          :class="{ active: activeTab === 'mydeliveries' }"
          @click="activeTab = 'mydeliveries'"
        >
          <i class="ri-truck-line"></i> Mening Yuklarim
        </button>
        <button
          :class="{ active: activeTab === 'history' }"
          @click="activeTab = 'history'"
        >
          <i class="ri-history-line"></i> Yetkazilganlar Tarixi
        </button>
      </nav>
    </aside>

    <div class="main-content-area">
      <header class="main-header">
        <div class="page-title">
          <h2>
            <span v-if="activeTab === 'available'"
              >Diler So'rov Yuborgan Buyurtmalar</span
            >
            <span v-if="activeTab === 'mydeliveries'"
              >Sizga Biriktirilgan Yuklar</span
            >
            <span v-if="activeTab === 'history'"
              >Yetkazib Berilgan Buyurtmalar Tarixi</span
            >
          </h2>
        </div>
        <div class="header-actions">
          <button @click="refreshAll" class="refresh-btn">
            <i class="ri-refresh-line"></i> Yangilash
          </button>
          <button @click="handleLogout" class="logout-btn">
            <i class="ri-logout-box-r-line"></i> Chiqish
          </button>
        </div>
      </header>

      <div class="content-body">
        <!-- YANGI BUYURTMALAR (hali hech kim olmagan) -->
        <div
          v-if="activeTab === 'available'"
          class="tab-content animate-fade-in"
        >
          <div v-if="loadingAvailable" class="no-data">
            Buyurtmalar yuklanmoqda...
          </div>
          <div v-else-if="availableOrders.length === 0" class="no-data">
            Hozircha diler tomonidan so'rov yuborilgan buyurtma yo'q.
          </div>
          <div v-else class="cards-grid">
            <div
              v-for="order in availableOrders"
              :key="order.id"
              class="order-card"
            >
              <div class="order-card-head">
                <span class="order-id">Buyurtma #{{ order.id }}</span>
                <span class="status-pill courier_requested">{{
                  order.status_display
                }}</span>
              </div>
              <div class="order-card-body">
                <p>
                  <i class="ri-store-2-line"></i>
                  <strong>{{ order.dealer_company_name }}</strong> firmasidan
                </p>
                <p>
                  <i class="ri-map-pin-line"></i>
                  {{ order.client_store_name }} —
                  {{ order.client_address || "Manzil ko'rsatilmagan" }}
                </p>
                <p>
                  <i class="ri-phone-line"></i>
                  {{ order.client_phone || "Tel ko'rsatilmagan" }}
                </p>
                <p class="order-amount">
                  <i class="ri-money-dollar-circle-line"></i>
                  {{ formatPrice(order.total_amount) }} so'm
                </p>
              </div>
              <button
                class="action-btn accept-btn full-width"
                @click="acceptDelivery(order.id)"
                :disabled="acceptingId === order.id"
              >
                <i class="ri-check-double-line"></i>
                {{
                  acceptingId === order.id
                    ? "Qabul qilinmoqda..."
                    : "Buyurtmani Qabul Qilish"
                }}
              </button>
            </div>
          </div>
        </div>

        <!-- MENING YUKLARIM (biriktirilgan, hali yetkazilmagan) -->
        <div
          v-if="activeTab === 'mydeliveries'"
          class="tab-content animate-fade-in"
        >
          <div v-if="activeDeliveries.length === 0" class="no-data">
            Sizga hozircha faol yuk biriktirilmagan.
          </div>
          <div v-else class="table-container">
            <table class="custom-data-table">
              <thead>
                <tr>
                  <th>Buyurtma ID</th>
                  <th>Diler</th>
                  <th>Magazin / Manzil</th>
                  <th>Jami Summa</th>
                  <th>Status</th>
                  <th>Harakat</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in activeDeliveries" :key="order.id">
                  <td>#{{ order.id }}</td>
                  <td>
                    <strong>{{ order.dealer_company_name }}</strong>
                    <p class="c-phone">
                      {{ order.dealer_phone || "Tel ko'rsatilmagan" }}
                    </p>
                  </td>
                  <td>
                    <strong>{{ order.client_store_name }}</strong>
                    <p class="c-phone">
                      {{ order.client_address || "Manzil ko'rsatilmagan" }}
                    </p>
                    <p class="c-phone">
                      {{ order.client_phone || "" }}
                    </p>
                  </td>
                  <td>{{ formatPrice(order.total_amount) }} so'm</td>
                  <td>
                    <span
                      class="status-pill"
                      :class="order.status.toLowerCase()"
                    >
                      {{ order.status_display || order.status }}
                    </span>
                  </td>
                  <td>
                    <span
                      v-if="order.status === 'COURIER_REQUESTED'"
                      class="status-text text-warning animate-pulse"
                    >
                      ⏳ Diler yukni topshirishini kutmoqda...
                    </span>
                    <button
                      v-if="order.status === 'SHIPPED'"
                      @click="deliverOrder(order.id)"
                      class="action-btn ship-btn"
                      :disabled="deliveringId === order.id"
                    >
                      <i class="ri-checkbox-circle-line"></i>
                      {{
                        deliveringId === order.id
                          ? "Yuborilmoqda..."
                          : "Yetkazib Berdim"
                      }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- TARIX (DELIVERED / CANCELED) -->
        <div v-if="activeTab === 'history'" class="tab-content animate-fade-in">
          <div v-if="historyDeliveries.length === 0" class="no-data">
            Hali yetkazib berilgan buyurtmalaringiz yo'q.
          </div>
          <div v-else class="table-container">
            <table class="custom-data-table">
              <thead>
                <tr>
                  <th>Buyurtma ID</th>
                  <th>Diler</th>
                  <th>Magazin</th>
                  <th>Sana</th>
                  <th>Jami Summa</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in historyDeliveries" :key="order.id">
                  <td>#{{ order.id }}</td>
                  <td>{{ order.dealer_company_name }}</td>
                  <td>{{ order.client_store_name }}</td>
                  <td>{{ formatDate(order.created_at) }}</td>
                  <td>{{ formatPrice(order.total_amount) }} so'm</td>
                  <td>
                    <span
                      class="status-pill"
                      :class="order.status.toLowerCase()"
                    >
                      {{ order.status_display || order.status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";

export default {
  setup() {
    const router = useRouter();

    const activeTab = ref("available");

    const isAvailable = ref(true);
    const togglingAvailability = ref(false);

    const availableOrders = ref([]);
    const loadingAvailable = ref(false);
    const acceptingId = ref(null);

    const myOrders = ref([]); // barcha kuryerga tegishli buyurtmalar
    const deliveringId = ref(null);

    // Faol yuklar: kuryerga biriktirilgan, hali DELIVERED/CANCELED bo'lmagan
    const activeDeliveries = computed(() =>
      myOrders.value.filter((o) =>
        ["COURIER_REQUESTED", "SHIPPED"].includes(o.status),
      ),
    );

    // Tarix: yakunlangan buyurtmalar
    const historyDeliveries = computed(() =>
      myOrders.value.filter((o) =>
        ["DELIVERED", "CANCELED"].includes(o.status),
      ),
    );

    // 1. Kuryerning o'z profilini (bo'sh/band holatini) yuklash
    const fetchCourierProfile = async () => {
      try {
        const response = await api.get("/courier/me/");
        isAvailable.value = response.data.is_available;
      } catch (error) {
        console.error("Kuryer profilini yuklashda xatolik:", error);
      }
    };

    // 2. Hali hech kim olmagan, diler so'rov yuborgan buyurtmalarni yuklash
    const fetchAvailableOrders = async () => {
      loadingAvailable.value = true;
      try {
        const response = await api.get("orders/available_deliveries/");
        availableOrders.value = response.data || [];
      } catch (error) {
        console.error("Yangi buyurtmalarni yuklashda xatolik:", error);
      } finally {
        loadingAvailable.value = false;
      }
    };

    // 3. Kuryerga tegishli barcha buyurtmalarni yuklash (faol + tarix)
    const fetchMyOrders = async () => {
      try {
        const response = await api.get("orders/");
        myOrders.value = response.data || [];
      } catch (error) {
        console.error("Yuklarni yuklashda xatolik:", error);
      }
    };

    const refreshAll = () => {
      fetchAvailableOrders();
      fetchMyOrders();
    };

    // 4. Bo'sh/band holatini almashtirish
    const toggleAvailability = async () => {
      togglingAvailability.value = true;
      try {
        await api.patch("/courier/me/", { is_available: isAvailable.value });
      } catch (error) {
        alert("Holatni yangilashda xatolik yuz berdi.");
        isAvailable.value = !isAvailable.value; // orqaga qaytaramiz
      } finally {
        togglingAvailability.value = false;
      }
    };

    // 5. Buyurtmani o'ziga biriktirib olish
    const acceptDelivery = async (orderId) => {
      acceptingId.value = orderId;
      try {
        const response = await api.post(`orders/${orderId}/accept-delivery/`);
        alert(response.data?.message || "Buyurtma muvaffaqiyatli qabul qilindi!");
        await Promise.all([fetchAvailableOrders(), fetchMyOrders()]);
        activeTab.value = "mydeliveries";
      } catch (error) {
        const msg =
          error?.response?.data?.message ||
          "Buyurtmani qabul qilib bo'lmadi. Ehtimol, uni boshqa kuryer olib ulgurdi.";
        alert(msg);
        await fetchAvailableOrders();
      } finally {
        acceptingId.value = null;
      }
    };

    // 6. Yukni magazinchiga yetkazib berdim deb belgilash
    const deliverOrder = async (orderId) => {
      deliveringId.value = orderId;
      try {
        const response = await api.post(`orders/${orderId}/deliver/`);
        alert(response.data?.message || "Buyurtma muvaffaqiyatli yopildi!");
        await fetchMyOrders();
      } catch (error) {
        const msg =
          error?.response?.data?.message || "Amalni bajarib bo'lmadi!";
        alert(msg);
      } finally {
        deliveringId.value = null;
      }
    };

    const handleLogout = () => {
      localStorage.clear();
      router.push("/login");
    };

    const formatPrice = (val) => parseFloat(val || 0).toLocaleString();
    const formatDate = (dateStr) =>
      new Date(dateStr).toLocaleDateString("uz-UZ");

    onMounted(() => {
      fetchCourierProfile();
      fetchAvailableOrders();
      fetchMyOrders();
    });

    return {
      activeTab,
      isAvailable,
      togglingAvailability,
      availableOrders,
      loadingAvailable,
      acceptingId,
      activeDeliveries,
      historyDeliveries,
      deliveringId,
      refreshAll,
      toggleAvailability,
      acceptDelivery,
      deliverOrder,
      handleLogout,
      formatPrice,
      formatDate,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ---------- Asosiy struktura (boshqa panellar bilan bir xil dizayn tizimi) ---------- */
.dashboard-wrapper {
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

  display: flex;
  min-height: 100vh;
  background-color: var(--paper);
  font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* ---------- Sidebar ---------- */
.sidebar-menu {
  width: 264px;
  min-width: 264px;
  background: linear-gradient(190deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  color: white;
  padding: 26px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 18px;
}
.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  color: #06170e;
  font-size: 17px;
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.32);
  flex-shrink: 0;
}
.sidebar-brand h3 {
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #eafbf2;
  margin: 0;
}

.user-brief-info {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 12px;
  border-radius: 12px;
}
.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: rgba(110, 231, 168, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #6ee7a8;
  flex-shrink: 0;
}
.user-role { font-size: 12.5px; font-weight: 600; color: #bcd9c8; }

/* ---------- Ish holati toggle karta ---------- */
.availability-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 14px;
  border-radius: 12px;
}
.availability-text { display: flex; flex-direction: column; gap: 4px; }
.a-label { font-size: 11.5px; color: #9db3a8; }
.a-value { font-size: 13.5px; font-weight: 700; }

/* Toggle switch */
.switch { position: relative; display: inline-block; width: 46px; height: 26px; flex-shrink: 0; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255, 255, 255, 0.25);
  transition: 0.3s;
  border-radius: 26px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 20px;
  width: 20px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}
.switch input:checked + .slider { background: linear-gradient(to right, var(--accent-500), var(--accent-600)); }
.switch input:checked + .slider:before { transform: translateX(20px); }

/* ---------- Nav ---------- */
.nav-links { display: flex; flex-direction: column; gap: 6px; }
.nav-links button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: none;
  border: none;
  color: #bcd9c8;
  padding: 12px 14px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  text-align: left;
  transition: all 0.2s ease;
}
.nav-links button:hover { background: rgba(255, 255, 255, 0.07); color: #fff; }
.nav-links button.active {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3);
}
.badge-count {
  margin-left: auto;
  background: #dc2626;
  color: white;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
}

/* ---------- Asosiy hudud ---------- */
.main-content-area { flex: 1; padding: 30px 36px; min-width: 0; }
.main-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 26px; flex-wrap: wrap; gap: 12px; }
.page-title h2 { font-family: 'Manrope', sans-serif; font-size: 20px; font-weight: 800; color: var(--ink-900); margin: 0; }
.header-actions { display: flex; gap: 10px; }
.refresh-btn {
  background: rgba(34, 197, 94, 0.1);
  color: var(--forest-700);
  border: none;
  padding: 10px 16px;
  border-radius: 9px;
  font-weight: 700;
  font-family: inherit;
  font-size: 13.5px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.refresh-btn:hover { background: rgba(34, 197, 94, 0.18); }
.logout-btn {
  background: transparent;
  color: var(--ink-900);
  border: 1px solid var(--line);
  padding: 10px 18px;
  border-radius: 9px;
  cursor: pointer;
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.2s ease;
}
.logout-btn:hover { border-color: #fca5a5; color: #dc2626; background: #fef2f2; }

/* ---------- Kartochkalar (yangi buyurtmalar) ---------- */
.cards-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 18px; }
.order-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.order-card:hover { transform: translateY(-3px); box-shadow: 0 12px 26px rgba(10, 47, 29, 0.08); }
.order-card-head { display: flex; justify-content: space-between; align-items: center; }
.order-id { font-weight: 700; color: var(--ink-900); font-size: 14.5px; }
.order-card-body p { display: flex; align-items: center; gap: 8px; font-size: 13.5px; color: var(--ink-600); margin-bottom: 6px; }
.order-card-body p i { color: var(--forest-700); }
.order-amount { font-weight: 800 !important; color: var(--forest-700) !important; font-family: 'Manrope', sans-serif; }
.full-width { width: 100%; justify-content: center; }

/* ---------- Jadval ---------- */
.table-container {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--line);
  box-shadow: 0 4px 16px rgba(10, 47, 29, 0.04);
}
.custom-data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px; }
.custom-data-table th {
  background: var(--paper);
  padding: 14px 18px;
  color: var(--ink-600);
  border-bottom: 1px solid var(--line);
  font-weight: 700;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}
.custom-data-table td { padding: 14px 18px; border-bottom: 1px solid #f1f4f2; vertical-align: middle; color: var(--ink-900); }
.custom-data-table tr:hover { background: #fafcfa; }
.c-phone { font-size: 12px; color: var(--ink-600); margin-top: 2px; }

/* ---------- Amal tugmalari ---------- */
.action-btn {
  border: none;
  padding: 9px 15px;
  border-radius: 9px;
  font-weight: 700;
  font-family: inherit;
  font-size: 12.5px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.action-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.accept-btn { background: linear-gradient(to right, var(--accent-500), var(--accent-600)); color: #06170e; box-shadow: 0 6px 16px rgba(5, 150, 105, 0.28); }
.accept-btn:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(5, 150, 105, 0.36); }
.ship-btn { background: #0369a1; color: white; }
.ship-btn:hover:not(:disabled) { background: #075985; }

/* ---------- Status belgilari ---------- */
.status-pill { padding: 4px 11px; border-radius: 20px; font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.3px; display: inline-block; }
.status-pill.delivered, .status-pill.accepted { background: #e2fbe8; color: #15803d; }
.status-pill.cancelled, .status-pill.canceled { background: #fee2e2; color: #b91c1c; }
.status-pill.pending { background: #fef3c7; color: #b45309; }
.status-pill.courier_requested, .status-pill.shipped { background: #e0f2fe; color: #0369a1; }

.status-text { font-size: 12.5px; font-weight: 700; }
.text-success { color: var(--accent-600) !important; }
.text-danger { color: #dc2626 !important; }
.text-warning { color: #ea580c !important; }

.no-data {
  text-align: center;
  padding: 46px 0;
  color: #9aab9f;
  font-style: italic;
  background: white;
  border-radius: 16px;
  border: 1px solid var(--line);
}

.animate-fade-in { animation: fadeIn 0.3s ease; }
.animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* =========================================================================
   RESPONSIV (Planshet va Telefon) MOSLASHUV
   ========================================================================= */
@media (max-width: 900px) {
  .dashboard-wrapper { flex-direction: column; }
  .sidebar-menu {
    width: 100%;
    min-width: 100%;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    padding: 14px 16px;
    gap: 12px;
    position: sticky;
    top: 0;
    z-index: 50;
  }
  .sidebar-brand { flex: 1 1 auto; border-bottom: none; padding-bottom: 0; }
  .user-brief-info { flex: 1 1 auto; padding: 8px 10px; }
  .availability-card { flex: 1 1 100%; order: 3; }
  .nav-links {
    flex-direction: row;
    flex-wrap: nowrap;
    overflow-x: auto;
    width: 100%;
    order: 4;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 4px;
    scrollbar-width: none;
  }
  .nav-links::-webkit-scrollbar { display: none; }
  .nav-links button { white-space: nowrap; flex-shrink: 0; }
  .badge-count { margin-left: 6px; }
  .main-content-area { padding: 18px 14px; }
  .main-header { flex-direction: column; align-items: flex-start; gap: 12px; }
  .page-title h2 { font-size: 18px; }
  .header-actions { width: 100%; }
  .header-actions button { flex: 1; justify-content: center; }
  .cards-grid { grid-template-columns: 1fr; }
  .table-container { overflow-x: auto; }
  .custom-data-table { min-width: 640px; }
}

@media (max-width: 480px) {
  .sidebar-brand h3 { font-size: 15px; }
  .page-title h2 { font-size: 16px; }
  .order-card { padding: 14px; }
  .order-card-body p { font-size: 13px; }
  .refresh-btn, .logout-btn { padding: 9px 12px; font-size: 13px; }
}
</style>