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

        <v-card prepend-icon="mdi-cogs" title="选课阶段设置" max-width="600px" location="bottom">
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
    </v-container>
</template>

<script lang="ts" setup name="EnvManagement">
    import { useEnv } from "@/stores/env"
    import { callapi } from "@/utils/callapi"
    import { envManager } from "@/utils/envManager"
    import { ref } from "vue"

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
</script>

<style scoped></style>
