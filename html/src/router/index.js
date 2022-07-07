import { createRouter, createWebHistory } from 'vue-router'
import MyDay from '@/components/MyDay.vue'
import User from '@/domain/user'
import Login from "@/components/Login.vue"
import Index from "@/components/Index.vue"
import Search from "@/components/Search.vue"

let routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Index',
    component: Index,
    children: [
      {
        path: '/',
        redirect: to => {
          return { path: '/myday' }
        }
      },
      {
        path: '/myday',
        name: "Myday",
        component: MyDay,
        meta: { title: "我的一天" }
      }, {
        path: '/important',
        name: 'Important',
        meta: { title: "重要" },
        component: MyDay,
      }, {
        path: '/tasks',
        name: 'Tasks',
        meta: { title: "任务" },
        component: MyDay
      }, {
        path: '/task/:listID',
        name: 'Task',
        component: MyDay,
      }, {
        path: '/search/:keyword',
        name: 'Search',
        component: Search
      }
    ]
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const user = new User()
  if (to.name == "Login") {
    next();
    return
  }

  if (to.name != "Login" && user.isLogin()) {
    next()
  } else {
    next("/login")
    return
  }
})

export default router