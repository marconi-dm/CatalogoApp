import { createRouter, createWebHistory } from 'vue-router'

import ProductView from '../views/ProductView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(),

  routes: [
    {
      path: '/produto/:id',
      name: 'product',
      component: ProductView,
    },
    {
      path: '/sobre',
      name: 'about',
      component: AboutView,
    },
  ],
})

export default router