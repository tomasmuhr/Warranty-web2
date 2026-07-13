import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ItemsView from '../views/ItemsView.vue'
import ShopsView from '../views/ShopsView.vue'
import DatabaseView from '../views/DatabaseView.vue'
import SearchView from '../views/SearchView.vue'
import AboutView from '../views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/items', name: 'items', component: ItemsView },
    { path: '/shops', name: 'shops', component: ShopsView },
    { path: '/database', name: 'database', component: DatabaseView },
    { path: '/search', name: 'search', component: SearchView },
    { path: '/about', name: 'about', component: AboutView },
  ],
})

export default router
