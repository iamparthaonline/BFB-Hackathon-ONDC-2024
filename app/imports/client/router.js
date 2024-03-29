import VueRouter from 'vue-router';

const router = new VueRouter({
  base: '/',
  routes: [
    {
      path: '/',
      component: () => import('./pages/home/index.vue'),
    },
    {
      path: '/imageScanner',
      component: () => import('./pages/imageScanner/index.vue'),
    },
    {
      path: '/test',
      component: () => import('./pages/admin/index.vue'),
    },
  ],
  mode: 'history',
});

export default router;
