import { useEnv } from "@/stores/env"
import { callapi } from "./callapi"
import type {
    envInfo,
    queryPlaceResponse,
    queryDepartmentResponse,
    queryMajorResponse,
    queryClassResponse,
    querySemesterResponse,
    placeInfo,
    departmentFullInfo,
    marjorFullInfo,
    classFullInfo,
    semesterInfo,
} from "@/types"

const env = {
    updatePlace: function () {
        callapi.get("Admin", "queryPlace", null, (data) => {
            const result = <queryPlaceResponse>data
            useEnv().places = result.places
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
    getplaceInfo: function (place_id: number): placeInfo | undefined {
        return useEnv().places.find((place) => place.place_id == place_id)
    },
    getDepartmentFullInfo: function (department_id: number): departmentFullInfo | undefined {
        console.log(department_id)
        console.log(useEnv().department)
        return useEnv().department.find((department) => department.department_id == department_id)
    },
    getMajorInfo: function (major_id: number): marjorFullInfo | undefined {
        let majorLessInfo = useEnv().major.find((major) => major.major_id == major_id)
        if (majorLessInfo == undefined) {
            return undefined
        } else {
            let majorFullInfo = <marjorFullInfo>majorLessInfo
            majorFullInfo.major_department_name = this.getDepartmentFullInfo(
                majorLessInfo.major_department_id
            )!.department_name
            return majorFullInfo
        }
    },
    getClassInfo: function (class_id: number): classFullInfo | undefined {
        let classLessInfo = useEnv().class.find((classInfo) => classInfo.class_id == class_id)
        if (classLessInfo == undefined) {
            return undefined
        } else {
            let classFullInfo = <classFullInfo>classLessInfo
            classFullInfo.class_major_name = this.getMajorInfo(classLessInfo.class_major_id)!.major_name
            classFullInfo.class_department_name = this.getDepartmentFullInfo(
                classLessInfo.class_department_id
            )!.department_name
            return classFullInfo
        }
    },
    getSemesterInfo: function (semester_id: number): semesterInfo | undefined {
        return useEnv().semester.find((semester) => semester.semester_id == semester_id)
    },
}

export { env }
