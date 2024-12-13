<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">查看选课情况</p>
        <p class="text-subtitle-2 mb-4">查看选课情况，在退改时间段可以退课</p>

        <v-data-table
            :headers="headers"
            :items="attendances.filter((item) => item.curriculum_semester_id === env.env.now_semester_id)"
            disable-sort
            sticky
            items-per-page="50">
            <template v-slot:item.course_type_string="{ item }">
                {{
                    item.course_type === 0
                        ? "必修"
                        : item.course_type === 1
                        ? "选修"
                        : item.course_type === 2
                        ? "通识"
                        : item.course_type === 3
                        ? "体育"
                        : item.course_type === 4
                        ? "科研"
                        : "其他"
                }}
            </template>
            <template v-slot:item.curriculum_attendance_capacity="{ item }">
                {{ item.curriculum_attendance_number }} / {{ item.curriculum_capacity }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="env.env.now_step === 4"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="deleteAttendance(item)">
                    <v-icon size="default"> mdi-delete </v-icon>
                    退课
                </v-btn>
            </template>
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="StudentAttendance">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { attendanceInfo, queryStudentAttendancesResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref } from "vue"

    const headers = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "上课时间与地点", key: "curriculum_utilization_string" },
        { title: "已选/容量", key: "curriculum_attendance_capacity" },
        { title: "说明", key: "curriculum_info" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let attendances = ref([] as attendanceInfo[])

    function queryAttendances() {
        callapi.get("Choice", "queryStudentAttendances", { student_id: token.id }, (data) => {
            const result = <queryStudentAttendancesResponse>data
            attendances.value = result.attendances
        })
    }

    onMounted(() => {
        queryAttendances()
    })

    function deleteAttendance(item: attendanceInfo) {
        callapi.post(
            "json",
            "Choice",
            "deleteAttendance",
            {
                student_id: token.id,
                curriculum_id: item.attendance_curriculum_id,
                operator_id: token.id,
            },
            () => {
                emitter.emit("success_snackbar", "取消预选成功")
                queryAttendances()
            }
        )
    }
</script>

<style scoped></style>
