<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">预选情况</p>
        <p class="text-h6 mb-4">教学班编号：{{ curriculum?.curriculum_course_id }}</p>
        <p class="text-h6 mb-4">课程名称：{{ curriculum?.course_name }}</p>
        <p class="text-h6 mb-4">开设老师：{{ curriculum?.curriculum_teacher_name }}</p>
        <p class="text-h6 mb-4">
            上课时间与地点：
            {{ curriculum?.curriculum_utilization_string ? curriculum?.curriculum_utilization_string : "暂未分配" }}
        </p>

        <v-data-table
            :headers="curriculum?.course_type === 4 ? headers_4 : headers_0123"
            :items="choices"
            disable-sort
            sticky
            items-per-page="50">
            <template v-slot:item.student_major_name="{ item }">
                {{ env.getMajorInfo(item.student_major_id)?.major_name }}
            </template>
            <template v-slot:item.student_department_name="{ item }">
                {{ env.getDepartmentInfo(item.student_department_id)?.department_name }}
            </template>
            <template v-slot:item.choice_introduction="{ item }">
                {{ item.choice_introduction ? item.choice_introduction : "无" }}
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn variant="tonal" density="comfortable" color="green" class="me-1" @click="addAttendance(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                    中选
                </v-btn>
            </template>
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="CurriculumChoice">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type {
        curriculumChoiceInfo,
        curriculumInfo,
        queryCurriculumChoicesResponse,
        queryCurriculumsResponse,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref } from "vue"

    const props = defineProps<{ curriculum_id: string }>()

    const headers_0123 = [
        { title: "学号", key: "choice_student_id" },
        { title: "姓名", key: "student_name" },
        { title: "班级", key: "student_class_id" },
        { title: "专业", key: "student_major_name" },
        { title: "学院", key: "student_department_name" },
        { title: "志愿顺序", key: "choice_order" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const headers_4 = [
        { title: "学号", key: "choice_student_id" },
        { title: "姓名", key: "student_name" },
        { title: "班级", key: "student_class_id" },
        { title: "专业", key: "student_major_name" },
        { title: "学院", key: "student_department_name" },
        { title: "自我介绍", key: "choice_introduction" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let curriculum = ref<curriculumInfo>()
    let choices = ref([] as curriculumChoiceInfo[])

    function queryChoices() {
        callapi.get("Course", "queryCurriculums", {}, (data) => {
            const result = <queryCurriculumsResponse>data
            curriculum.value = result.curriculums.find((c) => c.curriculum_id === parseInt(props.curriculum_id))
        })
        callapi.get(
            "Choice",
            "queryCurriculumChoices",
            {
                curriculum_id: props.curriculum_id,
            },
            (data) => {
                const result = <queryCurriculumChoicesResponse>data
                choices.value = result.choices
            }
        )
    }

    onMounted(() => {
        queryChoices()
    })

    function addAttendance(item: curriculumChoiceInfo) {
        callapi.post(
            "json",
            "Choice",
            "addAttendance",
            {
                student_id: item.choice_student_id,
                curriculum_id: curriculum.value?.curriculum_id,
                operator_id: token.id,
            },
            () => {
                emitter.emit("success_snackbar", "已确认中选")
                queryChoices()
            }
        )
    }
</script>

<style scoped></style>
