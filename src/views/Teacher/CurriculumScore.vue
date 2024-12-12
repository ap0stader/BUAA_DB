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
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="CurriculumAttendance">
    import { useEnv } from "@/stores/env"
    import type {
        curriculumInfo,
        curriculumScoreInfo,
        queryCurriculumScoresResponse,
        queryCurriculumsResponse,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref } from "vue"

    const props = defineProps<{ curriculum_id: string }>()

    const headers = [
        { title: "学号", key: "student_id" },
        { title: "姓名", key: "student_name" },
        { title: "班级", key: "student_class_id" },
        { title: "专业", key: "student_major_name" },
        { title: "学院", key: "student_department_name" },
        { title: "成绩", key: "score" },
    ]

    const env = useEnv()

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
</script>

<style scoped></style>
