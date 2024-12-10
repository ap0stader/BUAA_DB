import { createRouter, createWebHistory } from "vue-router"
import Auth from "@/views/Auth/AuthView.vue"
import Login from "@/views/Auth/Login.vue"
import Home from "@/views/Home/HomeView.vue"
import UserCenter from "@/views/Home/UserCenter.vue"
import PlaceManagement from "@/views/Admin/PlaceManagement.vue"
import DepartmentManagment from "@/views/Admin/DepartmentManagement.vue"
import MajorManagement from "@/views/Admin/MajorManagement.vue"
import ClassManagement from "@/views/Admin/ClassManagement.vue"
import StudentMangement from "@/views/Admin/StudentMangement.vue"
import TeacherManagement from "@/views/Admin/TeacherManagement.vue"
import FacultyManagement from "@/views/Admin/FacultyManagement.vue"
import SemesterManagement from "@/views/Admin/SemesterManagement.vue"
import EnvManagement from "@/views/Admin/EnvManagement.vue"
import AuditCenter from "@/views/Admin/AuditCenter.vue"
import TeacherCourse from "@/views/Teacher/TeacherCourse.vue"
import MyCourse from "@/views/Teacher/MyCourse.vue"
import TeacherCurriculum from "@/views/Teacher/TeacherCurriculum.vue"
import MyCurriculum from "@/views/Teacher/MyCurriculum.vue"
import CourseManagement from "@/views/Admin/CourseManagement.vue"

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
                {
                    name: "classManagement",
                    path: "classManagement",
                    component: ClassManagement,
                },
                {
                    name: "studentManagement",
                    path: "studentManagement",
                    component: StudentMangement,
                },
                {
                    name: "teacherManagement",
                    path: "teacherManagement",
                    component: TeacherManagement,
                },
                {
                    name: "facultyManagement",
                    path: "facultyManagement",
                    component: FacultyManagement,
                },
                {
                    name: "semesterManagement",
                    path: "semesterManagement",
                    component: SemesterManagement,
                },
                {
                    name: "envManagement",
                    path: "envManagement",
                    component: EnvManagement,
                },
                {
                    name: "auditCenter",
                    path: "auditCenter",
                    component: AuditCenter,
                },
                {
                    path: "teacherCourse",
                    component: TeacherCourse,
                    children: [
                        {
                            name: "myCourse",
                            path: "",
                            component: MyCourse,
                        },
                    ],
                },
                {
                    name: "courseManagement",
                    path: "courseManagement",
                    component: CourseManagement,
                },
                {
                    path: "teacherCurriculum",
                    component: TeacherCurriculum,
                    children: [
                        {
                            name: "myCurriculum",
                            path: "",
                            component: MyCurriculum,
                        },
                    ],
                },
            ],
        },
    ],
})

export default router
