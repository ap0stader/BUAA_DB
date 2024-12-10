// ===== Auth =====
export interface LoginResponse {
    token: string
    type: number
}

export interface studentInfo {
    student_name: string
    student_gender: string | null
    student_phone: string | null
    student_class_id: number
    student_major_id: number
    student_department_id: number
    headmaster_id: string | null
    headmaster_name: string | null
}

export interface teacherInfo {
    teacher_name: string
    teacher_gender: string | null
    teacher_phone: string | null
    teacher_department_id: number
    headmaster_of_class_id: number | null
}

export interface facultyInfo {
    faculty_name: string
    faculty_gender: string | null
    faculty_phone: string | null
    faculty_department_id: number
}

// ===== Admin =====
export interface placeInfo {
    place_id: number
    place_name: string
    place_is_enable: number
}

export interface queryPlaceResponse {
    places: placeInfo[]
}

export interface departmentFullInfo {
    department_id: number
    department_name: string
}

export interface queryDepartmentResponse {
    departments: departmentFullInfo[]
}

export interface majorInfo {
    major_id: number
    major_name: string
    major_department_id: number
}

export interface marjorFullInfo extends majorInfo {
    major_department_name: string
}

export interface queryMajorResponse {
    majors: majorInfo[]
}

export interface classInfo {
    class_id: number
    class_major_id: number
    class_department_id: number
    class_headmaster_id: number | null
    class_headmaster_name: string | null
}

export interface classFullInfo extends classInfo {
    class_major_name: string
    class_department_name: string
}

export interface queryClassResponse {
    classes: classInfo[]
}

export interface envInfo {
    now_step: number
    now_semester_id: number
}

export interface semesterInfo {
    semester_id: number
    semester_name: string
}

export interface querySemesterResponse {
    semesters: semesterInfo[]
}

export interface studentInfo {
    student_id: string
    student_name: string
    student_gender: string | null
    student_phone: string | null
    student_class_id: number
    student_major_id: number
    student_department_id: number
    login_is_enable: number
}

export interface queryStudentResponse {
    count: number
    students: studentInfo[]
}

export interface addStudentBatchFailedInfo {
    student_id: string
    reason: number
}

export interface addStudentBatchResponse {
    failed_info: addStudentBatchFailedInfo[]
}

export interface teacherInfo {
    teacher_id: string
    teacher_name: string
    teacher_gender: string | null
    teacher_phone: string | null
    teacher_department_id: number
    login_is_enable: number
}

export interface queryTeacherResponse {
    count: number
    teachers: teacherInfo[]
}

export interface facultyInfo {
    faculty_id: string
    faculty_name: string
    faculty_gender: string | null
    faculty_phone: string | null
    faculty_department_id: number
    login_is_enable: number
}

export interface queryFacultyResponse {
    count: number
    faculties: facultyInfo[]
}
