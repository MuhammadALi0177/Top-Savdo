<template>
  <div class="dashboard-wrapper">
    <aside class="sidebar-menu">
      <div class="sidebar-brand">
        <span class="logo-icon"><i class="ri-box-3-line"></i></span>
        <h3>Top-Savdo B2B</h3>
      </div>
      <div class="user-brief-info">
        <div class="user-avatar"><i class="ri-user-star-line"></i></div>
        <div class="user-meta">
          <span class="user-role">Diler Boshqaruv Paneli</span>
        </div>
      </div>
      <nav class="nav-links">
        <button :class="{ active: activeTab === 'warehouse' }" @click="activeTab = 'warehouse'">
          <i class="ri-database-2-line"></i> Mening Omborim
        </button>
        <button :class="{ active: activeTab === 'bundles' }" @click="activeTab = 'bundles'">
          <i class="ri-shopping-basket-2-line"></i> Savat Yaratish
        </button>
        <button :class="{ active: activeTab === 'orders' }" @click="activeTab = 'orders'">
          <i class="ri-file-list-3-line"></i> Kelgan Buyurtmalar
        </button>
        <button :class="{ active: activeTab === 'clients' }" @click="activeTab = 'clients'">
          <i class="ri-group-line"></i> Magazinchilar & Limitlar
        </button>
        <button :class="{ active: activeTab === 'stats' }" @click="activeTab = 'stats'">
          <i class="ri-line-chart-line"></i> Statistika (Foyda/Zarar)
        </button>
      </nav>
    </aside>

    <div class="main-content-area">
      <header class="main-header">
        <div class="page-title">
          <h2>
            <span v-if="activeTab === 'warehouse'">Mening Mahsulotlarim (Ombor)</span>
            <span v-if="activeTab === 'bundles'">Savat Yaratish (Mahsulotlar To'plami)</span>
            <span v-if="activeTab === 'orders'">Kelib Tushgan Buyurtmalar (Boshqaruv)</span>
            <span v-if="activeTab === 'clients'">Magazinchilar Balansi va Umumiy Limit</span>
            <span v-if="activeTab === 'stats'">Savdo Statistikasi va Foyda/Zarar Hisoboti</span>
          </h2>
        </div>
        <div class="header-actions">
          <button v-if="activeTab === 'warehouse'" @click="openAddModal" class="add-product-btn">
            <i class="ri-add-line"></i> Yangi Mahsulot
          </button>
          <button v-if="activeTab === 'bundles'" @click="openBundleModal" class="add-product-btn">
            <i class="ri-add-line"></i> Yangi Savat
          </button>
          <button @click="handleLogout" class="logout-btn">
            <i class="ri-logout-box-r-line"></i> Chiqish
          </button>
        </div>
      </header>

      <div class="content-body">
        <div v-if="activeTab === 'warehouse'" class="tab-content">
          <div v-if="loading" class="no-data">Mahsulotlar yuklanmoqda...</div>
          <div v-else-if="errorMsg" class="error-box">{{ errorMsg }}</div>
          <div v-else>
            <div class="search-bar-wrap">
              <i class="ri-search-line"></i>
              <input type="text" v-model="warehouseSearch" placeholder="Mahsulot nomi bo'yicha qidirish..."
                class="search-input" />
            </div>

            <div v-if="myProducts.length === 0" class="no-data">
              Sizda mahsulotlar yo'q. Yangi qo'shing!
            </div>
            <div v-else-if="filteredMyProducts.length === 0" class="no-data">
              "{{ warehouseSearch }}" bo'yicha mahsulot topilmadi.
            </div>

            <div v-else class="table-container animate-fade-in">
              <table class="custom-data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Rasm</th>
                    <th>Mahsulot Nomi</th>
                    <th>Kategoriya</th>
                    <th>Narxi</th>
                    <th>Tan narxi</th>
                    <th>Foyda (1 dona)</th>
                    <th>Omborda</th>
                    <th>Holati</th>
                    <th>Harakatlar</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="product in filteredMyProducts" :key="product.id">
                    <td>#{{ product.id }}</td>
                    <td>
                      <img :src="product.main_image ||
                        product.image ||
                        'https://via.placeholder.com/44'
                        " alt="Rasm" style="
                          width: 44px;
                          height: 44px;
                          object-fit: cover;
                          border-radius: 8px;
                          border: 1px solid #e2e8f0;
                        " />
                    </td>
                    <td class="product-name">{{ product.name }}</td>
                    <td>
                      <span class="category-badge">{{
                        product.category_name || product.category || "—"
                      }}</span>
                    </td>
                    <td class="price text-success font-bold">
                      {{ formatPrice(product.price) }} so'm
                    </td>
                    <td class="text-muted-light" style="font-style: normal; color: #64748b">
                      {{ formatPrice(product.cost_price) }} so'm
                    </td>
                    <td class="font-bold" :class="product.profit_per_unit >= 0
                        ? 'text-success'
                        : 'text-danger'
                      ">
                      {{ formatPrice(product.profit_per_unit) }} so'm
                    </td>
                    <td>
                      <span class="stock-badge">{{ product.stock }} ta</span>
                    </td>
                    <td>
                      <span class="status-pill" :class="product.stock > 0 ? 'delivered' : 'cancelled'">
                        {{ product.stock > 0 ? "Sotuvda" : "Tugagan" }}
                      </span>
                    </td>
                    <td>
                      <button @click="deleteProduct(product.id, product.name)" class="delete-btn">
                        <i class="ri-delete-bin-7-line"></i> O'chirish
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'bundles'" class="tab-content animate-fade-in">
          <p class="stats-note" style="margin-bottom: 18px">
            <i class="ri-information-line"></i>
            Bir nechta mahsulotingizni birlashtirib, alohida nom, rasm va narx
            bilan yagona "Savat" sifatida sotuvga chiqarishingiz mumkin. Savat
            ham oddiy mahsulot kabi magazinchilarga ko'rinadi va buyurtma
            qilinadi.
          </p>

          <div v-if="bundlesLoading" class="no-data">
            Savatlar yuklanmoqda...
          </div>
          <div v-else-if="myBundles.length === 0" class="no-data">
            Sizda hali savatlar yo'q. "Yangi Savat" tugmasi orqali birinchi
            savatingizni yarating!
          </div>

          <div v-else class="table-container">
            <table class="custom-data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Rasm</th>
                  <th>Savat Nomi</th>
                  <th>Tarkibi</th>
                  <th>Narxi</th>
                  <th>Omborda</th>
                  <th>Holati</th>
                  <th>Harakatlar</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bundle in myBundles" :key="bundle.id">
                  <td>#{{ bundle.id }}</td>
                  <td>
                    <img :src="bundle.main_image ||
                      bundle.image ||
                      'https://via.placeholder.com/44'
                      " alt="Rasm" style="
                        width: 44px;
                        height: 44px;
                        object-fit: cover;
                        border-radius: 8px;
                        border: 1px solid #e2e8f0;
                      " />
                  </td>
                  <td class="product-name">{{ bundle.name }}</td>
                  <td>
                    <div class="bundle-contents-cell">
                      <span v-for="c in bundle.components" :key="c.id" class="category-badge" style="margin: 2px">
                        {{ c.name }} × {{ c.quantity }}
                      </span>
                    </div>
                  </td>
                  <td class="price text-success font-bold">
                    {{ formatPrice(bundle.price) }} so'm
                  </td>
                  <td>
                    <span class="stock-badge">{{ bundle.stock }} ta</span>
                  </td>
                  <td>
                    <span class="status-pill" :class="bundle.stock > 0 ? 'delivered' : 'cancelled'">
                      {{ bundle.stock > 0 ? "Sotuvda" : "Tugagan" }}
                    </span>
                  </td>
                  <td>
                    <button @click="deleteBundle(bundle.id, bundle.name)" class="delete-btn">
                      <i class="ri-delete-bin-7-line"></i> O'chirish
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'orders'" class="tab-content animate-fade-in">
          <div class="order-filter-bar">
            <button :class="{ active: orderStatusFilter === 'ALL' }" @click="orderStatusFilter = 'ALL'"
              class="filter-pill-btn">
              Hammasi
            </button>
            <button :class="{ active: orderStatusFilter === 'PENDING' }" @click="orderStatusFilter = 'PENDING'"
              class="filter-pill-btn">
              Yangi buyurtmalar
            </button>
            <button :class="{ active: orderStatusFilter === 'DELIVERED' }" @click="orderStatusFilter = 'DELIVERED'"
              class="filter-pill-btn">
              Yetkazib berilgan
            </button>
          </div>

          <div v-if="orders.length === 0" class="no-data">
            Sizga hali buyurtma kelib tushmagan.
          </div>
          <div v-else-if="filteredOrders.length === 0" class="no-data">
            Bu filtr bo'yicha buyurtma topilmadi.
          </div>
          <div v-else class="table-container">
            <table class="custom-data-table">
              <thead>
                <tr>
                  <th>Batafsil</th>
                  <th>Buyurtma ID</th>
                  <th>Magazin</th>
                  <th>Sana</th>
                  <th>Jami Summa</th>
                  <th>Biriktirilgan Kuryer</th>
                  <th>Status</th>
                  <th>Harakatlar (Boshqarish)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in filteredOrders" :key="order.id">
                  <td>
                    <button @click="openOrderDetail(order)" class="detail-btn">
                      <i class="ri-file-search-line"></i> Batafsil
                    </button>
                  </td>
                  <td>#{{ order.id }}</td>
                  <td>
                    <strong>{{
                      order.client_company_name || "Magazinchi"
                    }}</strong>
                  </td>
                  <td>{{ formatDate(order.created_at) }}</td>
                  <td>{{ formatPrice(order.total_amount) }} so'm</td>

                  <td>
                    <div v-if="order.courier_name" class="courier-info-cell">
                      <i class="ri-user-received-2-line"></i>
                      <div>
                        <p class="c-name">{{ order.courier_name }}</p>
                        <p class="c-phone">
                          {{ order.courier_phone || "Tel ko'rsatilmagan" }}
                        </p>
                      </div>
                    </div>
                    <span v-else class="text-muted-light">Hali biriktirilmagan</span>
                  </td>

                  <td>
                    <span class="status-pill" :class="order.status.toLowerCase()">
                      {{ order.status_display || order.status }}
                    </span>
                  </td>
                  <td>
                    <button v-if="order.status === 'PENDING'" @click="processOrder(order.id, 'accept')"
                      class="action-btn accept-btn">
                      <i class="ri-check-line"></i> Qabul qilish
                    </button>

                    <button v-if="order.status === 'ACCEPTED'" @click="processOrder(order.id, 'request-courier')"
                      class="action-btn courier-btn">
                      <i class="ri-truck-line"></i> Kuryer Chaqirish
                    </button>

                    <button v-if="
                      order.status === 'COURIER_REQUESTED' && order.courier_id
                    " @click="shipOrderAutomatic(order.id, order.courier_id)" class="action-btn ship-btn">
                      <i class="ri-hand-coin-line"></i> Yukni topshirdim
                    </button>

                    <span v-if="
                      order.status === 'COURIER_REQUESTED' &&
                      !order.courier_id
                    " class="status-text text-warning animate-pulse">
                      ⏳ Kuryer qabul qilishini kutilmoqda...
                    </span>

                    <span v-if="order.status === 'SHIPPED'" class="status-text text-primary">🚚 Yo'lda...</span>
                    <span v-if="order.status === 'DELIVERED'" class="status-text text-success">✅ Magazinga
                      Yetkazildi</span>
                    <span v-if="order.status === 'CANCELED'" class="status-text text-danger">❌ Bekor qilingan</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'clients'" class="tab-content animate-fade-in">
          <div class="limit-setter-card">
            <div class="limit-info">
              <i class="ri-shield-user-line"></i>
              <div>
                <h4>Magazinchiga Individual Kredit Limiti Belgilash</h4>
                <p>
                  Har bir magazinchiga alohida limit qo'yiladi (boshqalarga
                  ta'sir qilmaydi)
                </p>
              </div>
            </div>
            <div class="limit-input-group">
              <select v-model="selectedClientId" @change="onClientPick" class="client-select">
                <option :value="null" disabled>Magazinchini tanlang...</option>
                <option v-for="c in clientsList" :key="c.id" :value="c.id">
                  {{ c.store_name }} ({{ c.phone_number }})
                </option>
              </select>
              <input type="number" v-model.number="editingLimit" placeholder="Yangi limit kiriting..."
                :disabled="!selectedClientId" />
              <button @click="updateClientLimit" :disabled="updatingLimit || !selectedClientId" class="save-limit-btn">
                {{ updatingLimit ? "Saqlanmoqda..." : "Limitni Yangilash" }}
              </button>
            </div>
          </div>

          <div v-if="clientsList.length === 0" class="no-data">
            Tizimda hali magazinchilar mavjud emas.
          </div>
          <div v-else class="table-container">
            <table class="custom-data-table">
              <thead>
                <tr>
                  <th>Magazin (Kompaniya)</th>
                  <th>Amaldagi Limit</th>
                  <th>Sizdan Joriy Qarzi</th>
                  <th>Mavjud Bo'sh Joyi</th>
                  <th>Holat</th>
                  <th>Qarzni Boshqarish</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="client in clientsList" :key="client.id">
                  <td>
                    <strong>{{ client.store_name }}</strong>
                  </td>
                  <td>{{ formatPrice(client.limit_amount) }} so'm</td>
                  <td class="text-danger font-bold">
                    {{ formatPrice(client.current_debt) }} so'm
                  </td>
                  <td :class="client.limit_amount - client.current_debt < 0
                      ? 'text-danger'
                      : 'text-success'
                    " class="font-bold">
                    {{ formatPrice(client.limit_amount - client.current_debt) }}
                    so'm
                  </td>
                  <td>
                    <span class="status-pill" :class="client.current_debt > client.limit_amount
                        ? 'cancelled'
                        : 'delivered'
                      ">{{
                        client.current_debt > client.limit_amount
                          ? "Limit To'lgan"
                          : "Faol"
                      }}
                    </span>
                  </td>
                  <td>
                    <div class="debt-manage-cell">
                      <input
                        type="number"
                        v-model.number="debtReduceAmount"
                        placeholder="Summa"
                        class="debt-reduce-input"
                        :disabled="client.current_debt <= 0 || reducingDebtId === client.id"
                      />
                      <button
                        class="reduce-debt-btn"
                        :disabled="client.current_debt <= 0 || reducingDebtId === client.id"
                        @click="reduceClientDebt(client)"
                        title="Kiritilgan summaga qarzni kamaytirish"
                      >
                        <i class="ri-subtract-line"></i> Kamaytirish
                      </button>
                      <button
                        class="clear-debt-btn"
                        :disabled="client.current_debt <= 0 || reducingDebtId === client.id"
                        @click="clearClientDebt(client)"
                        title="Butun qarzni nolga tushirish"
                      >
                        <i class="ri-checkbox-circle-line"></i> To'liq Yopish
                      </button>
                    </div>
                  </td>
                  <td>
                    <button class="edit-limit-btn" @click="selectClientForEdit(client)">
                      <i class="ri-edit-line"></i> Limitni o'zgartirish
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="activeTab === 'stats'" class="tab-content animate-fade-in">
          <div class="stats-filter-bar">
            <label>Oy:</label>
            <select v-model.number="statsMonth">
              <option v-for="m in monthOptions" :key="m.value" :value="m.value">
                {{ m.label }}
              </option>
            </select>
            <label>Yil:</label>
            <select v-model.number="statsYear">
              <option v-for="y in yearOptions" :key="y" :value="y">{{ y }}</option>
            </select>
          </div>

          <div v-if="statsLoading" class="no-data">
            Statistika yuklanmoqda...
          </div>
          <div v-else-if="statsErrorMsg" class="error-box">
            {{ statsErrorMsg }}
          </div>
          <div v-else class="stats-grid">
            <div class="stat-card">
              <div class="stat-card-icon" style="background: #e0f2fe; color: #0369a1">
                <i class="ri-calendar-check-line"></i>
              </div>
              <div class="stat-card-body">
                <span class="stat-label">{{ selectedMonthLabel }} sotilgan (savdo)</span>
                <span class="stat-value">{{ formatPrice(dealerStats.monthly_sales) }} so'm</span>
                <span class="stat-sub">{{ dealerStats.monthly_orders_count }} ta yetkazilgan
                  buyurtma</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-card-icon" :style="dealerStats.monthly_profit >= 0
                  ? 'background:#e6f7f0;color:#10b981;'
                  : 'background:#fee2e2;color:#dc2626;'
                ">
                <i :class="dealerStats.monthly_profit >= 0
                    ? 'ri-arrow-up-circle-line'
                    : 'ri-arrow-down-circle-line'
                  "></i>
              </div>
              <div class="stat-card-body">
                <span class="stat-label">
                  {{ selectedMonthLabel }}
                  {{ dealerStats.monthly_profit >= 0 ? "foyda" : "zarar" }}
                </span>
                <span class="stat-value" :class="dealerStats.monthly_profit >= 0
                    ? 'text-success'
                    : 'text-danger'
                  ">
                  {{ formatPrice(dealerStats.monthly_profit) }} so'm
                </span>
                <span class="stat-sub">Tan narxi:
                  {{ formatPrice(dealerStats.monthly_cost) }} so'm</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-card-icon" style="background: #f1f5f9; color: #475569">
                <i class="ri-archive-line"></i>
              </div>
              <div class="stat-card-body">
                <span class="stat-label">Jami sotilgan (hammavaqt)</span>
                <span class="stat-value">{{ formatPrice(dealerStats.total_sales) }} so'm</span>
                <span class="stat-sub">{{ dealerStats.total_orders_count }} ta yetkazilgan
                  buyurtma</span>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-card-icon" :style="dealerStats.total_profit >= 0
                  ? 'background:#e6f7f0;color:#10b981;'
                  : 'background:#fee2e2;color:#dc2626;'
                ">
                <i :class="dealerStats.total_profit >= 0
                    ? 'ri-line-chart-line'
                    : 'ri-line-chart-line'
                  "></i>
              </div>
              <div class="stat-card-body">
                <span class="stat-label">
                  Jami {{ dealerStats.total_profit >= 0 ? "foyda" : "zarar" }}
                </span>
                <span class="stat-value" :class="dealerStats.total_profit >= 0
                    ? 'text-success'
                    : 'text-danger'
                  ">
                  {{ formatPrice(dealerStats.total_profit) }} so'm
                </span>
                <span class="stat-sub">Tan narxi:
                  {{ formatPrice(dealerStats.total_cost) }} so'm</span>
              </div>
            </div>
          </div>

          <p class="stats-note">
            <i class="ri-information-line"></i>
            Hisob-kitob faqat "Yetkazib berildi" holatidagi buyurtmalar bo'yicha
            amalga oshiriladi. Tan narxi va foyda/zarar ma'lumotlari faqat sizga
            ko'rinadi — magazinchilar bu ma'lumotlarni hech qachon ko'rmaydi.
          </p>
        </div>
      </div>
    </div>

    <div class="modal-overlay" v-if="isModalOpen" @click.self="isModalOpen = false">
      <div class="modal-content">
        <h3><i class="ri-add-box-line"></i> Yangi Mahsulot Qo'shish</h3>
        <form @submit.prevent="submitProduct">
          <div class="form-group">
            <label>Mahsulot nomi:</label>
            <input type="text" v-model="newProduct.name" required />
          </div>
          <div class="form-group">
            <label>SKU (Noyob kod):</label>
            <input type="text" v-model="newProduct.sku" placeholder="Masalan: M-001" required />
          </div>

          <div class="form-group">
            <label>Kategoriyasi:</label>
            <select v-model="newProduct.category" required class="select-input">
              <option :value="null" disabled>Kategoriyani tanlang...</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Narxi (so'm) — magazinchiga sotiladigan narx:</label>
            <input type="number" v-model.number="newProduct.price" required />
          </div>
          <div class="form-group">
            <label>Tan narxi (so'm) — sizga tushgan xarajat:</label>
            <input type="number" v-model.number="newProduct.cost_price" placeholder="Masalan: 8000" />
            <small style="color: #94a3b8; font-size: 12px">
              Bu maydon faqat sizga ko'rinadi, magazinchilarga chiqmaydi.
            </small>
          </div>
          <div class="form-group">
            <label>Ombordagi soni:</label>
            <input type="number" v-model.number="newProduct.stock" required />
          </div>
          <div class="form-group">
            <label>Mahsulot haqida (Batafsil / Tavsif):</label>
            <textarea v-model="newProduct.description" rows="4"
              placeholder="Mahsulot haqida batafsil ma'lumot: tarkibi, xususiyatlari, foydalanish bo'yicha tavsiyalar va h.k."
              class="description-textarea"></textarea>
            <small style="color: #94a3b8; font-size: 12px">
              Bu matn mahsulotning "Batafsil" sahifasida magazinchilarga ko'rsatiladi.
            </small>
          </div>
          <div class="form-group">
            <label>Mahsulot rasmi:</label>
            <input type="file" @change="handleImageUpload" accept="image/*" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="isModalOpen = false" class="cancel-btn">
              Bekor qilish
            </button>
            <button type="submit" :disabled="saving" class="save-btn">
              Saqlash
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="modal-overlay" v-if="isBundleModalOpen" @click.self="isBundleModalOpen = false">
      <div class="modal-content" style="max-width: 560px">
        <h3><i class="ri-shopping-basket-2-line"></i> Yangi Savat Yaratish</h3>
        <form @submit.prevent="submitBundle">
          <div class="form-group">
            <label>Savat nomi:</label>
            <input type="text" v-model="newBundle.name" placeholder="Masalan: Oshxona to'plami" required />
          </div>
          <div class="form-group">
            <label>Savat narxi (so'm) — magazinchiga sotiladigan narx:</label>
            <input type="number" v-model.number="newBundle.price" required />
          </div>
          <div class="form-group">
            <label>Omborda nechta savat bor:</label>
            <input type="number" v-model.number="newBundle.stock" required />
          </div>
          <div class="form-group">
            <label>Savat rasmi:</label>
            <input type="file" @change="handleBundleImageUpload" accept="image/*" />
          </div>
          <div class="form-group">
            <label>Savat haqida (Batafsil / Tavsif):</label>
            <textarea v-model="newBundle.description" rows="4"
              placeholder="Savat haqida batafsil ma'lumot: tarkibi, xususiyatlari, foydalanish bo'yicha tavsiyalar va h.k."
              class="description-textarea"></textarea>
          </div>

          <div class="form-group">
            <div class="bundle-picker-header">
              <label>Savat tarkibiga mahsulot qo'shing (o'z omboringizdan):</label>
              <span v-if="selectedBundleProductIds.length > 0" class="bundle-picker-count-badge">
                {{ selectedBundleProductIds.length }} ta tanlandi
              </span>
            </div>

            <div v-if="myProducts.length === 0" class="no-data" style="padding: 15px 0">
              Avval "Mening Omborim" bo'limiga mahsulot qo'shing.
            </div>
            <div v-else>
              <div class="bundle-picker-search-wrap">
                <i class="ri-search-line"></i>
                <input type="text" v-model="bundleProductSearch" placeholder="Mahsulot nomi bo'yicha qidirish..."
                  class="bundle-picker-search-input" />
              </div>

              <div v-if="filteredBundleProducts.length === 0" class="no-data" style="padding: 15px 0">
                "{{ bundleProductSearch }}" bo'yicha mahsulot topilmadi.
              </div>
              <div v-else class="bundle-picker">
                <label v-for="p in filteredBundleProducts" :key="p.id" class="bundle-picker-row"
                  :class="{ selected: selectedBundleProductIds.includes(p.id) }">
                  <input type="checkbox" class="bundle-picker-checkbox" :checked="selectedBundleProductIds.includes(p.id)"
                    @change="toggleBundleProduct(p.id)" />
                  <img :src="p.main_image || p.image || 'https://via.placeholder.com/32'
                    " class="bundle-picker-thumb" />
                  <div class="bundle-picker-info">
                    <span class="bundle-picker-name">{{ p.name }}</span>
                    <span class="bundle-picker-price">{{ formatPrice(p.price) }} so'm</span>
                  </div>
                  <div v-if="selectedBundleProductIds.includes(p.id)" class="bundle-picker-qty-wrap">
                    <input type="number" min="1" v-model.number="bundleQuantities[p.id]" class="bundle-picker-qty"
                      placeholder="Soni" @click.stop />
                    <span class="bundle-picker-qty-label">dona</span>
                  </div>
                </label>
              </div>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" @click="isBundleModalOpen = false" class="cancel-btn">
              Bekor qilish
            </button>
            <button type="submit" :disabled="savingBundle" class="save-btn">
              {{ savingBundle ? "Saqlanmoqda..." : "Savatni Sotuvga Chiqarish" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div class="modal-overlay" v-if="isOrderDetailModalOpen" @click.self="closeOrderDetail">
      <div class="modal-content" style="max-width: 620px" v-if="selectedOrderDetail">
        <h3>
          <i class="ri-file-search-line"></i> Buyurtma #{{
            selectedOrderDetail.id
          }}
          — Batafsil
        </h3>

        <div class="order-detail-meta">
          <p>
            <strong>Magazin:</strong>
            {{
              selectedOrderDetail.client_company_name ||
              selectedOrderDetail.client_store_name ||
              "Magazinchi"
            }}
          </p>
          <p>
            <strong>Sana:</strong>
            {{ formatDate(selectedOrderDetail.created_at) }}
          </p>
          <p>
            <strong>Status:</strong>
            {{
              selectedOrderDetail.status_display ||
              selectedOrderDetail.status
            }}
          </p>
        </div>

        <h4 style="margin: 18px 0 10px">
          <i class="ri-shopping-bag-3-line"></i> Zakaz qilingan mahsulotlar
        </h4>
        <div class="table-container" style="box-shadow: none; margin-bottom: 14px">
          <table class="custom-data-table">
            <thead>
              <tr>
                <th>Mahsulot</th>
                <th>Soni</th>
                <th>Narxi</th>
                <th>Jami</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedOrderDetail.items" :key="item.id">
                <td class="product-name">{{ item.product_name }}</td>
                <td>{{ item.quantity }} ta</td>
                <td>{{ formatPrice(item.price_at_order) }} so'm</td>
                <td class="font-bold">
                  {{ formatPrice(item.price_at_order * item.quantity) }} so'm
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="order-detail-summary">
          <p>
            <span>Umumiy summa:</span>
            <strong>{{ formatPrice(selectedOrderDetail.total_amount) }} so'm</strong>
          </p>
          <p>
            <span>To'langan summa:</span>
            <strong>{{ formatPrice(selectedOrderDetail.paid_amount) }} so'm</strong>
          </p>
          <p class="debt-row">
            <span>Qarzga olingan summa:</span>
            <strong>{{ formatPrice(selectedOrderDetail.debt_amount) }} so'm</strong>
          </p>
        </div>

        <div class="modal-actions">
          <button type="button" @click="closeOrderDetail" class="cancel-btn">
            Yopish
          </button>
          <button type="button" @click="printOrderDetail" class="save-btn">
            <i class="ri-printer-line"></i> Chop etish
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../api";

export default {
  setup() {
    const activeTab = ref("warehouse");
    const myProducts = ref([]);
    // 🟢 YANGI: "Mening Omborim" bo'limida mahsulot nomi bo'yicha qidiruv
    const warehouseSearch = ref("");
    const filteredMyProducts = computed(() => {
      const q = warehouseSearch.value.trim().toLowerCase();
      if (!q) return myProducts.value;
      return myProducts.value.filter((p) =>
        (p.name || "").toLowerCase().includes(q)
      );
    });
    const categories = ref([]); // 🟢 Tizim kategoriyalari state
    const orders = ref([]);
    // 🟢 YANGI: Kelgan buyurtmalarni statusi bo'yicha filtrlash
    // (Hammasi / Yangi buyurtmalar / Yetkazib berilgan)
    const orderStatusFilter = ref("ALL");
    const filteredOrders = computed(() => {
      if (orderStatusFilter.value === "ALL") return orders.value;
      if (orderStatusFilter.value === "PENDING") {
        return orders.value.filter((o) => o.status === "PENDING");
      }
      if (orderStatusFilter.value === "DELIVERED") {
        return orders.value.filter((o) => o.status === "DELIVERED");
      }
      return orders.value;
    });
    const isOrderDetailModalOpen = ref(false);
    const selectedOrderDetail = ref(null);
    const loading = ref(false);
    const saving = ref(false);
    const errorMsg = ref("");
    const isModalOpen = ref(false);
    const router = useRouter();

    // 🟢 YANGI: "Savat yaratish" bo'limi uchun state
    const myBundles = ref([]);
    const bundlesLoading = ref(false);
    const isBundleModalOpen = ref(false);
    const savingBundle = ref(false);
    const newBundle = ref({ name: "", price: null, stock: null, image: null, description: "" });
    const selectedBundleProductIds = ref([]);
    const bundleQuantities = ref({});
    // 🟢 YANGI: "Savat yaratish" oynasida mahsulot nomi bo'yicha qidiruv
    const bundleProductSearch = ref("");
    const filteredBundleProducts = computed(() => {
      const q = bundleProductSearch.value.trim().toLowerCase();
      if (!q) return myProducts.value;
      return myProducts.value.filter((p) =>
        (p.name || "").toLowerCase().includes(q)
      );
    });

    // 🟢 Endi HAR BIR magazinchi uchun alohida limit tizimi
    const clientsList = ref([]); // {id, store_name, phone_number, limit_amount, current_debt}
    const selectedClientId = ref(null);
    const editingLimit = ref(0);
    const updatingLimit = ref(false);

    // 🟢 YANGI: Magazinchining qarzini kamaytirish/nolga tushirish uchun state
    const debtReduceAmount = ref(null);
    const reducingDebtId = ref(null); // hozir amal bajarilayotgan client id (tugmalarni disable qilish uchun)

    // 🟢 Katalog arxitekturasiga 'category' maydoni bog'landi
    const newProduct = ref({
      name: "",
      price: null,
      cost_price: null,
      stock: null,
      category: null,
      sku: "",
      image: null,
      description: "",
    });

    // 🟢 Diler uchun savdo/foyda statistikasi
    const dealerStats = ref({
      monthly_sales: 0,
      monthly_cost: 0,
      monthly_profit: 0,
      monthly_orders_count: 0,
      total_sales: 0,
      total_cost: 0,
      total_profit: 0,
      total_orders_count: 0,
    });
    const statsLoading = ref(false);
    const statsErrorMsg = ref("");

    // 🟢 YANGI: Statistika uchun oy/yil tanlash (masalan, aprel oyi savdosi)
    const nowForStats = new Date();
    const statsMonth = ref(nowForStats.getMonth() + 1);
    const statsYear = ref(nowForStats.getFullYear());
    const monthOptions = [
      { value: 1, label: "Yanvar" },
      { value: 2, label: "Fevral" },
      { value: 3, label: "Mart" },
      { value: 4, label: "Aprel" },
      { value: 5, label: "May" },
      { value: 6, label: "Iyun" },
      { value: 7, label: "Iyul" },
      { value: 8, label: "Avgust" },
      { value: 9, label: "Sentabr" },
      { value: 10, label: "Oktabr" },
      { value: 11, label: "Noyabr" },
      { value: 12, label: "Dekabr" },
    ];
    const yearOptions = (() => {
      const currentYear = nowForStats.getFullYear();
      const years = [];
      for (let y = currentYear; y >= currentYear - 4; y--) years.push(y);
      return years;
    })();
    const selectedMonthLabel = computed(() => {
      const found = monthOptions.find((m) => m.value === statsMonth.value);
      return found ? `${found.label} oyida` : "Tanlangan oyda";
    });

    // 1. Ombor mahsulotlarini yuklash (savatlar bu yerga kirmaydi)
    const fetchMyProducts = async () => {
      loading.value = true;
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("products/?is_bundle=false", {
          headers: { Authorization: `Token ${token}` },
        });
        myProducts.value = response.data;
      } catch (error) {
        errorMsg.value = "Yuklashda xatolik yuz berdi.";
      } finally {
        loading.value = false;
      }
    };

    // 🟢 YANGI: Dilerning o'zi yaratgan savatlarini (to'plamlarini) yuklash
    const fetchMyBundles = async () => {
      bundlesLoading.value = true;
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("products/?is_bundle=true", {
          headers: { Authorization: `Token ${token}` },
        });
        myBundles.value = response.data || [];
      } catch (error) {
        console.error("Savatlarni yuklashda xatolik:", error);
      } finally {
        bundlesLoading.value = false;
      }
    };

    // 🟢 2. Tizimdagi katalog kategoriyalarini yuklash funksiyasi
    // DealerView.vue
    const fetchCategories = async () => {
      try {
        // ESKI: api.get('products/categories/')
        // YANGI:
        const response = await api.get("/categories/");
        categories.value = response.data;
      } catch (e) {
        console.error("Kategoriyalar yuklanmadi:", e);
      }
    };

    // 🟢 Dilerga tegishli barcha magazinchilarni (har birining o'z limiti bilan) yuklaymiz
    const fetchMyClients = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("orders/my_clients/", {
          headers: { Authorization: `Token ${token}` },
        });
        clientsList.value = response.data || [];
      } catch (error) {
        console.error("Magazinchilar ro'yxatini yuklashda xatolik:", error);
      }
    };

    // 🟢 Diler savdo/foyda statistikasini yuklash (faqat DELIVERED buyurtmalar bo'yicha)
    const fetchDealerStats = async () => {
      statsLoading.value = true;
      statsErrorMsg.value = "";
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("orders/dealer_stats/", {
          headers: { Authorization: `Token ${token}` },
          params: { month: statsMonth.value, year: statsYear.value },
        });
        dealerStats.value = response.data;
      } catch (error) {
        statsErrorMsg.value = "Statistikani yuklashda xatolik yuz berdi.";
        console.error("Statistika yuklashda xatolik:", error);
      } finally {
        statsLoading.value = false;
      }
    };

    // 🟢 MUAMMONI TUZATADI: oldin @change="fetchDealerStats" select elementida
    // v-model bilan bir xil "change" hodisasiga ulangani uchun ba'zida
    // statsMonth/statsYear yangilanishidan OLDIN chaqirilib, natijada har doim
    // eski (joriy) oy statistikasi qaytardi. watch orqali bu ishonchli hal qilindi —
    // statsMonth yoki statsYear reaktiv qiymati o'zgarishi TUGAGANDAN keyin
    // avtomatik ravishda fetchDealerStats chaqiriladi.
    watch([statsMonth, statsYear], () => {
      fetchDealerStats();
    });

    // 3. Kelgan buyurtmalar tarixini olish
    const fetchOrderHistory = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.get("orders/", {
          headers: { Authorization: `Token ${token}` },
        });
        orders.value = response.data || [];
      } catch (error) {
        console.error("Buyurtmalarni yuklashda xatolik:", error);
      }
    };

    // 4. Buyurtmani qayta ishlash amallari
    const processOrder = async (orderId, actionType) => {
      try {
        const token = localStorage.getItem("token");
        await api.post(
          `orders/${orderId}/${actionType}/`,
          {},
          {
            headers: { Authorization: `Token ${token}` },
          },
        );
        alert("Muvaffaqiyatli bajarildi!");
        fetchOrderHistory();
      } catch (error) {
        console.error("Xatolik:", error);
        alert("Amalni bajarib bo'lmadi!");
      }
    };

    // 5. Yukni kuryerga topshirish
    const shipOrderAutomatic = async (orderId, currentCourierId) => {
      try {
        const token = localStorage.getItem("token");
        await api.post(
          `orders/${orderId}/ship/`,
          { courier_id: currentCourierId },
          {
            headers: { Authorization: `Token ${token}` },
          },
        );
        alert("Yuk kuryerga topshirildi va yo'lga chiqdi! 🚚");
        fetchOrderHistory();
      } catch (error) {
        alert("Backend tasdiqlashda xatolik berdi.");
      }
    };

    // 5.1 Buyurtma tafsilotlarini (zakaz qilingan mahsulotlar va qarz) ko'rsatish
    const openOrderDetail = (order) => {
      selectedOrderDetail.value = order;
      isOrderDetailModalOpen.value = true;
    };
    const closeOrderDetail = () => {
      isOrderDetailModalOpen.value = false;
      selectedOrderDetail.value = null;
    };

    // 5.2 Buyurtma tafsilotini chop etish (print)
    const printOrderDetail = () => {
      const order = selectedOrderDetail.value;
      if (!order) return;

      const storeName =
        order.client_company_name || order.client_store_name || "Magazinchi";

      const itemsRows = (order.items || [])
        .map(
          (item) => `
            <tr>
              <td>${item.product_name}</td>
              <td style="text-align:center">${item.quantity} ta</td>
              <td style="text-align:right">${formatPrice(item.price_at_order)} so'm</td>
              <td style="text-align:right">${formatPrice(item.price_at_order * item.quantity)} so'm</td>
            </tr>`,
        )
        .join("");

      const printHtml = `
        <html>
          <head>
            <meta charset="utf-8" />
            <title>Buyurtma #${order.id}</title>
            <style>
              body { font-family: Arial, sans-serif; padding: 24px; color: #1f2026; }
              h2 { margin-bottom: 4px; }
              .meta p { margin: 4px 0; font-size: 14px; }
              table { width: 100%; border-collapse: collapse; margin-top: 18px; }
              th, td { border: 1px solid #cbd5e1; padding: 8px 10px; font-size: 13px; }
              th { background: #f1f5f9; text-align: left; }
              .summary { margin-top: 18px; font-size: 14px; }
              .summary p { display: flex; justify-content: space-between; max-width: 320px; margin: 6px 0; }
              .debt { color: #b91c1c; font-weight: bold; }
            </style>
          </head>
          <body>
            <h2>Buyurtma #${order.id}</h2>
            <div class="meta">
              <p><strong>Magazin:</strong> ${storeName}</p>
              <p><strong>Sana:</strong> ${formatDate(order.created_at)}</p>
            </div>
            <table>
              <thead>
                <tr>
                  <th>Mahsulot</th>
                  <th>Soni</th>
                  <th>Narxi</th>
                  <th>Jami</th>
                </tr>
              </thead>
              <tbody>${itemsRows}</tbody>
            </table>
            <div class="summary">
              <p><span>Umumiy summa:</span><strong>${formatPrice(order.total_amount)} so'm</strong></p>
              <p><span>To'langan summa:</span><strong>${formatPrice(order.paid_amount)} so'm</strong></p>
              <p class="debt"><span>Qarzga olingan summa:</span><strong>${formatPrice(order.debt_amount)} so'm</strong></p>
            </div>
          </body>
        </html>`;

      const printWindow = window.open("", "_blank", "width=750,height=850");
      if (!printWindow) {
        alert("Chop etish oynasini ochib bo'lmadi. Brauzer pop-up bloklagan bo'lishi mumkin.");
        return;
      }
      printWindow.document.write(printHtml);
      printWindow.document.close();
      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
      }, 300);
    };

    // 6. Tanlangan bitta magazinchi uchun individual kredit limitini yangilash
    const updateClientLimit = async () => {
      if (!selectedClientId.value) return alert("Avval magazinchini tanlang!");
      if (editingLimit.value < 0)
        return alert("Limit musbat son bo'lishi shart!");
      updatingLimit.value = true;
      try {
        const token = localStorage.getItem("token");
        const response = await api.post(
          "orders/set_client_limit/",
          { client_id: selectedClientId.value, limit: editingLimit.value },
          {
            headers: { Authorization: `Token ${token}` },
          },
        );
        alert(
          response.data?.message || "Kredit limiti muvaffaqiyatli yangilandi!",
        );
        await fetchMyClients(); // ro'yxatni yangi qiymat bilan yangilaymiz
      } catch (error) {
        const data = error?.response?.data;
        const realMessage =
          data?.message ||
          data?.detail ||
          (typeof data === "string" ? data : null) ||
          "Limitni saqlashda xatolik yuz berdi.";
        alert(realMessage);
      } finally {
        updatingLimit.value = false;
      }
    };

    // Select'dan magazinchi tanlanganda, uning hozirgi limiti inputga o'rnatiladi
    const onClientPick = () => {
      const found = clientsList.value.find(
        (c) => c.id === selectedClientId.value,
      );
      editingLimit.value = found ? found.limit_amount : 0;
    };

    // Jadval qatoridagi "Limitni o'zgartirish" tugmasi bosilganda ham xuddi shunday
    const selectClientForEdit = (client) => {
      selectedClientId.value = client.id;
      editingLimit.value = client.limit_amount;
    };

    // 🟢 YANGI: Magazinchining qarzini kiritilgan summaga kamaytirish
    const reduceClientDebt = async (client) => {
      const amount = Number(debtReduceAmount.value);
      if (!amount || amount <= 0) {
        return alert("Kamaytirish uchun to'g'ri summa kiriting!");
      }
      if (!confirm(`${client.store_name} ning qarzi ${formatPrice(amount)} so'mga kamaytirilsinmi?`)) {
        return;
      }
      reducingDebtId.value = client.id;
      try {
        const token = localStorage.getItem("token");
        const response = await api.post(
          "orders/reduce_client_debt/",
          { client_id: client.id, amount },
          { headers: { Authorization: `Token ${token}` } },
        );
        alert(response.data?.message || "Qarz muvaffaqiyatli kamaytirildi!");
        debtReduceAmount.value = null;
        await fetchMyClients();
      } catch (error) {
        const data = error?.response?.data;
        const realMessage =
          data?.message ||
          data?.detail ||
          (typeof data === "string" ? data : null) ||
          "Qarzni kamaytirishda xatolik yuz berdi.";
        alert(realMessage);
      } finally {
        reducingDebtId.value = null;
      }
    };

    // 🟢 YANGI: Magazinchining butun qarzini nolga tushirish (to'liq yopish)
    const clearClientDebt = async (client) => {
      if (
        !confirm(
          `${client.store_name} ning BUTUN qarzi (${formatPrice(client.current_debt)} so'm) nolga tushirilsinmi? Bu amalni orqaga qaytarib bo'lmaydi!`,
        )
      ) {
        return;
      }
      reducingDebtId.value = client.id;
      try {
        const token = localStorage.getItem("token");
        const response = await api.post(
          "orders/reduce_client_debt/",
          { client_id: client.id, clear: true },
          { headers: { Authorization: `Token ${token}` } },
        );
        alert(response.data?.message || "Qarz to'liq yopildi!");
        await fetchMyClients();
      } catch (error) {
        const data = error?.response?.data;
        const realMessage =
          data?.message ||
          data?.detail ||
          (typeof data === "string" ? data : null) ||
          "Qarzni yopishda xatolik yuz berdi.";
        alert(realMessage);
      } finally {
        reducingDebtId.value = null;
      }
    };

    const openAddModal = () => {
      newProduct.value = {
        name: "",
        price: null,
        cost_price: null,
        stock: null,
        category: null,
        sku: "",
        image: null,
        description: "",
      };
      isModalOpen.value = true;
    };

    const handleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        // Faylni to'g'ridan-to'g'ri obyektdagi image maydoniga joylang
        newProduct.value.image = file;
        console.log("Fayl obyekti:", newProduct.value.image); // Konsolda 'File' deb chiqishi kerak
      }
    };

    // 7. Yangi mahsulotni yuborish (FormData modeli)
    // DealerView.vue ichidagi submitProduct funksiyasi
    const submitProduct = async () => {
      // Talab qilinadigan maydonlarni oldindan tekshirish
      if (
        !newProduct.value.name ||
        !newProduct.value.sku ||
        !newProduct.value.category ||
        newProduct.value.price === null ||
        newProduct.value.stock === null
      ) {
        alert("Iltimos, barcha majburiy maydonlarni to'ldiring!");
        return;
      }

      saving.value = true;

      const formData = new FormData();

      // 1. Har bir maydonni tekshirib append qiling
      // name va boshqa maydonlar aniq string ekanligiga ishonch hosil qiling
      formData.append("name", String(newProduct.value.name || ""));
      formData.append("sku", String(newProduct.value.sku || ""));
      formData.append("price", String(newProduct.value.price || 0));
      formData.append("cost_price", String(newProduct.value.cost_price || 0));
      formData.append("stock", String(newProduct.value.stock || 0));
      formData.append("category", String(newProduct.value.category || ""));
      formData.append("description", String(newProduct.value.description || ""));

      // 2. Faylni faqat File obyekti bo'lsa qo'shing
      if (newProduct.value.image instanceof File) {
        formData.append("image", newProduct.value.image);
      }

      // 3. API so'rovini yuborish (Eng muhim joyi: Headers)
      // DealerView.vue
      try {
        await api.post("/products/", formData, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        });

        // Muvaffaqiyatli bo'lsa: modalni yopish, ro'yxatni yangilash va formani tozalash
        alert("Mahsulot muvaffaqiyatli qo'shildi!");
        isModalOpen.value = false;
        newProduct.value = {
          name: "",
          price: null,
          cost_price: null,
          stock: null,
          category: null,
          sku: "",
          image: null,
          description: "",
        };
        await fetchMyProducts();
      } catch (error) {
        // Xatolikni to'liq va xavfsiz ko'rsatish (error.response bo'lmasligi ham mumkin)
        const details = error.response
          ? JSON.stringify(error.response.data)
          : error.message;
        console.error("Mahsulot qo'shishda xato:", details);
        alert("Mahsulot qo'shishda xatolik yuz berdi: " + details);
      } finally {
        saving.value = false;
      }
    };

    const deleteProduct = async (id, name) => {
      if (confirm(`"${name}" o'chirilsinmi?`)) {
        try {
          const token = localStorage.getItem("token");
          const res = await api.delete(`products/${id}/`, {
            headers: { Authorization: `Token ${token}` },
          });
          // 🟢 Backend endi mahsulot buyurtmalarda ishlatilgan bo'lsa,
          // uni o'chirish o'rniga faolsizlantiradi va xabar bilan 200 qaytaradi.
          if (res?.data?.message) {
            alert(res.data.message);
          }
          fetchMyProducts();
        } catch (error) {
          const msg = error.response?.data?.message || "O'chirishda xatolik.";
          alert(msg);
        }
      }
    };

    // 🟢 YANGI: Savat modalini ochish (holatni tozalab)
    const openBundleModal = () => {
      newBundle.value = { name: "", price: null, stock: null, image: null, description: "" };
      selectedBundleProductIds.value = [];
      bundleQuantities.value = {};
      bundleProductSearch.value = "";
      isBundleModalOpen.value = true;
    };

    // 🟢 Mahsulotni savat tarkibiga qo'shish/olib tashlash
    const toggleBundleProduct = (id) => {
      const idx = selectedBundleProductIds.value.indexOf(id);
      if (idx === -1) {
        selectedBundleProductIds.value.push(id);
        if (!bundleQuantities.value[id]) {
          bundleQuantities.value[id] = 1;
        }
      } else {
        selectedBundleProductIds.value.splice(idx, 1);
      }
    };

    const handleBundleImageUpload = (event) => {
      const file = event.target.files[0];
      if (file) {
        newBundle.value.image = file;
      }
    };

    // 🟢 Yangi savatni backendga yuborish va sotuvga chiqarish
    const submitBundle = async () => {
      if (
        !newBundle.value.name ||
        newBundle.value.price === null ||
        newBundle.value.stock === null
      ) {
        alert("Iltimos, savat nomi, narxi va sonini kiriting!");
        return;
      }
      if (selectedBundleProductIds.value.length === 0) {
        alert("Savat tarkibiga kamida bitta mahsulot qo'shing!");
        return;
      }

      const items = selectedBundleProductIds.value.map((id) => ({
        product_id: id,
        quantity: bundleQuantities.value[id] || 1,
      }));

      savingBundle.value = true;
      const formData = new FormData();
      formData.append("name", String(newBundle.value.name));
      formData.append("price", String(newBundle.value.price));
      formData.append("stock", String(newBundle.value.stock));
      formData.append("description", String(newBundle.value.description || ""));
      formData.append("items", JSON.stringify(items));
      if (newBundle.value.image instanceof File) {
        formData.append("image", newBundle.value.image);
      }

      try {
        await api.post("/products/create_bundle/", formData, {
          headers: {
            Authorization: `Token ${localStorage.getItem("token")}`,
          },
        });
        alert("Savat muvaffaqiyatli yaratildi va sotuvga chiqarildi!");
        isBundleModalOpen.value = false;
        await fetchMyBundles();
      } catch (error) {
        const details = error.response
          ? JSON.stringify(error.response.data)
          : error.message;
        console.error("Savat yaratishda xato:", details);
        alert("Savat yaratishda xatolik yuz berdi: " + details);
      } finally {
        savingBundle.value = false;
      }
    };

    // 🟢 Savatni o'chirish (savat ham Product bo'lgani uchun xuddi shu endpoint ishlaydi)
    const deleteBundle = async (id, name) => {
      if (confirm(`"${name}" savati o'chirilsinmi?`)) {
        try {
          const token = localStorage.getItem("token");
          const res = await api.delete(`products/${id}/`, {
            headers: { Authorization: `Token ${token}` },
          });
          // 🟢 Savat ham buyurtmalarda ishlatilgan bo'lsa, backend uni
          // faolsizlantiradi va tushunarli xabar bilan 200 qaytaradi.
          if (res?.data?.message) {
            alert(res.data.message);
          }
          fetchMyBundles();
        } catch (error) {
          const msg = error.response?.data?.message || "Savatni o'chirishda xatolik.";
          alert(msg);
        }
      }
    };

    const handleLogout = () => {
      localStorage.clear();
      router.push("/");
    };
    const formatPrice = (val) => parseFloat(val).toLocaleString();
    const formatDate = (dateStr) =>
      new Date(dateStr).toLocaleDateString("uz-UZ");

    onMounted(() => {
      fetchMyProducts();
      fetchCategories(); // Komponent ochilganda kategoriyalarni ham olyapmiz
      fetchOrderHistory();
      fetchMyClients(); // 🟢 Magazinchilar va ularning individual limitlari
      fetchDealerStats(); // 🟢 Savdo/foyda statistikasi
      fetchMyBundles(); // 🟢 Diler yaratgan savatlar (to'plamlar)
    });

    return {
      activeTab,
      myProducts,
      warehouseSearch,
      filteredMyProducts,
      categories,
      orders,
      orderStatusFilter,
      filteredOrders,
      loading,
      saving,
      errorMsg,
      isModalOpen,
      newProduct,
      clientsList,
      selectedClientId,
      editingLimit,
      updatingLimit,
      dealerStats,
      statsLoading,
      statsErrorMsg,
      statsMonth,
      statsYear,
      monthOptions,
      yearOptions,
      selectedMonthLabel,
      updateClientLimit,
      onClientPick,
      selectClientForEdit,
      debtReduceAmount,
      reducingDebtId,
      reduceClientDebt,
      clearClientDebt,
      processOrder,
      shipOrderAutomatic,
      isOrderDetailModalOpen,
      selectedOrderDetail,
      openOrderDetail,
      closeOrderDetail,
      printOrderDetail,
      openAddModal,
      submitProduct,
      deleteProduct,
      handleLogout,
      formatPrice,
      handleImageUpload,
      formatDate,
      // 🟢 YANGI: Savat yaratish bo'limi
      myBundles,
      bundlesLoading,
      isBundleModalOpen,
      savingBundle,
      newBundle,
      selectedBundleProductIds,
      bundleProductSearch,
      filteredBundleProducts,
      bundleQuantities,
      openBundleModal,
      toggleBundleProduct,
      handleBundleImageUpload,
      submitBundle,
      deleteBundle,
    };
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ---------- Asosiy struktura ---------- */
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
  flex-shrink: 0;
  background: linear-gradient(190deg, var(--forest-950) 0%, var(--forest-900) 55%, var(--forest-700) 100%);
  color: white;
  padding: 26px 20px;
  display: flex;
  flex-direction: column;
  gap: 22px;
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
  margin: 0;
  color: #eafbf2;
  font-weight: 700;
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
  width: 34px;
  height: 34px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(110, 231, 168, 0.15);
  font-size: 17px;
  color: #6ee7a8;
  flex-shrink: 0;
}

