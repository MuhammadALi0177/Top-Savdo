<template>
  <div class="admin-layout">
    <!-- 🟢 Mobil/planshet uchun tepa panel: hamburger tugma va brend -->
    <header class="mobile-topbar">
      <button class="hamburger-btn" @click="toggleSidebar" title="Menyu">
        <i class="ri-menu-line"></i>
      </button>
      <div class="mobile-brand">
        <span class="brand-icon"><i class="ri-settings-4-line"></i></span>
        <h2>Top-Savdo B2B</h2>
      </div>
    </header>

    <!-- 🟢 Sidebar ochiq bo'lganda orqa fonni qorong'ilashtiruvchi qatlam (faqat mobil/planshet) -->
    <div
      class="sidebar-overlay"
      v-if="isSidebarOpen"
      @click="closeSidebar"
    ></div>

    <aside class="sidebar" :class="{ open: isSidebarOpen }">
      <div class="sidebar-brand">
        <span class="brand-icon"><i class="ri-settings-4-line"></i></span>
        <div>
          <h2>Top-Savdo B2B</h2>
          <p>Super Admin Paneli</p>
        </div>
      </div>

      <div class="menu-section">
        <label>ASOSIY</label>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'boshqaruv' }"
          @click="currentTab = 'boshqaruv'; closeSidebar()"
        >
          <span class="icon"><i class="ri-dashboard-3-line"></i></span>
          Boshqaruv
        </button>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'users' }"
          @click="currentTab = 'users'; closeSidebar()"
        >
          <span class="icon"><i class="ri-team-line"></i></span>
          Foydalanuvchilar
        </button>
      </div>

      <div class="menu-section">
        <label>SAVDO</label>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'mahsulotlar' }"
          @click="currentTab = 'mahsulotlar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-box-3-line"></i></span> Mahsulotlar
        </button>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'buyurtmalar' }"
          @click="currentTab = 'buyurtmalar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-bill-line"></i></span> Buyurtmalar
        </button>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'kategoriyalar' }"
          @click="currentTab = 'kategoriyalar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-apps-2-line"></i></span> Kategoriyalar
        </button>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'fermalar' }"
          @click="currentTab = 'fermalar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-bank-line"></i></span> Fermalar
        </button>
      </div>

      <div class="menu-section">
        <label>LOGISTIKA</label>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'kuryerlar' }"
          @click="currentTab = 'kuryerlar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-motorbike-line"></i></span> Kuryerlar
        </button>
      </div>

      <div class="menu-section">
        <label>TIZIM</label>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'tokens' }"
          @click="currentTab = 'tokens'; closeSidebar()"
        >
          <span class="icon"><i class="ri-key-2-line"></i></span> Access tokens
        </button>
        <button
          class="menu-item"
          :class="{ active: currentTab === 'loglar' }"
          @click="currentTab = 'loglar'; closeSidebar()"
        >
          <span class="icon"><i class="ri-file-list-3-line"></i></span> Loglar
        </button>
      </div>

      <div class="sidebar-footer">
        <div class="admin-profile">
          <div class="avatar">AA</div>
          <div class="info">
            <h4>Azizxon Admin</h4>
            <p>admin@gmail.com</p>
          </div>
        </div>
        <button
          @click="handleLogout"
          class="sidebar-logout-btn"
          title="Tizimdan chiqish"
        >
          <i class="ri-logout-box-r-line"></i> Chiqish
        </button>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <h2 class="page-title">{{ getTabTitle() }}</h2>
        <div class="header-right">
          <button v-if="currentTab === 'kategoriyalar'" @click="openCatModal" class="add-cat-btn">
            <i class="ri-add-line"></i> <span>Yangi Kategoriya</span>
          </button>
          <button class="icon-btn" title="Bildirishnomalar">
            <i class="ri-notification-3-line"></i>
          </button>
          <button class="icon-btn" title="Sozlamalar">
            <i class="ri-settings-3-line"></i>
          </button>
        </div>
      </header>

      <div class="tab-content-wrapper">
        <div v-if="currentTab === 'boshqaruv'" class="tab-pane">
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-info">
                <h3>{{ users.length }}</h3>
                <p>Jami foydalanuvchilar</p>
              </div>
              <div class="stat-icon u-icon"><i class="ri-group-line"></i></div>
            </div>
            <div class="stat-card">
              <div class="stat-info">
                <h3>{{ countByRole("DEALER") }}</h3>
                <p>Dilerlar</p>
              </div>
              <div class="stat-icon d-icon">
                <i class="ri-store-2-line"></i>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-info">
                <h3>{{ countByRole("CLIENT") }}</h3>
                <p>Mijozlar (Do'konlar)</p>
              </div>
              <div class="stat-icon c-icon"><i class="ri-user-line"></i></div>
            </div>
            <div class="stat-card">
              <div class="stat-info">
                <h3>{{ countByRole("COURIER") }}</h3>
                <p>Kuryerlar</p>
              </div>
              <div class="stat-icon k-icon">
                <i class="ri-motorbike-line"></i>
              </div>
            </div>
          </div>

          <div class="recent-orders-box table-card">
            <h3><i class="ri-time-line"></i> So'nggi buyurtmalar</h3>
            <div v-if="orders.length === 0" class="no-data">
              Hozircha buyurtmalar mavjud emas.
            </div>
            <table v-else class="modern-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Mijoz</th>
                  <th>Summa</th>
                  <th>Holati</th>
                  <th>Sana</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in orders.slice(0, 5)" :key="order.id">
                  <td>#{{ order.id }}</td>
                  <td>
                    {{ order.client_store_name || order.client_phone || "Noma'lum do'kon" }}
                  </td>
                  <td>
                    {{ parseFloat(order.total_amount || 0).toLocaleString() }}
                    so'm
                  </td>
                  <td>
                    <span
                      :class="
                        order.status === 'DELIVERED'
                          ? 'status-done'
                          : 'status-wait'
                      "
                    >
                      {{ order.status || "Kutilmoqda" }}
                    </span>
                  </td>
                  <td>
                    {{
                      order.created_at ? order.created_at.split("T")[0] : "—"
                    }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="currentTab === 'users'" class="tab-pane table-card">
          <div v-if="loading" class="no-data">
            Foydalanuvchilar yuklanmoqda...
          </div>
          <div v-else-if="errorMessage" class="error-box">
            {{ errorMessage }}
          </div>
          <div v-else-if="users.length === 0" class="no-data">
            Foydalanuvchilar mavjud emas.
          </div>
          <table v-else class="modern-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Ism (Login)</th>
                <th>Telefon</th>
                <th>Rol</th>
                <th>Holati</th>
                <th>Amallar</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>#{{ user.id }}</td>
                <td class="username-cell">{{ user.username }}</td>
                <td>{{ user.phone_number || "—" }}</td>
                <td>
                  <span
                    class="role-tag"
                    :class="user.role ? user.role.toLowerCase() : 'client'"
                    >{{ user.role || "CLIENT" }}</span
                  >
                </td>
                <td>
                  <span
                    class="status-tag"
                    :class="{ active: user.is_active }"
                    >{{ user.is_active ? "Faol" : "Bloklangan" }}</span
                  >
                </td>
                <td>
                  <button
                    @click="deleteUser(user.id, user.username)"
                    class="delete-btn"
                  >
                    <i class="ri-delete-bin-7-line"></i> O'chirish
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'mahsulotlar'" class="tab-pane table-card">
          <div class="section-header">
            <h3><i class="ri-box-3-line"></i> Tizimdagi barcha mahsulotlar nazorati</h3>
          </div>
          <div v-if="loading" class="no-data">Mahsulotlar yuklanmoqda...</div>
          <div v-else-if="products.length === 0" class="no-data">
            Hozircha tizimda hech qanday mahsulot mavjud emas.
          </div>
          <table v-else class="modern-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Rasm</th>
                <th>Mahsulot Nomi</th>
                <th>Kategoriya</th>
                <th>Narxi</th>
                <th>Ombor</th>
                <th>Holati</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id">
                <td>#{{ product.id }}</td>
                <td>
                  <img 
                    :src="product.main_image || product.image || 'https://via.placeholder.com/40'" 
                    alt="Rasm" 
                    style="width: 40px; height: 40px; object-fit: cover; border-radius: 6px;"
                  />
                </td>
                <td class="username-cell">{{ product.name }}</td>
                <td>{{ product.category_name || product.category || '—' }}</td>
                <td>{{ parseFloat(product.price || 0).toLocaleString() }} so'm</td>
                <td>
                  <span :class="product.stock > 0 ? 'status-done' : 'status-tag'">
                    {{ product.stock }} ta
                  </span>
                </td>
                <td>
                  <span class="status-tag" :class="{ active: product.is_active !== false }">
                    {{ product.is_active !== false ? "Sotuvda" : "Sotuvda emas" }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'buyurtmalar'" class="tab-pane table-card">
          <h3>
            <i class="ri-bill-line"></i> Jami buyurtmalar ro'yxati va holati
          </h3>
          <div v-if="orders.length === 0" class="no-data">
            Hozircha buyurtmalar ro'yxati bo'sh.
          </div>
          <table v-else class="modern-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Mijoz</th>
                <th>Summa</th>
                <th>Qarz (Nasiya)</th>
                <th>Holati</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>#{{ order.id }}</td>
                <td>{{ order.client_store_name || order.client_phone || "Noma'lum do'kon" }}</td>
                <td>
                  {{ parseFloat(order.total_amount || 0).toLocaleString() }} so'm
                </td>
                <td style="color: #c2410c; font-weight: 600;">
                  {{ parseFloat(order.debt_amount || 0).toLocaleString() }} so'm
                </td>
                <td>
                  <span :class="order.status === 'DELIVERED' ? 'status-done' : 'status-wait'">
                    {{ order.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'kategoriyalar'" class="tab-pane table-card">
  <h3><i class="ri-apps-2-line"></i> Mahsulot Kategoriyalari</h3>
  
  <div v-if="loading" class="no-data">Kategoriyalar yuklanmoqda...</div>
  <div v-else-if="categories.length === 0" class="no-data">Kategoriyalar ro'yxati bo'sh.</div>
  
  <table v-else class="modern-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Kategoriya Nomi</th>
        <th>Slug (URL Manzil)</th>
        <th>Harakatlar</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="cat in categories" :key="cat.id">
        <td>#{{ cat.id }}</td>
        <td class="username-cell">{{ cat.name }}</td>
        <td><code>{{ cat.slug }}</code></td>
        <td>
          <button @click="deleteCategory(cat.id, cat.name)" class="delete-btn">
            <i class="ri-delete-bin-7-line"></i> O'chirish
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</div>

        <div v-if="currentTab === 'fermalar'" class="tab-pane table-card">
          <div class="section-header">
            <h3><i class="ri-bank-line"></i> Hamkor Korxonalar / Fermalar</h3>
          </div>

          <div v-if="loading" class="no-data">Korxonalar yuklanmoqda...</div>
          <div v-else-if="fermalar.length === 0" class="no-data">
            Tizimda birorta ham korxona yoki diler ro'yxatdan o'tmagan.
          </div>

          <table v-else class="modern-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Firma / Korxona nomi</th>
                <th>Mas'ul Diler (User)</th>
                <th>Telefon</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ferma in fermalar" :key="ferma.id">
                <td>#{{ ferma.id }}</td>
                <td>
                  <strong class="username-cell">
                    {{ 
                      ferma.company_name || 
                      ferma.dealer_profile?.company_name || 
                      ferma.username || 
                      ferma.phone_number ||
                      'Yangi Diler Korxonasi'
                    }}
                  </strong>
                </td>
                <td>{{ ferma.phone_number || ferma.username || '—' }}</td>
                <td>{{ ferma.phone_number || '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'kuryerlar'" class="tab-pane table-card">
          <div class="section-header">
            <h3><i class="ri-motorbike-line"></i> Kuryerlar ro'yxati</h3>
          </div>

          <div v-if="loading" class="no-data">Kuryerlar yuklanmoqda...</div>
          <div v-else-if="kuryerlar.length === 0" class="no-data">
            Tizimda hali birorta ham kuryer ro'yxatdan o'tmagan.
          </div>

          <table v-else class="modern-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Ism (Login)</th>
                <th>Telefon</th>
                <th>Holati</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="kuryer in kuryerlar" :key="kuryer.id">
                <td>#{{ kuryer.id }}</td>
                <td class="username-cell">{{ kuryer.username || "—" }}</td>
                <td>{{ kuryer.phone_number || "—" }}</td>
                <td>
                  <span class="status-tag" :class="{ active: kuryer.is_active }">
                    {{ kuryer.is_active ? "Faol" : "Bloklangan" }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div
          v-if="['tokens', 'loglar'].includes(currentTab)"
          class="tab-pane table-card"
        >
          <h3>Ma'lumotlar mavjud emas</h3>
          <p class="empty-text">
            Ushbu bo'limni dasturga ulash jarayoni ketmoqda...
          </p>
        </div>
      </div>
    </main>

    <div class="modal-overlay" v-if="isCatModalOpen" @click.self="isCatModalOpen = false">
  <div class="modal-content">
    <h3>Yangi Kategoriya Yaratish</h3>
    <form @submit.prevent="submitCategory">
      <div class="form-group">
        <label>Kategoriya nomi:</label>
        <input type="text" v-model="newCategory.name" required />
      </div>
      <div class="form-group">
        <label>Slug:</label>
        <input type="text" v-model="newCategory.slug" required />
      </div>
      <div class="modal-actions">
        <button type="button" @click="isCatModalOpen = false" class="cancel-btn">Bekor</button>
        <button type="submit" :disabled="submittingCat" class="save-btn">
          {{ submittingCat ? 'Saqlanmoqda...' : 'Yaratish' }}
        </button>
      </div>
    </form>
  </div>
</div>

  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";

export default {
  setup() {
    const currentTab = ref("boshqaruv");
    const users = ref([]);
    const fermalar = ref([]);
    const kuryerlar = ref([]);
    const orders = ref([]);
    const products = ref([]);
    const categories = ref([]);
    const loading = ref(false);
    const errorMessage = ref("");
    const router = useRouter();

    const isCatModalOpen = ref(false);
    const submittingCat = ref(false);
    const newCategory = ref({ name: "", slug: ""});

    // 🟢 Mobil/planshet uchun: yon menyu (sidebar) ochiq/yopiqligini boshqarish
    const isSidebarOpen = ref(false);
    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value;
    };
    const closeSidebar = () => {
      isSidebarOpen.value = false;
    };

    const fetchUsers = async () => {
      loading.value = true;
      errorMessage.value = "";
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("admin/users/", {
          headers: { Authorization: `Token ${token}` },
        });
        users.value = response.data;
      } catch (error) {
        errorMessage.value = "Ma'lumotlarni yuklashda xatolik yuz berdi.";
      } finally {
        loading.value = false;
      }
    };

    // 🟢 Admin foydalanuvchini o'chirish
    const deleteUser = async (id, username) => {
      if (!confirm(`"${username}" foydalanuvchisini o'chirishni tasdiqlaysizmi?`)) return;

      const token = localStorage.getItem("token");
      try {
        await api.delete(`admin/users/${id}/`, {
          headers: { Authorization: `Token ${token}` },
        });

        // O'chirgandan so'ng ro'yxatni yangilash
        await fetchUsers();
        loadKuryerlar();
        fallbackFermalar();
      } catch (error) {
        console.error("Foydalanuvchini o'chirishda xato:", error);
        const msg =
          error.response && error.response.data && error.response.data.error
            ? error.response.data.error
            : "Foydalanuvchini o'chirib bo'lmadi.";
        alert(msg);
      }
    };

    const fetchProducts = async () => {
  try {
    // ESKI: api.get('admin/products/')
    // YANGI:
    const response = await api.get('/products/'); 
    products.value = response.data;
  } catch (e) {
    console.error("Mahsulotlar yuklanmadi:", e);
  }
};

    // To'g'rilangan: Toza nisbiy URL
    const fetchCategories = async () => {
  try {
    // 🟢 URL: 'products/categories/' -> '/categories/' ga o'zgartirildi
    // baseURL ('api/v1') allaqachon api/index.js da qo'shilgan.
    const response = await api.get("/categories/"); 
    
    // Authorization headerini to'g'ridan-to'g'ri yozish shart emas, 
    // chunki api/index.js dagi interceptor buni avtomatik bajaradi.
    categories.value = response.data;
  } catch (e) {
    console.error("Kategoriyalarni yuklashda xato:", e);
    // Xatolikni konsolda ko'rish uchun:
    if (e.response) {
      console.log("Xato javobi:", e.response.data);
    }
  }
};

    // To'g'rilangan: Dilerlarni xatosiz olish va filtrlash
    const fetchFermalar = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("admin/dealerprofile/", {
          headers: { Authorization: `Token ${token}` },
        });
        if (response && response.data && response.data.length > 0) {
          fermalar.value = response.data;
        } else {
          fallbackFermalar();
        }
      } catch (error) {
        fallbackFermalar();
      }
    };

    // Kuryerlar ro'yxati: mavjud users ro'yxatidan COURIER rolidagilarni ajratib olamiz
    const loadKuryerlar = () => {
      if (users.value && users.value.length > 0) {
        kuryerlar.value = users.value.filter((u) => u.role === "COURIER");
      } else {
        kuryerlar.value = [];
      }
    };

    const fallbackFermalar = () => {
      if (users.value && users.value.length > 0) {
        fermalar.value = users.value.filter(
          (u) => u.role === "DEALER" || u.role === "DILLER"
        );
      } else {
        fermalar.value = [];
      }
    };

    const fetchOrders = async () => {
  try {
    // ESKI: api.get('admin/orders/')
    // YANGI:
    const response = await api.get('/orders/');
    orders.value = response.data;
  } catch (e) {
    console.error("Buyurtmalar yuklanmadi:", e);
  }
};

    // To'g'rilangan: URL takrorlanishi olib tashlandi, faqat bitta toza so'rov qoldirildi
const submitCategory = async () => {
  submittingCat.value = true;
  
  // Yuborilayotgan obyektni tayyorlaymiz
  const dataToSend = {
    name: newCategory.value.name,
    slug: newCategory.value.slug
  };
  
  // Agar rasm ham bo'lsa, uni alohida FormData bilan yuborish kerak bo'ladi. 
  // Hozircha faqat shu ikkitasini yuborib ko'ring:
  
  try {
    await api.post("/categories/", dataToSend); // '/categories/' ga POST
    isCatModalOpen.value = false;
    newCategory.value = { name: "", slug: "" };
    await fetchCategories();
  } catch (error) {
    console.error("400 Bad Request detallari:", error.response.data);
    alert("Kategoriya yaratishda xatolik: " + JSON.stringify(error.response.data));
  } finally {
    submittingCat.value = false;
  }
};

   // AdminView.vue ichidagi deleteCategory funksiyasi
const deleteCategory = async (id, name) => {
  if (!confirm(`"${name}" kategoriyasini o'chirishni tasdiqlaysizmi?`)) return;
  
  const token = localStorage.getItem("token");
  try {
    // 🟢 ESKI KOD: await api.delete(`products/categories/${id}/`, ...
    // 🟢 YANGI KOD: `/categories/${id}/` deb o'zgartiring
    await api.delete(`/categories/${id}/`, {
      headers: { Authorization: `Token ${token}` },
    });
    
    // O'chirgandan so'ng ro'yxatni yangilash
    await fetchCategories();
  } catch (error) {
    console.error("O'chirishda xato:", error);
    alert("Kategoriyani o'chirib bo'lmadi. Ehtimol, unga bog'liq mahsulotlar mavjud.");
  }
};

    const openCatModal = () => {
      newCategory.value = { name: "", slug: "", parent: null };
      isCatModalOpen.value = true;
    };

    const countByRole = (role) => {
      return users.value.filter((u) => u.role === role).length;
    };

    const getTabTitle = () => {
      const titles = {
        boshqaruv: "Boshqaruv paneli",
        users: "Foydalanuvchilar ro'yxati",
        mahsulotlar: "Mahsulotlar boshqaruvi",
        buyurtmalar: "Buyurtmalar tizimi",
        kategoriyalar: "Kategoriyalar",
        fermalar: "Fermalar ro'yxati",
        kuryerlar: "Kuryerlar logistikasi",
        tokens: "Access tokens",
        loglar: "Tizim loglari",
      };
      return titles[currentTab.value] || "Admin Panel";
    };

    const handleLogout = () => {
      localStorage.clear();
      router.push("/");
    };

    onMounted(async () => {
      await fetchUsers();
      loadKuryerlar();
      fetchFermalar();
      fetchOrders();
      fetchProducts();
      fetchCategories();
    });

    return {
      currentTab,
      users,
      fermalar,
      kuryerlar,
      orders,
      products,
      categories,
      loading,
      errorMessage,
      isCatModalOpen,
      submittingCat,
      newCategory,
      isSidebarOpen,
      toggleSidebar,
      closeSidebar,
      openCatModal,
      submitCategory,
      deleteCategory,
      deleteUser,
      countByRole,
      getTabTitle,
      handleLogout,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

.admin-layout {
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
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--ink-900);
}

/* ---------- Mobil tepa panel (desktopda yashirin) ---------- */
.mobile-topbar {
  display: none;
  align-items: center;
  gap: 12px;
  background: linear-gradient(160deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  padding: 14px 16px;
  position: sticky;
  top: 0;
  z-index: 25;
}
.hamburger-btn {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #fff;
  width: 38px;
  height: 38px;
  border-radius: 9px;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.2s ease;
}
.hamburger-btn:hover { background: rgba(255, 255, 255, 0.16); }
.mobile-brand { display: flex; align-items: center; gap: 10px; min-width: 0; }
.mobile-brand .brand-icon {
  color: #06170e;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 8px;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  flex-shrink: 0;
}
.mobile-brand h2 {
  font-family: 'Manrope', sans-serif;
  color: #eafbf2;
  font-size: 15px;
  margin: 0;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* ---------- Sidebar overlay ---------- */
.sidebar-overlay { display: none; }

/* ---------- Sidebar ---------- */
.sidebar {
  width: 264px;
  background: linear-gradient(190deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  color: #d5ecdf;
  display: flex;
  flex-direction: column;
  padding: 26px 0;
  position: fixed;
  height: 100vh;
  box-sizing: border-box;
  z-index: 10;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0 20px 22px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.brand-icon {
  font-size: 17px;
  color: #06170e;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  box-shadow: 0 6px 16px rgba(16, 185, 129, 0.32);
  flex-shrink: 0;
}
.sidebar-brand h2 {
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  margin: 0;
  font-weight: 700;
  color: #eafbf2;
}
.sidebar-brand p {
  font-size: 11px;
  margin: 3px 0 0 0;
  color: #6ee7a8;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  font-weight: 600;
}

.menu-section { margin-top: 22px; }
.menu-section label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: rgba(213, 236, 223, 0.4);
  padding: 0 20px 9px 20px;
}

.menu-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  background: transparent;
  border: none;
  border-left: 4px solid transparent;
  color: #bcd9c8;
  padding: 10px 20px;
  font-size: 13.5px;
  font-weight: 600;
  font-family: inherit;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  outline: none;
  -webkit-tap-highlight-color: transparent;
}
.menu-item .icon {
  font-size: 17px;
  width: 22px;
  display: inline-flex;
  align-items: center;
  opacity: 0.8;
}
.menu-item:hover { background: rgba(255, 255, 255, 0.06); color: #fff; }

.menu-item.active {
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  font-weight: 700;
  border-left: 4px solid var(--accent-500);
}
.menu-item.active .icon { opacity: 1; color: #6ee7a8; }

.menu-item .badge {
  margin-left: auto;
  background: var(--accent-500);
  color: #06170e;
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 10px;
  font-weight: 800;
}

.sidebar-footer {
  margin-top: auto;
  padding: 18px 20px 0 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}
.admin-profile { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
.avatar {
  background: linear-gradient(135deg, var(--accent-500), var(--accent-600));
  color: #06170e;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 13px;
  font-family: 'Manrope', sans-serif;
  flex-shrink: 0;
}
.info h4 { margin: 0; font-size: 13px; color: #eafbf2; font-weight: 700; }
.info p { margin: 2px 0 0 0; font-size: 11px; color: #9db3a8; }

.sidebar-logout-btn {
  width: 100%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #f87171;
  padding: 9px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 13px;
  font-family: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.sidebar-logout-btn:hover { background: #ef4444; color: white; border-color: #ef4444; }

/* ---------- Asosiy hudud ---------- */
.main-content {
  flex: 1;
  margin-left: 264px;
  padding: 30px;
  box-sizing: border-box;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 26px;
  background: white;
  padding: 16px 26px;
  border-radius: 14px;
  border: 1px solid var(--line);
}
.page-title { font-family: 'Manrope', sans-serif; margin: 0; font-size: 19px; font-weight: 800; color: var(--ink-900); }
.header-right { display: flex; gap: 10px; align-items: center; }
.icon-btn {
  background: var(--paper);
  border: 1px solid var(--line);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ink-600);
  transition: all 0.2s ease;
}
.icon-btn:hover { background: rgba(34, 197, 94, 0.1); color: var(--forest-700); border-color: var(--accent-500); }

/* ---------- Statistika kartochkalari ---------- */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 26px; }
.stat-card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--line);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 26px rgba(10, 47, 29, 0.08); }
.stat-info h3 { font-family: 'Manrope', sans-serif; margin: 0; font-size: 25px; font-weight: 800; color: var(--ink-900); }
.stat-info p { margin: 4px 0 0 0; color: var(--ink-600); font-size: 13px; }
.stat-icon { width: 46px; height: 46px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 20px; }
.u-icon { background: #e0f2fe; color: #0369a1; }
.d-icon { background: rgba(34, 197, 94, 0.12); color: var(--forest-700); }
.c-icon { background: #fef3c7; color: #92400e; }
.k-icon { background: #f3e8ff; color: #6b21a8; }

/* ---------- Jadval kartasi ---------- */
.table-card {
  background: white;
  padding: 24px;
  border-radius: 16px;
  border: 1px solid var(--line);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.table-card h3 {
  font-family: 'Manrope', sans-serif;
  font-size: 15.5px;
  font-weight: 700;
  color: var(--forest-900);
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 16px;
}
.table-card h3 i { color: var(--accent-600); margin-right: 2px; }
.section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }

.modern-table { width: 100%; min-width: 600px; border-collapse: collapse; text-align: left; }
.modern-table th {
  padding: 12px 14px;
  background: var(--paper);
  color: var(--ink-600);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  border-bottom: 1px solid var(--line);
}
.modern-table td { padding: 14px; border-bottom: 1px solid #f1f4f2; font-size: 13.5px; color: var(--ink-900); }
.modern-table tr:hover td { background: #fafcfa; }
.username-cell { font-weight: 700; color: var(--ink-900); }

/* ---------- Chip / status belgilari ---------- */
.role-tag { padding: 3px 9px; border-radius: 7px; font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.3px; }
.role-tag.admin { background: #e0f2fe; color: #0369a1; }
.role-tag.dealer { background: rgba(34, 197, 94, 0.12); color: var(--forest-700); }
.role-tag.client { background: #fef3c7; color: #92400e; }
.role-tag.courier { background: #f3e8ff; color: #6b21a8; }

.status-tag { padding: 3px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; background: #fee2e2; color: #991b1b; }
.status-tag.active { background: #dcfce7; color: #15803d; }

.status-wait { background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }
.status-done { background: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 6px; font-size: 11.5px; font-weight: 700; }

.error-box { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; padding: 13px 15px; border-radius: 10px; font-size: 13.5px; margin-bottom: 16px; }

.no-data {
  text-align: center;
  color: #9aab9f;
  padding: 44px 20px;
  font-style: italic;
  background: var(--paper);
  border-radius: 12px;
  border: 1px dashed var(--line);
  font-size: 14px;
}

.empty-text { color: var(--ink-600); font-size: 13.5px; }

code {
  background: var(--paper);
  padding: 2px 7px;
  border-radius: 5px;
  font-family: monospace;
  color: var(--forest-700);
  border: 1px solid var(--line);
}

/* ---------- Tugmalar ---------- */
.add-cat-btn {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  padding: 9px 17px;
  border-radius: 9px;
  font-weight: 700;
  font-family: inherit;
  font-size: 13px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.28);
  transition: all 0.2s ease;
}
.add-cat-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(5, 150, 105, 0.36); }

.delete-btn {
  background: transparent;
  border: 1px solid #fecaca;
  color: #ef4444;
  padding: 7px 13px;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  transition: all 0.2s ease;
}
.delete-btn:hover { background: #ef4444; color: white; }

/* ---------- Modal ---------- */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(7, 27, 16, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}
.modal-content {
  background: white;
  padding: 30px;
  border-radius: 18px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 24px 60px rgba(7, 27, 16, 0.3);
  box-sizing: border-box;
}
.modal-content h3 {
  font-family: 'Manrope', sans-serif;
  font-size: 17px;
  font-weight: 800;
  color: var(--ink-900);
  margin: 0 0 20px;
}
.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 7px; font-size: 13px; font-weight: 600; color: var(--forest-900); }
.form-group input, .select-input {
  width: 100%;
  padding: 11px 13px;
  border: 1.5px solid var(--line);
  border-radius: 9px;
  box-sizing: border-box;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  background: white;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-group input:focus, .select-input:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 26px; }
.cancel-btn {
  background: var(--paper);
  color: var(--ink-600);
  border: 1px solid var(--line);
  padding: 10px 17px;
  border-radius: 9px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 600;
  transition: all 0.2s ease;
}
.cancel-btn:hover { background: #eef2ef; }
.save-btn {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  padding: 10px 20px;
  border-radius: 9px;
  cursor: pointer;
  font-family: inherit;
  font-weight: 700;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.28);
  transition: all 0.2s ease;
}
.save-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(5, 150, 105, 0.36); }
.save-btn:disabled { opacity: 0.6; box-shadow: none; transform: none; cursor: not-allowed; }

/* =========================================================================
   RESPONSIV (Planshet va Telefon) MOSLASHUV
   ========================================================================= */
@media (max-width: 1180px) {
  .sidebar { width: 220px; }
  .main-content { margin-left: 220px; padding: 22px; }
}

@media (max-width: 900px) {
  .mobile-topbar { display: flex; }
  .admin-layout { flex-direction: column; }
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 280px;
    max-width: 82vw;
    height: 100vh;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: 45;
  }
  .sidebar.open {
    transform: translateX(0);
    box-shadow: 10px 0 34px rgba(7, 27, 16, 0.35);
  }
  .sidebar-overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(7, 27, 16, 0.5);
    z-index: 40;
  }
  .main-content { margin-left: 0; padding: 16px; }
  .content-header { flex-wrap: wrap; gap: 10px; padding: 12px 16px; }
  .page-title { font-size: 17px; }
  .header-right { flex-wrap: wrap; }
  .stats-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 12px; }
  .stat-card { padding: 14px; }
  .stat-info h3 { font-size: 20px; }
  .table-card { padding: 16px; }
  .modal-content { max-width: 92vw; }
}

@media (max-width: 480px) {
  .mobile-brand h2 { font-size: 13px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .stat-card { flex-direction: column; align-items: flex-start; gap: 10px; }
  .table-card { padding: 12px; }
  .content-header { padding: 10px 12px; }
  .add-cat-btn span { display: none; }
  .modal-content { padding: 20px; }
  .form-group input, .select-input { font-size: 16px; }
}
</style>