<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">查看预选情况</p>
        <p class="text-subtitle-2 mb-4">查看预选情况。在预选时间段可以取消预选</p>

        <v-data-table
            :headers="headers"
            :items="choices.filter((item) => item.curriculum_semester_id === env.env.now_semester_id)"
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
            <template v-slot:item.curriculum_choice_capacity="{ item }">
                {{ item.curriculum_choice_number }} / {{ item.curriculum_capacity }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="env.env.now_step === 1"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="deleteChoice(item)">
                    <v-icon size="default"> mdi-delete </v-icon>
                    取消预选
                </v-btn>
            </template>
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="StudentChoice">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { choiceInfo, queryStudentChoicesResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref } from "vue"

    const headers = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "上课时间与地点", key: "curriculum_utilization_string" },
        { title: "预选/容量", key: "curriculum_choice_capacity" },
        { title: "说明", key: "curriculum_info" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let choices = ref([] as choiceInfo[])

    function queryChoices() {
        callapi.get("Choice", "queryStudentChoices", { student_id: token.id }, (data) => {
            const result = <queryStudentChoicesResponse>data
            choices.value = result.choices
        })
    }

    onMounted(() => {
        queryChoices()
    })

    function deleteChoice(item: choiceInfo) {
        callapi.post(
            "json",
            "Choice",
            "deleteChoice",
            {
                student_id: token.id,
                curriculum_id: item.choice_curriculum_id,
            },
            () => {
                emitter.emit("success_snackbar", "取消预选成功")
                queryChoices()
            }
        )
    }
</script>

<style scoped></style>
