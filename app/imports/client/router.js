import VueRouter from 'vue-router';

const router = new VueRouter({
  base: '/',
  routes: [
    {
      path: '/',
      component: () => import('./pages/home/index.vue'),
    },
  ],
  mode: 'history',
});

export default router;
