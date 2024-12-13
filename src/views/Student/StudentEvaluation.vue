<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">评教</p>
        <p class="text-subtitle-2 mb-4">评教、查看评教结果</p>

        <v-data-table
            :headers="headers"
            :items="evaluations.filter((item) => item.curriculum_semester_id === env.env.now_semester_id)"
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
            <template v-slot:item.evaluation="{ item }">
                {{ item.evaluation ? item.evaluation : "未评教" }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="env.env.now_step === 6"
                    variant="tonal"
                    density="comfortable"
                    color="green"
                    class="me-1"
                    :disabled="!!item.evaluation"
                    @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-chat-outline </v-icon>
                    评教
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>评教</v-toolbar-title>
            </v-toolbar>
            <v-card-item>
                <p>课程名称： {{ modifyDialogItem.course_name }}</p>
                <p>教师： {{ modifyDialogItem.curriculum_teacher_name }}</p>
            </v-card-item>

            <div class="mx-6">
                <p>问题1</p>
                <v-slider
                    v-model="modifyDialogScore1"
                    min="0"
                    max="10"
                    step="1"
                    color="green"
                    thumb-label="always"
                    class="mx-6 mt-8 mb-1" />
            </div>
            <div class="mx-6">
                <p>问题2</p>
                <v-slider
                    v-model="modifyDialogScore2"
                    min="0"
                    max="10"
                    step="1"
                    color="green"
                    thumb-label="always"
                    class="mx-6 mt-8" />
            </div>
            <div class="mx-6">
                <p>问题3</p>
                <v-slider
                    v-model="modifyDialogScore3"
                    min="0"
                    max="10"
                    step="1"
                    color="green"
                    thumb-label="always"
                    class="mx-6 mt-8" />
            </div>
            <div class="mx-6">
                <p>问题4</p>
                <v-slider
                    v-model="modifyDialogScore4"
                    min="0"
                    max="10"
                    step="1"
                    color="green"
                    thumb-label="always"
                    class="mx-6 mt-8" />
            </div>
            <div class="mx-6">
                <p>问题5</p>
                <v-slider
                    v-model="modifyDialogScore5"
                    min="0"
                    max="10"
                    step="1"
                    color="green"
                    thumb-label="always"
                    class="mx-6 mt-8" />
            </div>
            <v-card-item>
                <p>
                    评教总分：
                    {{
                        (modifyDialogScore1 +
                            modifyDialogScore2 +
                            modifyDialogScore3 +
                            modifyDialogScore4 +
                            modifyDialogScore5) *
                        2
                    }}
                </p>
            </v-card-item>

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn color="green" :loading="modifyDialogSubmitLoading" @click="onModifyDialogSubmitClick">
                    评教
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="StudentEvaluation">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { studentEvaluationInfo, queryStudentEvaluationsResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "说明", key: "curriculum_info" },
        { title: "评教分数", key: "evaluation" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let evaluations = ref([] as studentEvaluationInfo[])

    function queryEvaluations() {
        callapi.get("Student", "queryEvaluations", { student_id: token.id }, (data) => {
            const result = <queryStudentEvaluationsResponse>data
            evaluations.value = result.evaluations
        })
    }

    onMounted(() => {
        queryEvaluations()
    })

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as studentEvaluationInfo)
    let modifyDialogScore1 = ref(10)
    let modifyDialogScore2 = ref(10)
    let modifyDialogScore3 = ref(10)
    let modifyDialogScore4 = ref(10)
    let modifyDialogScore5 = ref(10)

    function openModifyDialog(item: studentEvaluationInfo) {
        modifyDialogItem.value = item
        modifyDialogScore1.value = 10
        modifyDialogScore2.value = 10
        modifyDialogScore3.value = 10
        modifyDialogScore4.value = 10
        modifyDialogScore5.value = 10
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryEvaluations()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyDialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Student",
            "updateEvaluation",
            {
                curriculum_id: modifyDialogItem.value.curriculum_id,
                student_id: token.id,
                evaluation:
                    (modifyDialogScore1.value +
                        modifyDialogScore2.value +
                        modifyDialogScore3.value +
                        modifyDialogScore4.value +
                        modifyDialogScore5.value) *
                    2,
            },
            (data) => {
                emitter.emit("success_snackbar", "评教成功")
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
