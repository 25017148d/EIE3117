import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Auth from '../views/Auth.vue';
import PublishRoute from '../views/PublishRoute.vue';
import MyBookings from '../views/MyBookings.vue';
import MyRoutes from '../views/MyRoutes.vue';
import RouteDetail from '../views/RouteDetail.vue';
import { useUserStore } from '../stores/user';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/auth',
      name: 'auth',
      component: Auth
    },
    {
      path: '/publish',
      name: 'publish',
      component: PublishRoute,
      meta: { requiresAuth: true, role: 'driver' }
    },
    {
      path: '/my-bookings',
      name: 'my-bookings',
      component: MyBookings,
      meta: { requiresAuth: true, role: 'passenger' }
    },
    {
      path: '/my-routes',
      name: 'my-routes',
      component: MyRoutes,
      meta: { requiresAuth: true, role: 'driver' }
    },
    {
      path: '/routes/:id',
      name: 'route-detail',
      component: RouteDetail,
      props: true
    }
  ]
});

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  void from;
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    await userStore.checkAuth();
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/auth');
    return;
  }
  
  if (to.meta.role && userStore.user?.type !== to.meta.role) {
      // Redirect to home if role doesn't match
      next('/');
      return;
  }

  next();
});

export default router;
