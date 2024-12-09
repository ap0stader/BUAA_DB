<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">专业管理</p>
        <p class="text-subtitle-2 mb-4">查看、查看管理专业</p>

        <v-data-table :headers="headers" :items="env.major" disable-sort sticky items-per-page="25"> </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加专业"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加专业</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogMajorId"
                :rules="[(v) => !!v || '请输入新专业专业号', (v) => parseInt(v) > 0 || '专业专业号必须为非负整数']"
                label="新专业专业号"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2" />

            <v-text-field
                v-model="addDialogMajorName"
                :rules="[(v) => !!v || '请输入新专业名称']"
                label="新专业名称"
                variant="outlined"
                class="ma-2" />

            <v-select
                v-model="addDialogDepartmentId"
                :rules="[(v) => !!v || '请选择新专业所属学院']"
                :items="env.department"
                item-title="department_name"
                item-value="department_id"
                label="新专业所属学院"
                variant="outlined"
                clearable
                class="ma-2" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogMajorId == '' ||
                        parseInt(addDialogMajorId) <= 0 ||
                        addDialogDepartmentId == undefined ||
                        addDialogMajorName == ''
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="MajorManagement">
    import { useEnv } from "@/stores/env"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "ID", key: "major_id" },
        { title: "专业名称", key: "major_name" },
    ]

    const env = useEnv()

    onMounted(() => {
        envManager.updateMajor()
    })

    // ===== Add Dialog =====
    let addDialogActive = ref(false)
    let addDialogMajorId = ref("")
    let addDialogMajorName = ref("")
    let addDialogDepartmentId = ref()

    function openAddDialog() {
        addDialogMajorId.value = ""
        addDialogMajorName.value = ""
        addDialogDepartmentId.value = undefined
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updateMajor()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addMajor",
            {
                major_id: parseInt(addDialogMajorId.value),
                major_name: addDialogMajorName.value,
                major_department_id: addDialogDepartmentId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "专业添加成功")
                addDialogSubmitLoading.value = false
                addDialogActive.value = false
            },
            (errCode) => {
                addDialogSubmitLoading.value = false
            }
        )
    }
</script>

<style scoped></style>
