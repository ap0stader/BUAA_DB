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
import CourseManagement from "@/views/Admin/CourseManagement.vue"
import TeacherCurriculum from "@/views/Teacher/TeacherCurriculum.vue"
import CurriculumChoice from "@/views/Admin/CurriculumChoice.vue"
import CurriculumAttendance from "@/views/Admin/CurriculumAttendance.vue"
import AddCurriculum from "@/views/Teacher/AddCurriculum.vue"
import CurriculumManagement from "@/views/Admin/CurriculumManagement.vue"
import CurriculumScore from "@/views/Teacher/CurriculumScore.vue"

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
                    name: "teacherCourse",
                    path: "teacherCourse",
                    component: TeacherCourse,
                },
                {
                    name: "courseManagement",
                    path: "courseManagement",
                    component: CourseManagement,
                },
                {
                    name: "teacherCurriculum",
                    path: "teacherCurriculum",
                    component: TeacherCurriculum,
                },
                {
                    name: "addCurriculum",
                    path: "addCurriculum",
                    component: AddCurriculum,
                },
                {
                    name: "curriculumManagement",
                    path: "curriculumManagement",
                    component: CurriculumManagement,
                },
                {
                    name: "curriculumAttendance",
                    path: "attendance/:curriculum_id",
                    component: CurriculumAttendance,
                    props: true,
                },
                {
                    name: "curriculumChoice",
                    path: "choice/:curriculum_id",
                    component: CurriculumChoice,
                    props: true,
                },
                {
                    name: "curriculumScore",
                    path: "score/:curriculum_id",
                    component: CurriculumScore,
                    props: true,
            ],
        },
    ],
})

export default router
