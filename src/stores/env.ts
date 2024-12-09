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

const stepString: {
    [key: number]: string
} = {
    0: "预选未开始",
    1: "预选时间段",
    2: "正在抽签",
    3: "抽签结束",
    4: "退改时间段",
    5: "退改已结束",
    6: "本学期已结束",
}

export const useEnv = defineStore("env", {
    state: () => {
        return {
            env: {} as envInfo,
            place: [] as placeInfo[],
            department: [] as departmentFullInfo[],
            major: [] as majorInfo[],
            class: [] as classInfo[],
            semester: [] as semesterInfo[],
        }
    },
    getters: {
        getStepString(): string {
            return stepString[this.env.now_step]
        },
        getplaceInfo() {
            return (place_id: number) => {
                return this.place.find((place) => place.place_id == place_id)
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
