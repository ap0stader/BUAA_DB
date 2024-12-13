<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">查看个人成绩</p>
        <p class="text-subtitle-2 mb-4">查看个人过往成绩</p>
        <p class="text-h6 mb-4">GPA：{{ gpa }}</p>
        <p class="text-h6 mb-4">加权平均分：{{ weighted_average }}</p>
        <p class="text-h6 mb-4">算数平均分：{{ average }}</p>

        <v-data-table
            :headers="headers"
            :items="scores.filter((item) => !!item.score)"
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
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="StudentScore">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { queryStudentScoresResponse, studentScoreInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref } from "vue"

    const headers = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "说明", key: "curriculum_info" },
        { title: "分数", key: "score" },
    ]

    const env = useEnv()
    const token = useToken()

    let scores = ref([] as studentScoreInfo[])
    let gpa = ref()
    let weighted_average = ref()
    let average = ref()

    function queryScores() {
        callapi.get("Student", "queryScores", { student_id: token.id }, (data) => {
            const result = <queryStudentScoresResponse>data
            scores.value = result.scores
            gpa.value = result.gpa
            weighted_average.value = result.weighted_average
            average.value = result.average
        })
    }

    onMounted(() => {
        queryScores()
    })
</script>

<style scoped></style>
