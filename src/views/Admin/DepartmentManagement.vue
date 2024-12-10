<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">学院管理</p>
        <p class="text-subtitle-2 mb-4">查看、查看管理学院</p>

        <v-data-table :headers="headers" :items="env.department" disable-sort sticky> </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加学院"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加学院</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogDepartmentId"
                :rules="[(v) => !!v || '请输入新学院系号', (v) => parseInt(v) > 0 || '学院系号必须为非负整数']"
                label="新学院系号"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2 mb-0" />

            <v-text-field
                v-model="addDialogDepartmentName"
                :rules="[(v) => !!v || '请输入新学院名称']"
                label="新学院名称"
                variant="outlined"
                class="mx-2" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogDepartmentId == '' ||
                        parseInt(addDialogDepartmentId) <= 0 ||
                        addDialogDepartmentName == ''
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="DepartmentManagement">
    import { useEnv } from "@/stores/env"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "院系号", key: "department_id" },
        { title: "学院名称", key: "department_name" },
    ]

    const env = useEnv()

    onMounted(() => {
        envManager.updateDepartment()
    })

    // ===== Add Dialog =====
    let addDialogActive = ref(false)
    let addDialogDepartmentId = ref("")
    let addDialogDepartmentName = ref("")

    function openAddDialog() {
        addDialogDepartmentId.value = ""
        addDialogDepartmentName.value = ""
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updateDepartment()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addDepartment",
            {
                department_id: parseInt(addDialogDepartmentId.value),
                department_name: addDialogDepartmentName.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学院添加成功")
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
