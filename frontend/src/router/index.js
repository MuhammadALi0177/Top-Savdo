import { createRouter, createWebHistory } from 'vue-router';
import LandingView from '../views/LandingView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
      meta: { requiresGuest: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresGuest: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrdersView.vue'),
      meta: { requiresAuth: true, role: 'CLIENT' }
    },
    {
      path: '/dealer',
      name: 'dealer',
      component: () => import('../views/DealerView.vue'),
      meta: { requiresAuth: true, role: 'DEALER' }
    },
    {
      path: '/admin/users',
      name: 'AdminUsers',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, role: 'ADMIN' }
    },
    {
      path: '/courier',
      name: 'courier',
      component: () => import('../views/CourierView.vue'), // Yangi kuryer sahifamiz
      meta: { requiresAuth: true, role: 'COURIER' }
    },
    {
      // 🟢 YANGI: Mahsulot "Batafsil" (detail) sahifasi.
      // Bu sahifa ochiq (hech qanday meta.requiresAuth/requiresGuest yo'q),
      // shuning uchun ham mehmon (LandingView) ham tizimga kirgan magazinchi
      // (OrdersView) mahsulot ustiga bosganda shu sahifaga o'ta oladi.
      path: '/product/:id',
      name: 'product-detail',
      component: () => import('../views/ProductDetailView.vue'),
      props: true
    },
    {
      // 🟢 YANGI: Diler "Batafsil" (detail) sahifasi.
      // LandingView'da diler ustiga bosilganda shu sahifaga o'tadi.
      // Ochiq sahifa — login talab qilinmaydi.
      path: '/dealer/:id',
      name: 'dealer-detail',
      component: () => import('../views/DealerDetailView.vue'),
      props: true
    }
  ]
});

// Rolga qarab foydalanuvchining "uy" sahifasini aniqlaydigan yordamchi funksiya
function homePathForRole(userRole) {
  if (userRole === 'ADMIN') return '/admin/users';
  if (userRole === 'DEALER') return '/dealer';
  if (userRole === 'COURIER') return '/courier';
  return '/orders';
}

router.beforeEach((to, from) => {
  const isAuthenticated = !!localStorage.getItem('token');
  const userRole = localStorage.getItem('role') ? localStorage.getItem('role').toUpperCase() : null;

  if (to.meta.requiresAuth && !isAuthenticated) {
    return { path: '/login' };
  }

  if (to.meta.requiresGuest && isAuthenticated) {
    return { path: homePathForRole(userRole) };
  }

  if (to.meta.role && to.meta.role !== userRole) {
    const target = homePathForRole(userRole);
    if (target === to.path) return; // Aylanma yo'naltirishning oldini olamiz
    return { path: target };
  }
});

export default router;