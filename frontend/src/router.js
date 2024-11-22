import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: "/s/:sheetId",
    name: "Spreadsheet",
    component: () => import('@/pages/Spreadsheet.vue'),
    props: true
  }
]

let router = createRouter({
  history: createWebHistory('/sheets'),
  routes,
})

export default router
