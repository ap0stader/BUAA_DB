<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">学期管理</p>
        <p class="text-subtitle-2 mb-4">查看、查看管理学期</p>

        <v-data-table :headers="headers" :items="env.semester" disable-sort sticky> </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加学期"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加学期</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogSemesterName"
                :rules="[(v) => !!v || '请输入新学期名称']"
                label="新学期名称"
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="addDialogSemesterName == ''"
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="SemesterManagement">
    import { useEnv } from "@/stores/env"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "学期编号  ", key: "semester_id" },
        { title: "学期名称", key: "semester_name" },
    ]

    const env = useEnv()

    onMounted(() => {
        envManager.updateSemester()
    })

    // ===== Add Dialog =====
    let addDialogActive = ref(false)
    let addDialogSemesterName = ref("")

    function openAddDialog() {
        addDialogSemesterName.value = ""
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updateSemester()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addSemester",
            {
                semester_name: addDialogSemesterName.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学期添加成功")
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
