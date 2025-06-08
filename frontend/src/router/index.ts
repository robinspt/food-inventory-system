import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue') // You'll create this view later
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue')
  },
  {
    path: '/inventory',
    name: 'InventoryList',
    component: () => import('../views/InventoryListView.vue')
  },
  {
    path: '/add-food-item',
    name: 'AddFoodItem',
    component: () => import('../views/FoodItemManageView.vue')
  },
  {
    path: '/manage-food-item/:id',
    name: 'EditFoodItem',
    component: () => import('../views/FoodItemManageView.vue')
  },
  // Add other routes here as needed
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router 