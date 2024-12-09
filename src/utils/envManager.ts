import { useEnv } from "@/stores/env"
import { callapi } from "./callapi"
import type {
    envInfo,
    queryPlaceResponse,
    queryDepartmentResponse,
    queryMajorResponse,
    queryClassResponse,
    querySemesterResponse,
} from "@/types"

const envManager = {
    updatePlace: function () {
        callapi.get("Admin", "queryPlace", null, (data) => {
            const result = <queryPlaceResponse>data
            useEnv().place = result.places
        })
    },
    updateDepartment: function () {
        callapi.get("Admin", "queryDepartment", null, (data) => {
            const result = <queryDepartmentResponse>data
            useEnv().department = result.departments
        })
    },
    updateMajor: function () {
        callapi.get("Admin", "queryMajor", null, (data) => {
            const result = <queryMajorResponse>data
            useEnv().major = result.majors
        })
    },
    updateClass: function () {
        callapi.get("Admin", "queryClass", null, (data) => {
            const result = <queryClassResponse>data
            useEnv().class = result.classes
        })
    },
    updateSemester: function () {
        callapi.get("Admin", "querySemester", null, (data) => {
            const result = <querySemesterResponse>data
            useEnv().semester = result.semesters
        })
    },
    updateEnv: function () {
        callapi.get("Admin", "getEnv", null, (data) => {
            const result = <envInfo>data
            useEnv().env = result
        })
    },
    updateAll: function () {
        useEnv().$reset()
        this.updatePlace()
        this.updateDepartment()
        this.updateMajor()
        this.updateClass()
        this.updateSemester()
        this.updateEnv()
    },
}

export { envManager }
