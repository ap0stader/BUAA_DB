<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">开设教学班</p>
        <p class="text-subtitle-2 mb-4">选择课程以开设教学班</p>

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
                <v-btn variant="tonal" density="comfortable" color="green" class="me-1" @click="openAddDialog(item)">
                    <v-icon size="default"> mdi-plus </v-icon>
                    开设教学班
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>开设教学班</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 课程编号：{{ addDialogItem.course_id }} </v-card-item>

            <v-text-field
                v-model="addDialogCurriculumCapacity"
                :rules="[(v) => !!v || '请输入教学班容量', (v) => parseInt(v) > 0 || '教学班容量必须为非负整数']"
                label="教学班容量"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2 mb-1" />

            <v-textarea
                v-model="addDialogCurriculumInfo"
                label="教学班说明"
                variant="outlined"
                color="primary"
                density="compact"
                hide-details
                no-resize
                clearable
                class="mx-2" />

            <v-divider />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="addDialogCurriculumCapacity == '' || parseInt(addDialogCurriculumCapacity) < 0"
                    @click="onAddDialogSubmitClick">
                    开设
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="AddCurriculum">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
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
    const token = useToken()

    let courses = ref([] as courseInfo[])

    function queryCourses() {
        callapi.get("Course", "queryCourses", {}, (data) => {
            const result = <queryCoursesResponse>data
            courses.value = result.courses.filter((course) => course.course_status === 1)
        })
    }

    onMounted(() => {
        queryCourses()
    })

    function openCoursePlanFile(item: courseInfo) {
        window.open(`/static/upload/${item.course_plan_filename}`)
    }

    // ===== Add Dialog =====
    let addDialogActive = ref(false)
    let addDialogItem = ref({} as courseInfo)
    let addDialogCurriculumCapacity = ref("")
    let addDialogCurriculumInfo = ref("")

    function openAddDialog(item: courseInfo) {
        addDialogItem.value = item
        addDialogCurriculumCapacity.value = ""
        addDialogCurriculumInfo.value = ""
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCourses()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Course",
            "addCurriculum",
            {
                curriculum_teacher_id: token.id,
                curriculum_course_id: addDialogItem.value.course_id,
                curriculum_semester_id: env.env.now_semester_id,
                curriculum_capacity: addDialogCurriculumCapacity.value,
                curriculum_info: addDialogCurriculumInfo.value,
            },
            () => {
                emitter.emit("success_snackbar", "开设教学班成功")
                addDialogSubmitLoading.value = false
                addDialogActive.value = false
            },
            () => {
                addDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
