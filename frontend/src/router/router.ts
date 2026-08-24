import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/MainPage.vue'
import Menu from '../components/Menu.vue'
import NewMenu from '../components/NewMenu.vue'
import Cart from '../components/Cart.vue'

const routes = [
     {
    path: '/',
    name: 'main',
    component: MainPage
  },
  {
    path: '/menu',
    name: 'menu',
    component: Menu
  },
  {
    path: '/new',
    name: 'new',
    component: NewMenu
  },
{
    path: '/cart',
    name: 'cart',
    component: Cart
  }]

  export const router = createRouter({
    history: createWebHistory(),
    routes
  })
