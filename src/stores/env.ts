import { defineStore } from "pinia"
import type {
    envInfo,
    placeInfo,
    departmentFullInfo,
    majorInfo,
    marjorFullInfo,
    classInfo,
    classFullInfo,
    semesterInfo,
} from "@/types"

export const useEnv = defineStore("env", {
    state: () => {
        return {
            env: {} as envInfo,
            places: [] as placeInfo[],
            department: [] as departmentFullInfo[],
            major: [] as majorInfo[],
            class: [] as classInfo[],
            semester: [] as semesterInfo[],
        }
    },
    getters: {
        getplaceInfo() {
            return (place_id: number) => {
                return this.places.find((place) => place.place_id == place_id)
            }
        },
        getDepartmentInfo() {
            return (department_id: number) => {
                return this.department.find((department) => department.department_id == department_id)
            }
        },
        getMajorInfo() {
            return (major_id: number) => {
                let majorLessInfo = this.major.find((major) => major.major_id == major_id)
                if (majorLessInfo == undefined) {
                    return undefined
                } else {
                    let majorFullInfo = <marjorFullInfo>majorLessInfo
                    let departmentInfo = this.getDepartmentInfo(majorFullInfo.major_department_id)
                    if (departmentInfo == undefined) {
                        return undefined
                    } else {
                        majorFullInfo.major_department_name = departmentInfo.department_name
                        return majorFullInfo
                    }
                }
            }
        },
        getClassInfo() {
            return (class_id: number) => {
                let classLessInfo = useEnv().class.find((classInfo) => classInfo.class_id == class_id)
                if (classLessInfo == undefined) {
                    return undefined
                } else {
                    let classFullInfo = <classFullInfo>classLessInfo
                    let departmentInfo = this.getDepartmentInfo(classFullInfo.class_department_id)
                    let majorInfo = this.getMajorInfo(classFullInfo.class_major_id)
                    if (departmentInfo == undefined || majorInfo == undefined) {
                        return undefined
                    } else {
                        classFullInfo.class_major_name = majorInfo.major_name
                        classFullInfo.class_department_name = departmentInfo.department_name
                        return classFullInfo
                    }
                }
            }
        },
        getSemesterInfo(state) {
            return (semester_id: number) => {
                return state.semester.find((semester) => semester.semester_id == semester_id)
            }
        },
    },
    persist: true,
})