.user-role {
  font-size: 12px;
  color: #bcd9c8;
  font-weight: 600;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.nav-links button {
  background: transparent;
  border: none;
  color: #bcd9c8;
  padding: 12px 14px;
  border-radius: 10px;
  text-align: left;
  cursor: pointer;
  font-size: 13.5px;
  font-weight: 600;
  font-family: inherit;
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  transition: all 0.2s ease;
}

.nav-links button i {
  font-size: 17px;
}

.nav-links button:hover {
  background: rgba(255, 255, 255, 0.07);
  color: #fff;
}

.nav-links button.active {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.3);
}

/* ---------- Asosiy hudud ---------- */
.main-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 18px 30px;
  border-bottom: 1px solid var(--line);
}

.main-header h2 {
  font-family: 'Manrope', sans-serif;
  font-size: 19px;
  margin: 0;
  color: var(--ink-900);
  font-weight: 800;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.content-body {
  padding: 28px;
  max-width: 1300px;
  width: 100%;
  margin: 0 auto;
  box-sizing: border-box;
}

/* ---------- Tugmalar ---------- */
.add-product-btn {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  color: #06170e;
  border: none;
  padding: 10px 18px;
  border-radius: 10px;
  font-weight: 700;
  font-family: inherit;
  font-size: 13.5px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.28);
  transition: all 0.2s ease;
}
.add-product-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 20px rgba(5, 150, 105, 0.36); }

