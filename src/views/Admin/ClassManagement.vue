<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">班级管理</p>
        <p class="text-subtitle-2 mb-4">查看和管理班级</p>

        <v-data-table
            :headers="headers"
            :items="
                token.isFaculty
                    ? env.class.filter((item) => item.class_department_id == token.getDepartmentId)
                    : env.class
            "
            disable-sort
            sticky
            items-per-page="25">
            <template v-slot:item.class_major_name="{ item }">
                {{ env.getMajorInfo(item.class_major_id)?.major_name }}
            </template>
            <template v-slot:item.class_department_name="{ item }">
                {{ env.getDepartmentInfo(item.class_department_id)?.department_name }}
            </template>
            <template v-slot:item.class_headmaster_name="{ item }">
                {{ item.class_headmaster_name ? item.class_headmaster_name : "无" }}
            </template>
            <template v-slot:item.actions="{ item }">
                <v-btn variant="tonal" density="comfortable" color="blue" class="me-1" @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                    修改
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加班级"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>修改班级班主任</v-toolbar-title>
            </v-toolbar>
            <v-card-item>
                班级原班主任：{{
                    modifyDialogItem.class_headmaster_name ? modifyDialogItem.class_headmaster_name : "无"
                }}
            </v-card-item>

            <v-text-field
                v-model="modifyDialogHeadmasterId"
                :rules="[(v) => !!v || '请输入新班主任工号']"
                placeholder="无"
                persistent-placeholder
                label="新班主任工号"
                variant="outlined"
                class="ma-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="blue"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogHeadmasterId == ''"
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
                <v-toolbar-title>添加班级</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogClassId"
                :rules="[(v) => !!v || '请输入班级号', (v) => parseInt(v) > 0 || '班级号必须为非负整数']"
                label="班级号"
                type="number"
                hide-spin-buttons
                variant="outlined"
                class="ma-2 mb-1" />

            <v-select
                v-model="addDialogMajorId"
                :rules="[(v) => !!v || '请选择所属专业']"
                :items="
                    token.isFaculty
                        ? env.major.filter((item) => item.major_department_id == token.getDepartmentId)
                        : env.major
                "
                item-title="major_name"
                item-value="major_id"
                label="所属专业"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogClassId == '' || parseInt(addDialogClassId) <= 0 || addDialogMajorId == undefined
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ClassManagement">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { classInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "班级号", key: "class_id" },
        { title: "所属专业", key: "class_major_name" },
        { title: "所属学院", key: "class_department_name" },
        { title: "班级班主任", key: "class_headmaster_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    onMounted(() => {
        envManager.updateClass()
    })

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as classInfo)
    let modifyDialogHeadmasterId = ref()

    function openModifyDialog(item: classInfo) {
        modifyDialogItem.value = item
        modifyDialogHeadmasterId.value = item.class_headmaster_id
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updateClass()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyDialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "updateClassHeadmaster",
            {
                class_id: modifyDialogItem.value.class_id,
                class_headmaster_id: !!modifyDialogHeadmasterId.value ? modifyDialogHeadmasterId.value : null,
            },
            (data) => {
                emitter.emit("success_snackbar", "班级班主任修改成功")
                modifyDialogSubmitLoading.value = false
                modifyDialogActive.value = false
            },
            (errCode) => {
                modifyDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Add Dialog =====
    let addDialogActive = ref(false)
    let addDialogClassId = ref("")
    let addDialogMajorId = ref()

    function openAddDialog() {
        addDialogClassId.value = ""
        addDialogMajorId.value = undefined
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updateClass()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addClass",
            {
                class_id: parseInt(addDialogClassId.value),
                class_major_id: addDialogMajorId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "班级添加成功")
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
