import { createRouter, createWebHistory } from "vue-router"
import Auth from "@/views/Auth/AuthView.vue"
import Login from "@/views/Auth/Login.vue"
import Home from "@/views/Home/HomeView.vue"
import UserCenter from "@/views/Home/UserCenter.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/",
            redirect: "/auth",
        },
        {
            path: "/auth",
            component: Auth,
            children: [
                {
                    name: "login",
                    path: "login",
                    component: Login,
                },
            ],
        },
        {
            path: "/home",
            component: Home,
            children: [
                {
                    name: "userCenter",
                    path: "userCenter",
                    component: UserCenter,
                },
            ],
        },
    ],
})

export default router
