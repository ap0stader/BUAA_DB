<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">选课</p>
        <p class="text-subtitle-2 mb-4">查看、选择课程</p>

        <v-text-field
            v-model="searchText"
            label="全局搜索"
            variant="outlined"
            max-width="500px"
            clearable
            class="mt-4" />

        <v-data-table
            :headers="[0, 1].includes(env.env.now_step) ? header_choice : header_attendence"
            :search="searchText"
            :filter-keys="[
                'curriculum_course_id',
                'course_name',
                'course_type_string',
                'curriculum_teacher_name',
                'curriculum_utilization_string',
                'curriculum_info',
            ]"
            :items="
                curriculums.filter(
                    // 筛选能够显示的课程
                    (item) => {
                        let result = true
                        // 对于必修课和选修课，只能选择同学院老师开设的教学班
                        if (item.course_type === 0 || item.course_type === 1) {
                            result = result && item.curriculum_teacher_department_id === token.getDepartmentId
                        }
                        // 其他的课程则不做限制
                        // 课程必须是本学期的
                        result = result && item.curriculum_semester_id === env.env.now_semester_id
                        // 课程必须已经分配了场地
                        result = result && !!item.curriculum_utilization_string
                        return result
                    }
                )
            "
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
            <template v-slot:item.curriculum_attendance_capacity="{ item }">
                {{ item.curriculum_attendance_number }} / {{ item.curriculum_capacity }}
            </template>
            <template v-slot:item.actions="{ item }">
                <!-- 预选 -->
                <v-btn
                    v-if="
                        env.env.now_step === 1 &&
                        studentCurriculums.map((item) => item.choice_curriculum_id).includes(item.curriculum_id)
                    "
                    disabled
                    variant="tonal"
                    density="comfortable"
                    color="green-darken-4"
                    class="me-1">
                    <v-icon size="default"> mdi-check-circle-outline </v-icon>
                    已预选
                </v-btn>
                <v-btn
                    v-else-if="env.env.now_step === 1 && checkChoice(item)"
                    variant="tonal"
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="openChooseDialog(item)">
                    <v-icon size="default"> mdi-check-outline </v-icon>
                    预选
                </v-btn>
                <v-btn
                    v-else-if="env.env.now_step === 1"
                    disabled
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1">
                    <v-icon size="default"> mdi-close-outline </v-icon>
                    不可选择
                </v-btn>

                <!-- 直选 -->

                <v-btn
                    v-if="
                        env.env.now_step === 4 &&
                        studentAttendance.map((item) => item.attendance_curriculum_id).includes(item.curriculum_id)
                    "
                    disabled
                    variant="tonal"
                    density="comfortable"
                    color="green-darken-4"
                    class="me-1">
                    <v-icon size="default"> mdi-check-circle-outline </v-icon>
                    已选
                </v-btn>
                <v-btn
                    v-else-if="env.env.now_step === 4 && checkAttendence(item)"
                    variant="tonal"
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="addAttendance(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                    选课
                </v-btn>
                <v-btn
                    v-else-if="env.env.now_step === 4"
                    disabled
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1">
                    <v-icon size="default"> mdi-close-outline </v-icon>
                    不可选择
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="chooseDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="chooseDialogActive = false" />
                <v-toolbar-title>选课</v-toolbar-title>
            </v-toolbar>

            <v-card-item>
                <p>课程编号： {{ chooseDialogItem.curriculum_course_id }}</p>
                <p>课程名称： {{ chooseDialogItem.course_name }}</p>
                <p>教师： {{ chooseDialogItem.curriculum_teacher_name }}</p>
            </v-card-item>

            <v-select
                v-if="chooseDialogItem.course_type !== 4"
                v-model="chooseDialogOrder"
                :rules="[(v) => !!v || '请选择志愿']"
                :items="chooseDialogOrderList"
                item-title="order_name"
                item-value="order_id"
                label="志愿"
                variant="outlined"
                clearable
                class="ma-2 mb-1" />

            <v-textarea
                v-else
                v-model="chooseDialogIntroduction"
                label="科研自我介绍"
                variant="outlined"
                color="primary"
                density="compact"
                hide-details
                no-resize
                clearable
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="chooseDialogActive = false">取消</v-btn>
                <v-btn
                    color="green"
                    :loading="chooseDialogSubmitLoading"
                    :disabled="
                        (chooseDialogItem.course_type !== 4 && chooseDialogOrder == undefined) ||
                        (chooseDialogItem.course_type === 4 && chooseDialogIntroduction == '')
                    "
                    @click="onChooseDialogSubmitClick">
                    选课
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ChooseCurriculum">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type {
        attendanceInfo,
        choiceInfo,
        curriculumInfo,
        queryCurriculumsResponse,
        queryStudentAttendancesResponse,
        queryStudentChoicesResponse,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const header_choice = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "上课时间与地点", key: "curriculum_utilization_string" },
        { title: "预选/容量", key: "curriculum_choice_capacity" },
        { title: "说明", key: "curriculum_info" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const header_attendence = [
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "名称", key: "course_name" },
        { title: "类型", key: "course_type_string" },
        { title: "老师", key: "curriculum_teacher_name" },
        { title: "上课时间与地点", key: "curriculum_utilization_string" },
        { title: "已选/容量", key: "curriculum_attendance_capacity" },
        { title: "说明", key: "curriculum_info" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let searchText = ref()
    let curriculums = ref([] as curriculumInfo[])
    let studentCurriculums = ref([] as choiceInfo[])
    let studentAttendance = ref([] as attendanceInfo[])

    function queryCurriculums() {
        callapi.get("Course", "queryCurriculums", {}, (data) => {
            const result = <queryCurriculumsResponse>data
            curriculums.value = result.curriculums
        })
        callapi.get("Choice", "queryStudentChoices", { student_id: token.id }, (data) => {
            const result = <queryStudentChoicesResponse>data
            studentCurriculums.value = result.choices
        })
        callapi.get("Choice", "queryStudentAttendances", { student_id: token.id }, (data) => {
            const result = <queryStudentAttendancesResponse>data
            studentAttendance.value = result.attendances
        })
    }

    function checkChoice(item: curriculumInfo): boolean {
        let result = true
        // 首先该课程还有充足的志愿
        const courseChoiceNumber = studentCurriculums.value.filter(
            (choice) => choice.curriculum_course_id === item.curriculum_course_id
        ).length
        if (item.course_type === 0 || item.course_type === 1) {
            // 必修课、选修课
            result = result && courseChoiceNumber < 3
        } else if (item.course_type === 2) {
            // 通识课
            const typeChoiceNumber = studentCurriculums.value.filter(
                (choice) => choice.course_type === item.course_type
            ).length
            result = result && courseChoiceNumber < 3 && typeChoiceNumber < 5
        } else if (item.course_type === 3) {
            // 体育课
            result = result && courseChoiceNumber < 5
        } else if (item.course_type === 4) {
            // 科研课
            result = result && courseChoiceNumber < 1
        } else {
            result = false
        }
        // 其次该教学班不能与已预选的且非同课程编号的课程的教学班冲突
        result =
            result &&
            !studentCurriculums.value.some(
                (choice) =>
                    choice.curriculum_course_id != item.curriculum_course_id &&
                    choice.curriculum_utilization_resources
                        .map((choice_resource) => choice_resource & 0xffff)
                        .some((choice_resource) =>
                            item.curriculum_utilization_resources
                                .map((item_resource) => item_resource & 0xffff)
                                .includes(choice_resource)
                        )
            )
        return result
    }

    function checkAttendence(item: curriculumInfo): boolean {
        let result = true
        // 首先该课程未被选择
        result =
            result &&
            !studentAttendance.value.some((attendance) => attendance.curriculum_course_id === item.curriculum_course_id)
        // 其次该课程还有充足的名额
        result = result && item.curriculum_attendance_number < item.curriculum_capacity
        // 再次该教学班不能与已预选的且非同课程编号的课程的教学班冲突
        result =
            result &&
            !studentAttendance.value.some(
                (attendance) =>
                    attendance.curriculum_course_id != item.curriculum_course_id &&
                    attendance.curriculum_utilization_resources
                        .map((attendance_resource) => attendance_resource & 0xffff)
                        .some((attendance_resource) =>
                            item.curriculum_utilization_resources
                                .map((item_resource) => item_resource & 0xffff)
                                .includes(attendance_resource)
                        )
            )
        return result
    }

    function addAttendance(item: curriculumInfo) {
        callapi.post(
            "json",
            "Choice",
            "addAttendance",
            {
                student_id: token.id,
                curriculum_id: item.curriculum_id,
                operator_id: token.id,
            },
            () => {
                emitter.emit("success_snackbar", "选课成功")
                queryCurriculums()
            }
        )
    }

    onMounted(() => {
        queryCurriculums()
    })

    // ===== Choose Dialog =====
    const orderList: {
        order_id: number
        order_name: string
    }[] = [
        { order_id: 1, order_name: "第一志愿" },
        { order_id: 2, order_name: "第二志愿" },
        { order_id: 3, order_name: "第三志愿" },
        { order_id: 4, order_name: "第四志愿" },
        { order_id: 5, order_name: "第五志愿" },
    ]

    let chooseDialogActive = ref(false)
    let chooseDialogItem = ref({} as curriculumInfo)
    let chooseDialogOrder = ref()
    let chooseDialogOrderList = ref(
        [] as {
            order_id: number
            order_name: string
        }[]
    )
    let chooseDialogIntroduction = ref("")

    function openChooseDialog(item: curriculumInfo) {
        // 预选阶段
        chooseDialogItem.value = item
        chooseDialogOrder.value = undefined
        // 可选的志愿首先要限制最大选择数量
        if (item.course_type === 3) {
            // 体育
            chooseDialogOrderList.value = orderList
        } else {
            // 非体育
            chooseDialogOrderList.value = orderList.slice(0, 3)
        }
        chooseDialogOrderList.value = chooseDialogOrderList.value.filter(
            (order) =>
                !studentCurriculums.value.some(
                    (choice) =>
                        choice.curriculum_course_id === item.curriculum_course_id &&
                        choice.choice_order === order.order_id
                )
        )
        chooseDialogIntroduction.value = ""
        chooseDialogActive.value = true
    }

    watch(chooseDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCurriculums()
        }
    })

    let chooseDialogSubmitLoading = ref(false)

    function onChooseDialogSubmitClick() {
        chooseDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Choice",
            "addChoice",
            {
                student_id: token.id,
                curriculum_id: chooseDialogItem.value.curriculum_id,
                order: chooseDialogItem.value.course_type === 4 ? 1 : chooseDialogOrder.value,
                introduction: !!chooseDialogIntroduction.value ? chooseDialogIntroduction.value : null,
            },
            (data) => {
                emitter.emit("success_snackbar", "选课成功")
                chooseDialogSubmitLoading.value = false
                chooseDialogActive.value = false
            },
            (errCode) => {
                chooseDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
