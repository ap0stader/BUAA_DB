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

// ===== Public =====
export interface courseInfo {
    course_id: number
    course_name: string
    course_type: number
    course_credit: number
    course_hours: number
    course_teacher_id: string | null
    course_teacher_name: string | null
    course_plan_filename: string
    course_status: number
}

export interface curriculumPublicInfo {
    curriculum_semester_id: number
    curriculum_semester_name: string
    curriculum_course_id: string
    course_name: string
    course_type: number
    curriculum_teacher_id: string
    curriculum_teacher_name: string
    curriculum_utilization_string: string | null
}

// ===== Course ====

export interface uploadCoursePlanResponse {
    filename: string
}

export interface queryCoursesResponse {
    courses: courseInfo[]
}

export interface curriculumInfo extends curriculumPublicInfo {
    curriculum_id: number
    course_credit: number
    course_hours: number
    curriculum_teacher_department_id: number
    curriculum_capacity: number
    curriculum_choice_number: number
    curriculum_attendance_number: number
    curriculum_info: number
    curriculum_utilization_resources: number[]
}

export interface queryCurriculumsResponse {
    curriculums: curriculumInfo[]
}

// ===== Choice =====
export interface curriculumChoiceInfo {
    choice_student_id: string
    student_name: string
    student_class_id: number
    student_major_id: number
    student_department_id: number
    choice_order: number
    choice_introduction: string | null
}

export interface queryCurriculumChoicesResponse {
    choices: curriculumChoiceInfo[]
}
export interface curriculumAttendanceInfo {
    attendance_student_id: string
    student_name: string
    student_class_id: number
    student_major_id: number
    student_department_id: number
}

export interface queryCurriculumAttendancesResponse {
    attendances: curriculumAttendanceInfo[]
}

// ===== Teacher =====
export interface curriculumScoreInfo extends curriculumAttendanceInfo {
    score: number
}

export interface queryCurriculumScoresResponse {
    scores: curriculumScoreInfo[]
}

// ===== Audit =====
export interface loginAuditInfo {
    login_audit_id: number
    login_audit_claim: string
    login_audit_time: string
    login_audit_result: number
}

export interface queryLoginAuditResponse {
    count: number
    audits: loginAuditInfo[]
}

export interface selectionAuditInfo extends curriculumPublicInfo {
    selection_audit_id: number
    selection_audit_student_id: string
    selection_audit_operator_id: string
    selection_audit_curriculum_id: number
    selection_audit_type: number
    selection_audit_time: string
}

export interface querySelectionAuditResponse {
    count: number
    audits: selectionAuditInfo[]
}
