<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">申报课程</p>
        <p class="text-subtitle-2 mb-4">申报课程和查看由本人申报的课程</p>

        <v-container fluid class="d-flex fill-height">
            <v-card v-for="course in courses" width="24%" class="my-3 me-3">
                <v-card-title>{{ course.course_name }}</v-card-title>
                <v-card-text>
                    <p class="mb-3">课程编号： {{ course.course_id }}</p>
                    <p class="mb-3">
                        课程分类：
                        {{
                            course.course_type === 0
                                ? "必修课"
                                : course.course_type === 1
                                ? "选修课"
                                : course.course_type === 2
                                ? "通识课"
                                : course.course_type === 3
                                ? "体育课"
                                : course.course_type === 4
                                ? "科研课"
                                : "其他课"
                        }}
                    </p>
                    <p class="mb-3">学分： {{ course.course_credit }}</p>
                    <p>学时： {{ course.course_hours }}</p>
                </v-card-text>
                <v-card-actions>
                    <v-btn v-if="course.course_status === 0" color="deep-purple-lighten-2" block variant="tonal"
                        >课程审核中</v-btn
                    >
                    <v-btn
                        v-if="course.course_status === 1"
                        color="primary"
                        block
                        variant="tonal"
                        @click="openAddDialogAsModify(course)"
                        >查看或修改课程信息</v-btn
                    >
                    <v-btn v-if="course.course_status === 2" color="red" block variant="tonal">课程已停开</v-btn>
                </v-card-actions>
            </v-card>
        </v-container>

        <v-fab
            color="primary"
            prepend-icon="mdi-plus"
            location="top end"
            size="x-large"
            position="sticky"
            text="申报课程"
            extended
            app
            @click="openAddDialog"
            class="mt-4" />

        <v-dialog max-width="500px" v-model="addDialogActive">
            <v-card>
                <v-toolbar>
                    <v-btn icon="mdi-close" @click="addDialogActive = false" />
                    <v-toolbar-title>{{ addDialogAsModify ? "课程详情" : "新增课程" }}</v-toolbar-title>
                </v-toolbar>

                <v-text-field
                    v-model="addDialogName"
                    :rules="[(v) => !!v || '请输入课程名称']"
                    label="课程名称"
                    variant="outlined"
                    class="ma-2 mb-1" />

                <v-select
                    v-model="addDialogType"
                    :rules="[(v) => !!v || v === 0 || '请选择课程分类']"
                    label="课程分类"
                    variant="outlined"
                    class="mx-2 mb-1"
                    :items="courseTypes"
                    item-title="type_name"
                    item-value="type_id" />

                <v-text-field
                    v-model="addDialogCredit"
                    :rules="[(v) => !!v || '请输入学分']"
                    label="学分"
                    type="number"
                    hide-spin-buttons
                    variant="outlined"
                    class="mx-2 mb-1" />

                <v-text-field
                    v-model="addDialogHours"
                    :rules="[(v) => !!v || '请输入学时']"
                    label="学时"
                    type="number"
                    hide-spin-buttons
                    variant="outlined"
                    class="mx-2 mb-1" />

                <v-file-input
                    v-model="addDialogCoursePlanFile"
                    :rules="[(v) => !!v.length || '请选择课程方案文件']"
                    accept=".pdf"
                    label="课程方案文件"
                    variant="outlined"
                    class="mx-2 mb-1"
                    clearable>
                    <template #append>
                        <v-btn
                            color="primary"
                            :disabled="addDialogCoursePlanFile == null"
                            :loading="addDialogCoursePlanFileUploadLoading"
                            @click="onAddDialogCoursePlanFileUploadClick"
                            variant="text"
                            size="large">
                            上传
                        </v-btn>
                    </template>
                </v-file-input>

                <v-btn
                    v-if="!!addDialogCoursePlanFilename"
                    color="primary"
                    variant="tonal"
                    @click="openCoursePlanFile"
                    class="mx-2 mb-1">
                    查看课程方案文件
                </v-btn>

                <template v-slot:actions>
                    <v-btn @click="addDialogActive = false">取消</v-btn>
                    <v-btn
                        color="primary"
                        :loading="addDialogSubmitLoading"
                        :disabled="
                            addDialogName == '' ||
                            addDialogType == undefined ||
                            addDialogCredit == undefined ||
                            addDialogHours == undefined ||
                            addDialogCoursePlanFilename == ''
                        "
                        @click="onAddDialogSubmitClick">
                        确定
                    </v-btn>
                </template>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script lang="ts" setup name="TeacherCourse">
    import { useToken } from "@/stores/token"
    import type { courseInfo, queryCoursesResponse, uploadCoursePlanResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const token = useToken()

    let courses = ref([] as courseInfo[])

    function queryCourses() {
        callapi.get("Course", "queryCourses", {}, (data) => {
            const result = <queryCoursesResponse>data
            courses.value = result.courses.filter((course) => course.course_teacher_id === token.id)
        })
    }

    onMounted(() => {
        queryCourses()
    })

    // ===== Add Dialog =====

    const courseTypes: {
        type_id: number
        type_name: string
    }[] = [
        { type_id: 0, type_name: "必修课" },
        { type_id: 1, type_name: "选修课" },
        { type_id: 2, type_name: "通识课" },
        { type_id: 3, type_name: "体育课" },
        { type_id: 4, type_name: "科研课" },
    ]

    let addDialogActive = ref(false)
    let addDialogAsModify = ref(false)
    let addDialogItem = ref({} as courseInfo)
    let addDialogName = ref("")
    let addDialogType = ref()
    let addDialogCredit = ref()
    let addDialogHours = ref()
    let addDialogCoursePlanFile = ref()
    let addDialogCoursePlanFilename = ref("")

    function openAddDialog() {
        addDialogAsModify.value = false
        addDialogItem.value = {} as courseInfo
        addDialogName.value = ""
        addDialogType.value = undefined
        addDialogCredit.value = undefined
        addDialogHours.value = undefined
        addDialogCoursePlanFile.value = undefined
        addDialogCoursePlanFilename.value = ""
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCourses()
        }
    })

    function openAddDialogAsModify(item: courseInfo) {
        addDialogAsModify.value = true
        addDialogItem.value = item
        addDialogName.value = item.course_name
        addDialogType.value = item.course_type
        addDialogCredit.value = item.course_credit
        addDialogHours.value = item.course_hours
        addDialogCoursePlanFile.value = undefined
        addDialogCoursePlanFilename.value = item.course_plan_filename
        addDialogActive.value = true
    }

    let addDialogCoursePlanFileUploadLoading = ref(false)

    function onAddDialogCoursePlanFileUploadClick() {
        callapi.post(
            "form-data",
            "Course",
            "uploadCoursePlan",
            {
                file: addDialogCoursePlanFile.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "上传成功")
                const result = <uploadCoursePlanResponse>data
                addDialogCoursePlanFilename.value = result.filename
            }
        )
    }

    function openCoursePlanFile() {
        window.open(`/static/upload/${addDialogCoursePlanFilename.value}`)
    }

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        // 有之前的课程的，先取消开设
        if (addDialogAsModify.value) {
            callapi.post("json", "Course", "disableCourse", {
                course_id: addDialogItem.value.course_id,
            })
        }
        callapi.post(
            "json",
            "Course",
            "addCourse",
            {
                course_teacher_id: token.id,
                course_name: addDialogName.value,
                course_type: addDialogType.value,
                course_credit: addDialogCredit.value,
                course_hours: addDialogHours.value,
                course_plan_filename: addDialogCoursePlanFilename.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "课程申报成功")
                addDialogSubmitLoading.value = false
                addDialogActive.value = false
            },
            (errCode) => {
                addDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
