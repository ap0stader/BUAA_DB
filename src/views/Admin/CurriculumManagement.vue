<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">教学班管理</p>
        <p class="text-subtitle-2 mb-4">查看、管理教学班</p>

        <v-data-table
            :headers="headers"
            :items="
                token.isFaculty
                    ? curriculums.filter((item) => item.curriculum_teacher_department_id == token.getDepartmentId)
                    : curriculums
            "
            disable-sort
            sticky
            items-per-page="50">
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

            <template v-slot:item.curriculum_utilization_string="{ item }">
                {{ item.curriculum_utilization_string ? item.curriculum_utilization_string : "暂未分配" }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn
                    variant="tonal"
                    density="comfortable"
                    color="deep-purple-lighten-2"
                    class="me-1"
                    @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                    修改教学班容量
                </v-btn>
                <v-btn variant="tonal" density="comfortable" color="green" class="me-1" @click="openAddDialog(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                    分配场地资源
                </v-btn>
                <v-btn
                    v-if="item.curriculum_utilization_resources.length > 0"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="onReleaseCurriculumResourceClick(item)">
                    <v-icon size="default"> mdi-close </v-icon>
                    收回场地资源
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>修改教学班容量</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 教学班编号： {{ modifyDialogItem.curriculum_id }} </v-card-item>

            <v-text-field
                v-model="modifyDialogCurriculumCapacity"
                :rules="[(v) => !!v || '请输入新的教学班容量', (v) => parseInt(v) > 0 || '教学班容量必须为非负整数']"
                label="新的教学班容量"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="purple"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogCurriculumCapacity == '' || parseInt(modifyDialogCurriculumCapacity) < 0"
                    @click="onModifyDialogSubmitClick">
                    修改
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>分配场地资源</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 教学班编号：{{ addDialogItem.curriculum_id }} </v-card-item>

            <v-select
                v-model="addDialogPlaceId"
                :rules="[(v) => !!v || '请选择场地']"
                :items="env.place"
                item-title="place_name"
                item-value="place_id"
                label="场地"
                variant="outlined"
                clearable
                class="ma-2 mb-1" />
            <v-range-slider
                v-model="addDialogWeeks"
                min="1"
                max="18"
                step="1"
                color="primary"
                thumb-label="always"
                label="周次"
                class="mx-6 mt-4 mb-1" />
            <v-select
                v-model="addDialogWeekday"
                :rules="[(v) => !!v || '请选择上课日']"
                :items="weekdays"
                item-title="weekday_name"
                item-value="weekday_id"
                label="上课日"
                variant="outlined"
                clearable
                class="ma-2 mb-1" />
            <v-range-slider
                v-model="addDialogLessons"
                min="1"
                max="14"
                step="1"
                color="primary"
                thumb-label="always"
                label="节次"
                class="mx-6 mt-4 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="green"
                    :loading="addDialogSubmitLoading"
                    :disabled="addDialogPlaceId == ''"
                    @click="onAddDialogSubmitClick">
                    分配
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="CurriculumManagement">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { curriculumInfo, queryCurriculumsResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "教学班编号", key: "curriculum_id" },
        { title: "开设学期", key: "curriculum_semester_name" },
        { title: "开设老师", key: "curriculum_teacher_name" },
        { title: "课程名称", key: "course_name" },
        { title: "课程类型", key: "course_type_string" },
        { title: "教学班容量", key: "curriculum_capacity" },
        { title: "教学班说明", key: "curriculum_info" },
        { title: "上课时间与地点", key: "curriculum_utilization_string" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let curriculums = ref([] as curriculumInfo[])

    function queryCurriculums() {
        callapi.get("Course", "queryCurriculums", {}, (data) => {
            const result = <queryCurriculumsResponse>data
            curriculums.value = result.curriculums
        })
    }

    onMounted(() => {
        queryCurriculums()
    })

    function onReleaseCurriculumResourceClick(item: curriculumInfo) {
        callapi.post("json", "Course", "releaseCurriculumResource", { curriculum_id: item.curriculum_id }, () => {
            emitter.emit("success_snackbar", "收回场地资源成功")
            queryCurriculums()
        })
    }

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as curriculumInfo)
    let modifyDialogCurriculumCapacity = ref()

    function openModifyDialog(item: curriculumInfo) {
        modifyDialogItem.value = item
        modifyDialogCurriculumCapacity.value = item.curriculum_capacity
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCurriculums()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyDialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Course",
            "updateCurriculumCapacity",
            {
                curriculum_id: modifyDialogItem.value.curriculum_id,
                curriculum_capacity: modifyDialogCurriculumCapacity.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "教学班容量修改成功")
                modifyDialogSubmitLoading.value = false
                modifyDialogActive.value = false
            },
            (errCode) => {
                modifyDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Add Dialog =====
    const weekdays: {
        weekday_name: string
        weekday_id: number
    }[] = [
        { weekday_name: "星期一", weekday_id: 1 },
        { weekday_name: "星期二", weekday_id: 2 },
        { weekday_name: "星期三", weekday_id: 3 },
        { weekday_name: "星期四", weekday_id: 4 },
        { weekday_name: "星期五", weekday_id: 5 },
        { weekday_name: "星期六", weekday_id: 6 },
        { weekday_name: "星期日", weekday_id: 7 },
    ]
    let addDialogActive = ref(false)
    let addDialogItem = ref({} as curriculumInfo)
    let addDialogPlaceId = ref()
    let addDialogWeeks = ref([] as number[])
    let addDialogWeekday = ref()
    let addDialogLessons = ref([] as number[])

    function openAddDialog(item: curriculumInfo) {
        addDialogItem.value = item
        addDialogPlaceId.value = undefined
        addDialogWeeks.value = [1, 8]
        addDialogWeekday.value = undefined
        addDialogLessons.value = [3, 4]
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryCurriculums()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function generateAcquireResources(): number[] {
        let result = [] as number[]
        for (let week = addDialogWeeks.value[0]; week <= addDialogWeeks.value[1]; week++) {
            for (let lesson = addDialogLessons.value[0]; lesson <= addDialogLessons.value[1]; lesson++) {
                result.push((addDialogPlaceId.value << 16) | (week << 8) | (addDialogWeekday.value << 4) | lesson)
            }
        }
        return result
    }

    function onAddDialogSubmitClick() {
        console.log(generateAcquireResources())
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Course",
            "setCurriculumResource",
            {
                curriculum_id: addDialogItem.value.curriculum_id,
                acquire_resources: generateAcquireResources().concat(
                    addDialogItem.value.curriculum_utilization_resources
                ),
            },
            () => {
                emitter.emit("success_snackbar", "场地资源分配成功")
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
