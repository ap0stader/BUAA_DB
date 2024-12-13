<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">选课与成绩情况</p>
        <p class="text-h6 mb-4">教学班编号：{{ curriculum?.curriculum_course_id }}</p>
        <p class="text-h6 mb-4">课程名称：{{ curriculum?.course_name }}</p>
        <p class="text-h6 mb-4">
            上课时间与地点：
            {{ curriculum?.curriculum_utilization_string ? curriculum?.curriculum_utilization_string : "暂未分配" }}
        </p>

        <v-data-table :headers="headers" :items="scores" disable-sort sticky items-per-page="50">
            <template v-slot:item.student_major_name="{ item }">
                {{ env.getMajorInfo(item.student_major_id)?.major_name }}
            </template>
            <template v-slot:item.student_department_name="{ item }">
                {{ env.getDepartmentInfo(item.student_department_id)?.department_name }}
            </template>
            <template v-slot:item.score="{ item }">
                {{ item.score ? item.score : "未录入" }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    :disabled="curriculum?.curriculum_semester_id != env.env.now_semester_id || env.env.now_step < 6"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                    修改成绩
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        :disabled="curriculum?.curriculum_semester_id != env.env.now_semester_id || env.env.now_step < 6"
        color="purple"
        prepend-icon="mdi-plus-box-multiple-outline"
        location="top end"
        size="x-large"
        position="sticky"
        text="批量导入成绩"
        extended
        app
        @click="openUpdateBatchDialog"
        class="mt-4" />

    <v-fab
        color="primary"
        prepend-icon="mdi-download"
        location="bottom end"
        size="x-large"
        position="sticky"
        text="下载汇总表"
        extended
        app
        @click="downloadCurriculumScores"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="updateBatchDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="updateBatchDialogActive = false" />
                <v-toolbar-title>批量导入成绩</v-toolbar-title>
            </v-toolbar>
            <v-file-input
                v-model="updateBatchDialogFile"
                :rules="[(v) => !!v.length || '请选择文件']"
                accept=".xlsx"
                label="请上传填写后的汇总表文件"
                variant="outlined"
                clearable
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="updateBatchDialogActive = false">取消</v-btn>
                <v-btn
                    color="purple"
                    :loading="updateBatchDialogSubmitLoading"
                    :disabled="updateBatchDialogFile == null"
                    @click="onUpdateBatchDialogSubmitClick">
                    上传
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>修改成绩</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 学生学号： {{ modifyDialogItem.student_id }} </v-card-item>

            <v-text-field
                v-model="modifyDialogScore"
                :rules="[(v) => !!v || '请输入成绩', (v) => parseInt(v) > 0 || '成绩必须为非负整数']"
                label="成绩"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="red"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogScore == '' || parseInt(modifyDialogScore) < 0"
                    @click="onModifyDialogSubmitClick">
                    修改
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="CurriculumAttendance">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type {
        addStudentBatchFailedInfo,
        addStudentBatchResponse,
        curriculumInfo,
        curriculumScoreInfo,
        queryCurriculumScoresResponse,
        queryCurriculumsResponse,
    } from "@/types"
    import { baseURL, callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const props = defineProps<{ curriculum_id: string }>()

    const headers = [
        { title: "学号", key: "student_id" },
        { title: "姓名", key: "student_name" },
        { title: "班级", key: "student_class_id" },
        { title: "专业", key: "student_major_name" },
        { title: "学院", key: "student_department_name" },
        { title: "成绩", key: "score" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let curriculum = ref<curriculumInfo>()
    let scores = ref([] as curriculumScoreInfo[])

    function queryScores() {
        callapi.get("Course", "queryCurriculums", {}, (data) => {
            const result = <queryCurriculumsResponse>data
            curriculum.value = result.curriculums.find((c) => c.curriculum_id === parseInt(props.curriculum_id))
        })
        callapi.get(
            "Teacher",
            "queryCurriculumScores",
            {
                curriculum_id: props.curriculum_id,
            },
            (data) => {
                const result = <queryCurriculumScoresResponse>data
                scores.value = result.scores
            }
        )
    }

    onMounted(() => {
        queryScores()
    })

    function downloadCurriculumScores() {
        console.log(baseURL + `/Teacher/downloadCurriculumScores?curriculum_id=${curriculum.value?.curriculum_id}`)
        window.open(baseURL + `/Teacher/downloadCurriculumScores?curriculum_id=${curriculum.value?.curriculum_id}`)
    }

    // ===== Update Batch Dialog =====
    let updateBatchDialogActive = ref(false)
    let updateBatchDialogFile = ref()

    function openUpdateBatchDialog() {
        updateBatchDialogFile.value = undefined
        updateBatchDialogActive.value = true
    }

    let updateBatchDialogSubmitLoading = ref(false)

    function onUpdateBatchDialogSubmitClick() {
        updateBatchDialogSubmitLoading.value = true
        callapi.post(
            "form-data",
            "Teacher",
            "updateScoreBatch",
            {
                curriculum_id: curriculum.value?.curriculum_id,
                file: updateBatchDialogFile.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "成绩批量修改成功")
                updateBatchDialogSubmitLoading.value = false
                updateBatchDialogActive.value = false
            },
            (errCode) => {
                updateBatchDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as curriculumScoreInfo)
    let modifyDialogScore = ref()

    function openModifyDialog(item: curriculumScoreInfo) {
        modifyDialogItem.value = item
        modifyDialogScore.value = item.score
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryScores()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyDialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Teacher",
            "updateScore",
            {
                curriculum_id: curriculum.value?.curriculum_id,
                student_id: modifyDialogItem.value.student_id,
                score: modifyDialogScore.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "成绩修改成功")
                modifyDialogSubmitLoading.value = false
                modifyDialogActive.value = false
            },
            (errCode) => {
                modifyDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
