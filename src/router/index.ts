import { createRouter, createWebHistory } from "vue-router"
import Auth from "@/views/Auth/AuthView.vue"
import Login from "@/views/Auth/Login.vue"
import Home from "@/views/Home/HomeView.vue"
import UserCenter from "@/views/Home/UserCenter.vue"
import PlaceManagement from "@/views/Admin/PlaceManagement.vue"
import DepartmentManagment from "@/views/Admin/DepartmentManagement.vue"
import MajorManagement from "@/views/Admin/MajorManagement.vue"

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
                    path: "",
                    redirect: "/home/userCenter",
                },
                {
                    name: "userCenter",
                    path: "userCenter",
                    component: UserCenter,
                },
                {
                    name: "placeManagement",
                    path: "placeManagement",
                    component: PlaceManagement,
                },
                {
                    name: "departmentManagement",
                    path: "departmentManagement",
                    component: DepartmentManagment,
                },
                {
                    name: "majorManagement",
                    path: "majorManagement",
                    component: MajorManagement,
                },
            ],
        },
    ],
})

export default router