.logout-btn {
  background: transparent;
  color: var(--ink-900);
  border: 1px solid var(--line);
  padding: 10px 18px;
  border-radius: 10px;
  font-family: inherit;
  font-size: 13.5px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.logout-btn:hover { border-color: #fca5a5; color: #dc2626; background: #fef2f2; }

/* ---------- Qidiruv / filtr ---------- */
.search-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border: 1.5px solid var(--line);
  border-radius: 11px;
  padding: 10px 14px;
  margin-bottom: 18px;
  max-width: 380px;
  color: #9db3a8;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.search-bar-wrap:focus-within { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); color: var(--forest-700); }
.search-input { border: none; outline: none; flex: 1; font-size: 14px; color: var(--ink-900); background: transparent; font-family: inherit; }

.order-filter-bar { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.filter-pill-btn {
  border: 1.5px solid var(--line);
  background: #fff;
  color: var(--ink-600);
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
}
.filter-pill-btn:hover { border-color: var(--accent-500); color: var(--forest-700); }
.filter-pill-btn.active {
  background: linear-gradient(to right, var(--accent-500), var(--accent-600));
  border-color: transparent;
  color: #06170e;
  box-shadow: 0 6px 14px rgba(5, 150, 105, 0.28);
}

.stats-filter-bar { display: flex; align-items: center; gap: 10px; margin-bottom: 22px; flex-wrap: wrap; }
.stats-filter-bar label { font-size: 13px; font-weight: 700; color: var(--forest-900); }
.stats-filter-bar select {
  border: 1.5px solid var(--line);
  border-radius: 9px;
  padding: 8px 12px;
  font-size: 14px;
  color: var(--ink-900);
  background: #fff;
  cursor: pointer;
  font-family: inherit;
}

/* ---------- Jadval ---------- */
.table-container {
  background: white;
  border-radius: 16px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  border: 1px solid var(--line);
  box-shadow: 0 4px 16px rgba(10, 47, 29, 0.04);
}

.custom-data-table { width: 100%; min-width: 720px; border-collapse: collapse; text-align: left; font-size: 13.5px; }
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
.custom-data-table tr:last-child td { border-bottom: none; }

.product-name { font-weight: 700; color: var(--ink-900); }
.price { color: var(--forest-700); }

/* ---------- Chip va badge ---------- */
.category-badge {
  background: var(--paper);
  color: var(--forest-700);
  padding: 4px 9px;
  border-radius: 7px;
  font-size: 11.5px;
  font-weight: 600;
  border: 1px solid var(--line);
}

.select-input {
  width: 100%;
  padding: 10px 12px;
  border: 1.5px solid var(--line);
  border-radius: 9px;
  box-sizing: border-box;
  background: white;
  font-size: 14px;
  outline: none;
  font-family: inherit;
  color: var(--ink-900);
}
.select-input:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); }

.stock-badge {
  padding: 4px 10px;
  border-radius: 20px;
  background: var(--paper);
  border: 1px solid var(--line);
  font-size: 12px;
  font-weight: 700;
  color: var(--ink-900);
}

.status-pill { padding: 4px 11px; border-radius: 20px; font-size: 10.5px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.3px; display: inline-block; }
.status-pill.delivered, .status-pill.accepted { background: #e2fbe8; color: #15803d; }
.status-pill.cancelled, .status-pill.canceled { background: #fee2e2; color: #b91c1c; }
.status-pill.pending { background: #fef3c7; color: #b45309; }
.status-pill.courier_requested, .status-pill.shipped { background: #e0f2fe; color: #0369a1; }

/* ---------- Amal tugmalari (buyurtma boshqaruvi) ---------- */
.action-btn {
  padding: 8px 15px;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  font-family: inherit;
  font-size: 12.5px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.accept-btn { background: var(--accent-500); color: #06170e; }
.accept-btn:hover { background: var(--accent-600); }
.courier-btn { background: #3b82f6; color: white; }
.courier-btn:hover { background: #2563eb; }
.ship-btn { background: #f59e0b; color: white; box-shadow: 0 3px 8px rgba(245, 158, 11, 0.25); }
.ship-btn:hover { background: #d97706; }
.status-text { font-size: 12.5px; font-weight: 700; }

.delete-btn {
  background: transparent;
  border: 1px solid #fecaca;
  color: #ef4444;
  padding: 7px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 600;
  transition: all 0.2s ease;
}
.delete-btn:hover { background: #ef4444; color: white; }

.detail-btn {
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  padding: 7px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  font-size: 12.5px;
  font-weight: 700;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.detail-btn:hover { background: #1d4ed8; color: white; border-color: #1d4ed8; }

/* ---------- Kuryer ma'lumoti (jadval ichida) ---------- */
.courier-info-cell {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--paper);
  padding: 7px 10px;
  border-radius: 9px;
  border: 1px solid var(--line);
  max-width: 190px;
}
.courier-info-cell i { font-size: 18px; color: var(--forest-700); }
.courier-info-cell p { margin: 0; font-size: 12px; line-height: 1.35; }
.c-name { font-weight: 700; color: var(--ink-900); }
.c-phone { color: var(--ink-600); font-size: 11px !important; }
.text-muted-light { color: #b7c6bd; font-size: 12px; font-style: italic; }

/* ---------- Limit belgilash paneli ---------- */
.limit-setter-card {
  background: white;
  padding: 22px;
  border-radius: 16px;
  border: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
  gap: 20px;
  flex-wrap: wrap;
}
.limit-info { display: flex; align-items: center; gap: 15px; }
.limit-info i {
  font-size: 26px;
  color: var(--forest-700);
  background: rgba(34, 197, 94, 0.1);
  padding: 12px;
  border-radius: 50%;
}
.limit-info h4 { margin: 0 0 4px 0; font-size: 15.5px; color: var(--ink-900); font-weight: 700; }
.limit-info p { margin: 0; font-size: 13.5px; color: var(--ink-600); }

.limit-input-group { display: flex; gap: 10px; }
.limit-input-group input,
.limit-input-group .client-select {
  padding: 10px 14px;
  border: 1.5px solid var(--line);
  border-radius: 9px;
  font-size: 14px;
  outline: none;
  width: 200px;
  font-family: inherit;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.limit-input-group input:focus,
.limit-input-group .client-select:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); }

.save-limit-btn {
  background: var(--forest-900);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 9px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s ease;
}
.save-limit-btn:hover { background: var(--forest-700); }
.save-limit-btn:disabled { background: #cbd5c9; cursor: not-allowed; }

/* ---------- Qarzni boshqarish (jadval qatorida) ---------- */
.debt-manage-cell { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.debt-reduce-input {
  width: 92px;
  padding: 7px 9px;
  border: 1.5px solid var(--line);
  border-radius: 7px;
  font-size: 13px;
  box-sizing: border-box;
  font-family: inherit;
}
.debt-reduce-input:focus { outline: none; border-color: var(--accent-500); }

.reduce-debt-btn, .clear-debt-btn, .edit-limit-btn {
  border: none;
  border-radius: 7px;
  padding: 7px 11px;
  font-size: 12px;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: all 0.2s ease;
}
.reduce-debt-btn { background: #fef3c7; color: #b45309; }
.reduce-debt-btn:hover:not(:disabled) { background: #fde68a; }
.clear-debt-btn { background: #dcfce7; color: #15803d; }
.clear-debt-btn:hover:not(:disabled) { background: #bbf7d0; }
.edit-limit-btn { background: var(--paper); color: var(--forest-700); border: 1px solid var(--line); }
.edit-limit-btn:hover { border-color: var(--accent-500); }
.reduce-debt-btn:disabled, .clear-debt-btn:disabled, .debt-reduce-input:disabled { opacity: 0.5; cursor: not-allowed; }

/* ---------- Statistika kartochkalari ---------- */
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; margin-bottom: 20px; }
.stat-card {
  background: white;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 26px rgba(10, 47, 29, 0.08); }
.stat-card-icon { width: 46px; height: 46px; min-width: 46px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; }
.stat-card-body { display: flex; flex-direction: column; gap: 4px; }
.stat-label { font-size: 12.5px; color: var(--ink-600); font-weight: 700; }
.stat-value { font-family: 'Manrope', sans-serif; font-size: 20px; font-weight: 800; color: var(--ink-900); }
.stat-sub { font-size: 12px; color: #94a89d; }

.stats-note {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 13px 16px;
  color: var(--ink-600);
  font-size: 13px;
}
.stats-note i { font-size: 18px; color: var(--accent-600); }

/* ---------- Modal ---------- */
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  background: rgba(7, 27, 16, 0.55);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  overflow-y: auto;
  padding: 40px 16px;
  box-sizing: border-box;
  z-index: 999;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 18px;
  width: 100%;
  max-width: 450px;
  max-height: calc(100vh - 80px);
  overflow-y: auto;
  box-shadow: 0 24px 60px rgba(7, 27, 16, 0.3);
  box-sizing: border-box;
  font-family: 'Inter', sans-serif;
}
.modal-content h3 {
  font-family: 'Manrope', sans-serif;
  font-size: 18px;
  color: var(--ink-900);
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px;
}
.modal-content h3 i { color: var(--accent-600); }
.modal-content h4 { color: var(--forest-900); font-weight: 700; }
.modal-content::-webkit-scrollbar { width: 8px; }
.modal-content::-webkit-scrollbar-thumb { background: var(--line); border-radius: 8px; }
.modal-content::-webkit-scrollbar-track { background: transparent; }

.form-group { margin-bottom: 18px; }
.form-group label { display: block; margin-bottom: 7px; font-size: 13px; font-weight: 600; color: var(--forest-900); }
.form-group > input {
  width: 100%;
  padding: 11px 13px;
  border: 1.5px solid var(--line);
  border-radius: 9px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.form-group > input:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); }

.description-textarea {
  width: 100%;
  padding: 11px 13px;
  border: 1.5px solid var(--line);
  border-radius: 9px;
  box-sizing: border-box;
  font-family: inherit;
  font-size: 14px;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.description-textarea:focus { border-color: var(--accent-500); box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.12); }

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
.save-btn:disabled { background: #cbd5c9; box-shadow: none; cursor: not-allowed; transform: none; }

.order-detail-meta p { margin: 6px 0; font-size: 14px; color: var(--ink-900); }
.order-detail-summary { border-top: 1px solid var(--line); padding-top: 14px; }
.order-detail-summary p { display: flex; justify-content: space-between; margin: 7px 0; font-size: 14px; color: var(--ink-900); }
.order-detail-summary .debt-row { color: #b91c1c; font-weight: 700; }

/* ---------- Yordamchi klasslar ---------- */
.text-success { color: var(--accent-600) !important; }
.text-danger { color: #dc2626 !important; }
.text-primary { color: #2563eb !important; }
.text-warning { color: #ea580c !important; }
.font-bold { font-weight: 700; }

.no-data {
  text-align: center;
  padding: 46px 0;
  color: #9aab9f;
  font-style: italic;
  background: white;
  border-radius: 14px;
  border: 1px solid var(--line);
}

.error-box {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  padding: 14px 16px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 500;
}

.animate-fade-in { animation: fadeIn 0.3s ease; }
.animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

/* ---------- Savat (Bundle) tanlash paneli ---------- */
.bundle-picker-header { display: flex; align-items: center; justify-content: space-between; gap: 10px; flex-wrap: wrap; margin-bottom: 8px; }
.bundle-picker-count-badge {
  background: rgba(34, 197, 94, 0.1);
  color: var(--forest-700);
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 999px;
  white-space: nowrap;
}

.bundle-picker-search-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fff;
  border: 1.5px solid var(--line);
  border-radius: 10px;
  padding: 9px 12px;
  margin-bottom: 10px;
  color: #9db3a8;
  transition: border-color 0.2s ease, color 0.2s ease;
}
.bundle-picker-search-wrap:focus-within { border-color: var(--accent-500); color: var(--forest-700); }
.bundle-picker-search-input { border: none; outline: none; flex: 1; font-size: 14px; color: var(--ink-900); background: transparent; font-family: inherit; }

.bundle-picker {
  max-height: 280px;
  overflow-y: auto;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 6px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: var(--paper);
}

.bundle-picker-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px;
  border-radius: 10px;
  cursor: pointer;
  background: white;
  border: 1px solid var(--line);
  transition: background 0.15s ease, border-color 0.15s ease;
}
.bundle-picker-row:hover { background: #fafcfa; border-color: #cbd5c9; }
.bundle-picker-row.selected { background: rgba(34, 197, 94, 0.07); border-color: var(--accent-500); }

.bundle-picker-checkbox { width: 18px; height: 18px; min-width: 18px; margin: 0; padding: 0; border-radius: 4px; accent-color: var(--accent-600); cursor: pointer; }
.bundle-picker-thumb { width: 40px; height: 40px; min-width: 40px; object-fit: cover; border-radius: 8px; border: 1px solid var(--line); }
.bundle-picker-info { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
.bundle-picker-name { font-size: 14px; font-weight: 600; color: var(--ink-900); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.bundle-picker-price { font-size: 12px; color: var(--ink-600); white-space: nowrap; }
.bundle-picker-qty-wrap { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.bundle-picker-qty { width: 56px; padding: 6px 8px; border: 1.5px solid var(--line); border-radius: 7px; font-size: 13px; text-align: center; box-sizing: border-box; font-family: inherit; }
.bundle-picker-qty-label { font-size: 12px; color: #9db3a8; white-space: nowrap; }
.bundle-contents-cell { display: flex; flex-wrap: wrap; max-width: 260px; gap: 4px; }

/* =========================================================================
   RESPONSIV (Planshet va Telefon) MOSLASHUV
   ========================================================================= */
@media (max-width: 1024px) {
  .dashboard-wrapper { flex-direction: column; min-height: 100vh; }

  .sidebar-menu {
    width: 100%;
    flex-direction: row;
    align-items: center;
    gap: 14px;
    padding: 12px 16px;
    position: sticky;
    top: 0;
    z-index: 50;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;
  }
  .sidebar-menu::-webkit-scrollbar { display: none; }

  .sidebar-brand { flex-shrink: 0; border-bottom: none; padding-bottom: 0; }
  .sidebar-brand h3 { font-size: 15px; white-space: nowrap; }

  .user-brief-info { flex-shrink: 0; padding: 8px 10px; }
  .user-role { white-space: nowrap; }

  .nav-links { flex-direction: row; gap: 6px; flex-shrink: 0; }
  .nav-links button { width: auto; white-space: nowrap; padding: 10px 14px; }

  .main-header { padding: 14px 18px; flex-wrap: wrap; gap: 10px; }
  .content-body { padding: 18px; }

  .limit-input-group input { width: 160px; }
}

@media (max-width: 640px) {
  .sidebar-brand h3, .user-brief-info { display: none; }
  .sidebar-menu { padding: 10px 12px; gap: 8px; }
  .nav-links button { padding: 9px 12px; font-size: 13px; }
  .nav-links button i { font-size: 15px; }

  .main-header { padding: 12px 14px; }
  .main-header h2 { font-size: 15px; }
  .header-actions { width: 100%; }
  .header-actions button { flex: 1; justify-content: center; }

  .content-body { padding: 14px; }

  .search-bar-wrap { max-width: 100%; }

  .stats-grid { grid-template-columns: 1fr; gap: 12px; }

  .limit-setter-card { flex-direction: column; align-items: stretch; padding: 16px; }
  .limit-input-group { flex-direction: column; }
  .limit-input-group input, .limit-input-group .client-select { width: 100%; box-sizing: border-box; }
  .save-limit-btn { width: 100%; }

  .modal-overlay { padding: 16px 10px; }
  .modal-content { padding: 20px; border-radius: 14px; }

  .custom-data-table { min-width: 640px; font-size: 13px; }
  .custom-data-table th, .custom-data-table td { padding: 10px 12px; }
}

@media (max-width: 380px) {
  .nav-links button span, .nav-links button { font-size: 12.5px; }
  .modal-content { padding: 16px; }
}
</style>