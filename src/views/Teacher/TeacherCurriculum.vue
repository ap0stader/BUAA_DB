<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">查看教学班</p>
        <p class="text-subtitle-2 mb-4">查看本人开设的教学班的情况</p>

        <v-container fluid class="d-flex fill-height">
            <v-card v-for="curriculum in curriculums" width="23%" class="my-3 me-3">
                <v-card-title>{{ curriculum.course_name }}</v-card-title>
                <v-card-text>
                    <p class="mb-3">教学班编号： {{ curriculum.curriculum_id }}</p>
                    <p class="mb-3">开设学期： {{ curriculum.curriculum_semester_name }}</p>
                    <p class="mb-3">课程编号： {{ curriculum.curriculum_course_id }}</p>
                    <p class="mb-3">
                        类型：
                        {{
                            curriculum.course_type === 0
                                ? "必修课"
                                : curriculum.course_type === 1
                                ? "选修课"
                                : curriculum.course_type === 2
                                ? "通识课"
                                : curriculum.course_type === 3
                                ? "体育课"
                                : curriculum.course_type === 4
                                ? "科研课"
                                : "其他课"
                        }}
                    </p>
                    <p class="mb-3">容量： {{ curriculum.curriculum_capacity }}</p>
                    <p class="mb-3">说明： {{ curriculum.curriculum_info ? curriculum.curriculum_info : "无" }}</p>
                    <p class="text-no-wrap overflow-auto">
                        上课时间与地点：
                        {{
                            curriculum.curriculum_utilization_string
                                ? curriculum.curriculum_utilization_string
                                : "暂未分配"
                        }}
                    </p>
                </v-card-text>

                <v-card-actions>
                    <v-btn
                        v-if="curriculum.course_type === 4 && 2 <= env.env.now_step && env.env.now_step <= 4"
                        color="deep-purple-lighten-2"
                        variant="tonal"
                        class="flex-grow-1"
                        @click="gotoCurriculumChoice(curriculum.curriculum_id)"
                        >科研课双选</v-btn
                    >
                    <v-btn
                        color="primary"
                        variant="tonal"
                        class="flex-grow-1"
                        :disabled="env.env.now_step < 3"
                        @click="gotoCurriculumScore(curriculum.curriculum_id)"
                        >查看选课与成绩情况</v-btn
                    >
                </v-card-actions>
            </v-card>
        </v-container>
    </v-container>
</template>

<script lang="ts" setup name="TeacherCurriculum">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { curriculumInfo, queryCurriculumsResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref } from "vue"
    import { useRouter } from "vue-router"

    const env = useEnv()
    const token = useToken()
    const router = useRouter()

    let curriculums = ref([] as curriculumInfo[])

    function queryCurriculums() {
        callapi.get("Course", "queryCurriculums", {}, (data) => {
            const result = <queryCurriculumsResponse>data
            curriculums.value = result.curriculums.filter((curriculum) => curriculum.curriculum_teacher_id === token.id)
        })
    }

    onMounted(() => {
        queryCurriculums()
    })

    function gotoCurriculumChoice(curriculum_id: number) {
        router.push({
            name: "curriculumChoice",
            params: {
                curriculum_id: curriculum_id,
            },
        })
    }

    function gotoCurriculumScore(curriculum_id: number) {
        router.push({
            name: "curriculumScore",
            params: {
                curriculum_id: curriculum_id,
            },
        })
    }
</script>

<style scoped></style>
