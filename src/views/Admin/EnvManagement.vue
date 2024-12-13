<template>
    <v-container class="my-3">
        <v-card prepend-icon="mdi-cogs" title="学期设置" max-width="600px" location="bottom" class="mb-10">
            <v-divider />
            <v-select
                v-model="newSemester"
                :rules="[(v) => !!v || '请选择需要设置的学期']"
                :items="env.semester"
                item-title="semester_name"
                item-value="semester_id"
                :placeholder="env.getSemesterInfo(env.env.now_semester_id)?.semester_name"
                persistent-placeholder
                label="即将设置成的学期"
                variant="outlined"
                clearable
                class="mx-2 mt-4" />
            <v-card-actions>
                <v-btn color="red" block variant="tonal" :disabled="!newSemester" @click="onChangeSemesterClick"
                    >修改</v-btn
                >
            </v-card-actions>
        </v-card>

        <v-card prepend-icon="mdi-cogs" title="选课阶段设置" max-width="600px" location="bottom" class="mb-10">
            <v-divider />
            <v-select
                v-model="nowStep"
                :rules="[(v) => !!v || v === 0 || '请选择需要设置的选课阶段']"
                :items="steps"
                item-title="step_name"
                item-value="step_id"
                :placeholder="env.getStepString"
                persistent-placeholder
                label="即将设置成的选课阶段"
                variant="outlined"
                clearable
                class="mx-2 mt-4" />
            <v-card-actions>
                <v-btn
                    color="red"
                    block
                    variant="tonal"
                    :disabled="!nowStep && !(nowStep === 0)"
                    @click="onChangeStepClick"
                    >修改</v-btn
                >
            </v-card-actions>
        </v-card>

        <v-card
            v-if="env.env.now_step === 2"
            prepend-icon="mdi-cogs"
            title="课程抽签"
            max-width="600px"
            location="bottom">
            <v-divider />
            <v-card-actions>
                <v-btn color="primary" block variant="tonal" @click="onDrawingCourseClick">全部课程抽签</v-btn>
            </v-card-actions>
            <v-card-item v-if="drawingProgressShow">
                <p class="mb-2">抽签进度</p>
                <p class="mb-2">已抽签/全部课程：{{ drawingFinished }} / {{ courses.length }}</p>
                <v-progress-linear v-model="drawingProgress" color="primary" rounded height="15" />
            </v-card-item>
        </v-card>
    </v-container>
</template>

<script lang="ts" setup name="EnvManagement">
    import { useEnv } from "@/stores/env"
    import type { courseInfo, queryCoursesResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { computed, onMounted, ref } from "vue"

    const env = useEnv()

    let newSemester = ref()

    function onChangeSemesterClick() {
        callapi.post(
            "json",
            "Admin",
            "setEnvSemester",
            {
                semester_id: newSemester.value,
            },
            (data) => {
                newSemester.value = undefined
                envManager.updateEnv()
            }
        )
    }

    const steps: {
        step_id: number
        step_name: string
    }[] = [
        { step_id: 0, step_name: "预选未开始" },
        { step_id: 1, step_name: "预选时间段" },
        { step_id: 2, step_name: "正在抽签" },
        { step_id: 3, step_name: "抽签结束" },
        { step_id: 4, step_name: "退改时间段" },
        { step_id: 5, step_name: "退改已结束" },
        { step_id: 6, step_name: "本学期已结束" },
    ]

    let nowStep = ref()

    function onChangeStepClick() {
        callapi.post(
            "json",
            "Admin",
            "setEnvStep",
            {
                step: nowStep.value,
            },
            (data) => {
                nowStep.value = undefined
                envManager.updateEnv()
            }
        )
    }

    let courses = ref([] as courseInfo[])

    function queryCourses() {
        callapi.get("Course", "queryCourses", {}, (data) => {
            const result = <queryCoursesResponse>data
            courses.value = result.courses
        })
    }

    onMounted(() => {
        queryCourses()
    })

    let drawingProgressShow = ref(false)
    let drawingFinished = ref(0)
    let drawingProgress = ref(0.0)

    function onDrawingCourseClick() {
        if (courses.value.length === 0) {
            emitter.emit("normalerror", "没有课程可以抽签")
        } else {
            drawingFinished.value = 0
            drawingProgress.value = 0.0
            drawingProgressShow.value = true
            setTimeout(() => {
                callDrawingCourse()
            }, 1000)
        }
    }

    function callDrawingCourse() {
        callapi.post(
            "json",
            "Choice",
            "drawingCourse",
            {
                semester_id: env.env.now_semester_id,
                course_id: courses.value[drawingFinished.value].course_id,
            },
            (data) => {
                drawingFinished.value++
                drawingProgress.value = (drawingFinished.value / courses.value.length) * 100
                if (drawingFinished.value < courses.value.length) {
                    callDrawingCourse()
                } else {
                    emitter.emit("success_snackbar", "课程抽签完成")
                    queryCourses()
                }
            }
        )
    }
</script>

<style scoped></style>
