import { defineStore } from "pinia"
import type { envInfo, placeInfo, departmentFullInfo, majorInfo, classInfo, semesterInfo } from "@/types"

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
    persist: true,
})
