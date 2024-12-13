<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">课程管理</p>
        <p class="text-subtitle-2 mb-4">查看和管理课程</p>

        <v-data-table :headers="headers" :items="courses" disable-sort sticky items-per-page="50">
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
            <template v-slot:item.course_teacher_name="{ item }">
                {{ item.course_teacher_name ? item.course_teacher_name : "系统内置" }}
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn
                    variant="tonal"
                    density="comfortable"
                    color="blue"
                    class="me-1"
                    @click="openCoursePlanFile(item)">
                    <v-icon size="default"> mdi-magnify </v-icon>
                    查看课程方案
                </v-btn>
                <v-btn
                    v-if="item.course_status === 0"
                    variant="tonal"
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="openAcceptDialog(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                    通过审核
                </v-btn>
                <v-btn
                    v-if="item.course_status === 0 || item.course_status === 1"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="onDisableCourseClick(item)">
                    <v-icon size="default"> mdi-close </v-icon>
                    停开课程
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="acceptDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="acceptDialogActive = false" />
                <v-toolbar-title>通过审核</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 课程临时编号：{{ acceptDialogItem.course_id }} </v-card-item>

            <v-text-field
                v-model="acceptDialogCourseId"
                :rules="[(v) => !!v || '请输入正式的课程编号']"
                label="正式的课程编号"
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="acceptDialogActive = false">取消</v-btn>
                <v-btn
                    color="green"
                    :loading="acceptDialogSubmitLoading"
                    :disabled="acceptDialogCourseId == ''"
                    @click="onAcceptDialogSubmitClick">
                    通过
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="CourseManagement">
    import { useEnv } from "@/stores/env"
    import type { courseInfo, queryCoursesResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "课程编号", key: "course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "学分", key: "course_credit" },
        { title: "学时", key: "course_hours" },
        { title: "申报教师", key: "course_teacher_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()

    let courses = ref([] as courseInfo[])

    function queryCourses() {
        callapi.get("Course", "queryCourses", {}, (data) => {
            const result = <queryCoursesResponse>data
            courses.value = result.courses
        })
    }

    onMounted(() => {
        queryCourses()
    })

    function openCoursePlanFile(item: courseInfo) {
        window.open(`/static/upload/${item.course_plan_filename}`)
    }

    function onDisableCourseClick(item: courseInfo) {
        callapi.post("json", "Course", "disableCourse", { course_id: item.course_id }, () => {
            emitter.emit("success_snackbar", "停开课程成功")
            queryCourses()
        })
    }

    // ===== Accept Dialog =====
    let acceptDialogActive = ref(false)
    let acceptDialogItem = ref({} as courseInfo)
    let acceptDialogCourseId = ref("")

    function openAcceptDialog(item: courseInfo) {
        acceptDialogItem.value = item
        acceptDialogActive.value = true
    }

    watch(acceptDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCourses()
        }
    })

    let acceptDialogSubmitLoading = ref(false)

    function onAcceptDialogSubmitClick() {
        acceptDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Course",
            "acceptCourse",
            {
                temp_course_id: acceptDialogItem.value.course_id,
                accept_course_id: acceptDialogCourseId.value,
            },
            () => {
                emitter.emit("success_snackbar", "课程通过审核")
                acceptDialogSubmitLoading.value = false
                acceptDialogActive.value = false
            },
            () => {
                acceptDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
