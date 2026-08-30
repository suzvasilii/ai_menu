import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/pages/main_page/MainPage.vue'
import Menu from '../components/pages/menu_page/Menu.vue'
import NewMenu from '../components/pages/new_menu_page/NewMenu.vue'
import Cart from '../components/pages/cart_page/Cart.vue'

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
    path: '/stores',
    name: 'cart',
    component: Cart
  }]

  export const router = createRouter({
    history: createWebHistory(),
    routes
  })
