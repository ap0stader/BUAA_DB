<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">课程管理</p>
        <p class="text-subtitle-2 mb-4">查看、查看管理课程</p>

        <v-data-table :headers="headers" :items="courses" disable-sort sticky items-per-page="50">
            <template v-slot:item.course_type_string="{ item }">
                {{
                    item.course_type === 0
                        ? "必修课"
                        : item.course_type === 1
                        ? "选修课"
                        : item.course_type === 2
                        ? "通识课"
                        : item.course_type === 3
                        ? "体育课"
                        : item.course_type === 4
                        ? "科研课"
                        : "其他课"
                }}
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

    <v-dialog max-width="500px" v-model="accpetDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="accpetDialogActive = false" />
                <v-toolbar-title>通过审核</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 课程临时编号：{{ accpetDialogItem.course_id }} </v-card-item>

            <v-text-field
                v-model="acceptDialogCourseId"
                :rules="[(v) => !!v || '请输入正式的课程编号']"
                label="正式的课程编号"
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="accpetDialogActive = false">取消</v-btn>
                <v-btn
                    color="green"
                    :loading="accpetDialogSubmitLoading"
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
        { title: "课程名称", key: "course_name" },
        { title: "学分", key: "course_credit" },
        { title: "学时", key: "course_hours" },
        { title: "课程类型", key: "course_type_string" },
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
    let accpetDialogActive = ref(false)
    let accpetDialogItem = ref({} as courseInfo)
    let acceptDialogCourseId = ref("")

    function openAcceptDialog(item: courseInfo) {
        accpetDialogItem.value = item
        accpetDialogActive.value = true
    }

    watch(accpetDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCourses()
        }
    })

    let accpetDialogSubmitLoading = ref(false)

    function onAcceptDialogSubmitClick() {
        accpetDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Course",
            "acceptCourse",
            {
                temp_course_id: accpetDialogItem.value.course_id,
                accept_course_id: acceptDialogCourseId.value,
            },
            () => {
                emitter.emit("success_snackbar", "通过审核成功")
                accpetDialogActive.value = false
            }
        )
    }
</script>

<style scoped></style>
