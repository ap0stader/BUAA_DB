<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">成绩查看</p>
        <p class="text-subtitle-2 mb-4">查看学院、专业、班级成绩</p>

        <v-chip-group
            v-model="selectedExtent"
            mandatory
            selected-class="bg-green-darken-3"
            :disabled="!token.getDepartmentId">
            <v-label class="mr-5">查看范围</v-label>
            <v-chip v-for="item in extent" :key="item.extent_id" :value="item.extent_id" size="large">
                {{ item.extent_name }}
            </v-chip>
        </v-chip-group>

        <!-- 使用name是因为只能用字符串匹配 -->
        <v-select
            v-if="selectedExtent === 2"
            v-model="selectedMajor"
            :items="env.major.filter((m) => m.major_department_id === token.getDepartmentId)"
            item-title="major_name"
            item-value="major_id"
            persistent-placeholder
            label="查看专业"
            variant="outlined"
            max-width="500px"
            clearable
            class="mt-4" />

        <!-- 使用name是因为只能用字符串匹配 -->
        <v-select
            v-if="selectedExtent === 3"
            v-model="selectedClass"
            :items="env.class.filter((c) => c.class_department_id === token.getDepartmentId)"
            item-title="class_id"
            item-value="class_id"
            persistent-placeholder
            label="查看班级"
            variant="outlined"
            max-width="500px"
            clearable
            class="mt-4" />

        <v-data-table
            v-if="
                selectedExtent === 1 ||
                (selectedExtent === 2 && selectedMajor) ||
                (selectedExtent === 3 && selectedClass)
            "
            :headers="headers"
            :items="statistics"
            sticky
            items-per-page="50">
            <template v-slot:item.student_major_name="{ item }">
                {{ env.getMajorInfo(item.student_major_id)?.major_name }}
            </template>
            <template v-slot:item.student_department_name="{ item }">
                {{ env.getDepartmentInfo(item.student_department_id)?.department_name }}
            </template>
            <template v-slot:item.weighted_average="{ item }">
                {{ item.weighted_average ? item.weighted_average.toFixed(2) : "暂无" }}
            </template>
            <template v-slot:item.average="{ item }">
                {{ item.average ? item.average.toFixed(2) : "暂无" }}
            </template>
            <template v-slot:item.gpa="{ item }">
                {{ item.gpa ? item.gpa.toFixed(4) : "暂无" }}
            </template>
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="FacultyScore">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { queryScoreStatisticsResponse, scoreStatisticsInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { ref, watch } from "vue"

    const extent: {
        extent_id: number
        extent_name: string
    }[] = [
        { extent_id: 1, extent_name: "学院" },
        { extent_id: 2, extent_name: "专业" },
        { extent_id: 3, extent_name: "班级" },
    ]

    const headers = [
        { title: "学号", key: "student_id", sortable: false },
        { title: "姓名", key: "student_name", sortable: false },
        { title: "班级", key: "student_class_id", sortable: false },
        { title: "专业", key: "student_major_name", sortable: false },
        { title: "学院", key: "student_department_name", sortable: false },
        { title: "加权平均分", key: "weighted_average" },
        { title: "算数平均分", key: "average" },
        { title: "GPA", key: "gpa" },
    ]

    const env = useEnv()
    const token = useToken()

    let selectedExtent = ref()
    let selectedMajor = ref()
    let selectedClass = ref()

    let statistics = ref([] as scoreStatisticsInfo[])

    function queryDepartmentScoreStatistics() {
        callapi.get(
            "Faculty",
            "queryDepartmentScoreStatistics",
            {
                department_id: token.getDepartmentId,
            },
            (data) => {
                const result = <queryScoreStatisticsResponse>data
                statistics.value = result.statistics
            }
        )
    }

    function queryMajorScoreStatistics() {
        callapi.get(
            "Faculty",
            "queryMajorScoreStatistics",
            {
                major_id: selectedMajor.value,
            },
            (data) => {
                const result = <queryScoreStatisticsResponse>data
                statistics.value = result.statistics
            }
        )
    }

    function queryClassScoreStatistics() {
        callapi.get(
            "Faculty",
            "queryClassScoreStatistics",
            {
                class_id: selectedClass.value,
            },
            (data) => {
                const result = <queryScoreStatisticsResponse>data
                statistics.value = result.statistics
            }
        )
    }

    watch(selectedExtent, (newValue) => {
        statistics.value = []
        selectedMajor.value = undefined
        selectedClass.value = undefined
        if (newValue === 1) {
            queryDepartmentScoreStatistics()
        }
    })

    watch(selectedMajor, (newValue) => {
        statistics.value = []
        if (newValue) {
            queryMajorScoreStatistics()
        }
    })

    watch(selectedClass, (newValue) => {
        statistics.value = []
        if (newValue) {
            queryClassScoreStatistics()
        }
    })
</script>

<style scoped></style>
