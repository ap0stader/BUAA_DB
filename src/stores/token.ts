import type { studentInfo, teacherInfo, facultyInfo } from "@/types"
import { defineStore } from "pinia"
import { callapi } from "@/utils/callapi"

export const useToken = defineStore("token", {
    state: () => {
        return {
            token: "",
            id: "",
            type: -1,
            studentInfo: {} as studentInfo,
            teacherInfo: {} as teacherInfo,
            facultyInfo: {} as facultyInfo,
            superadminInfo: {
                superadmin_name: "superadmin",
            },
        }
    },
    actions: {
        setToken(token: string, type: number, id: string) {
            this.$reset()
            this.token = token
            this.id = id
            this.type = type
            if (this.isStudent) {
                callapi.get(
                    "Auth",
                    "queryStudentInfo",
                    {
                        student_id: this.id,
                    },
                    (data) => {
                        this.studentInfo = <studentInfo>data
                    }
                )
            } else if (this.isTeacher) {
                callapi.get(
                    "Auth",
                    "queryTeacherInfo",
                    {
                        teacher_id: this.id,
                    },
                    (data) => {
                        this.teacherInfo = <teacherInfo>data
                    }
                )
            } else if (this.isFaculty) {
                callapi.get(
                    "Auth",
                    "queryFacultyInfo",
                    {
                        faculty_id: this.id,
                    },
                    (data) => {
                        this.facultyInfo = <facultyInfo>data
                    }
                )
            }
        },
    },
    getters: {
        isInit(): boolean {
            return this.type == -1
        },
        isStudent(): boolean {
            return this.type == 0
        },
        isTeacher(): boolean {
            return this.type == 1
        },
        isFaculty(): boolean {
            return this.type == 2
        },
        isSuperAdmin(): boolean {
            return this.type == 3
        },
        getName(): string {
            if (this.isStudent) {
                return this.studentInfo.student_name
            } else if (this.isTeacher) {
                return this.teacherInfo.teacher_name
            } else if (this.isFaculty) {
                return this.facultyInfo.faculty_name
            } else if (this.isSuperAdmin) {
                return this.superadminInfo.superadmin_name
            } else {
                return ""
            }
        }
    },
    persist: true,
})
