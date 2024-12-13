<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">学院教务管理</p>
        <p class="text-subtitle-2 mb-4">查看和管理学院教务</p>

        <v-data-table
            :headers="headers"
            :items="faculties"
            :loading="tableLoading"
            disable-sort
            sticky
            items-per-page="50"
            loading-text="加载中">
            <template v-slot:item.faculty_gender="{ item }">
                {{ item.faculty_gender ? item.faculty_gender : "无" }}
            </template>
            <template v-slot:item.faculty_phone="{ item }">
                {{ item.faculty_phone ? item.faculty_phone : "无" }}
            </template>
            <template v-slot:item.faculty_department_name="{ item }">
                {{ env.getDepartmentInfo(item.faculty_department_id)?.department_name }}
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn variant="tonal" density="comfortable" color="blue" class="me-1" @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                    修改
                </v-btn>
                <v-btn
                    v-if="item.login_is_enable"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="openEnableDialog(item)">
                    <v-icon size="default"> mdi-close </v-icon>
                    暂停登录
                </v-btn>
                <v-btn
                    v-else
                    variant="tonal"
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="openEnableDialog(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                    启用登录
                </v-btn>
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowPage" :length="allPages"></v-pagination>
                </div>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加学院教务"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="enableDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="enableDialogActive = false" />
                <v-toolbar-title
                    >{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}学院教务登录权限</v-toolbar-title
                >
            </v-toolbar>
            <v-card-item>
                确定要{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}学院教务“{{
                    enableDialogItem.faculty_name
                }}”的登录权限？
            </v-card-item>

            <template v-slot:actions>
                <v-btn @click="enableDialogActive = false">取消</v-btn>
                <v-btn
                    :color="enableDialogItem.login_is_enable ? 'red' : 'green'"
                    :loading="enableDialogSubmitLoading"
                    @click="onEnableDialogSubmitClick">
                    {{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>修改学院教务信息</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 工号：{{ modifyDialogItem.faculty_id }} </v-card-item>
            <v-text-field
                v-model="modifyDialogFacultyName"
                :rules="[(v) => !!v || '请输入姓名']"
                label="姓名"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="modifyDialogFacultyGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男或女']"
                label="性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field v-model="modifyDialogFacultyPhone" label="联系方式" variant="outlined" class="mx-2 mb-1" />
            <v-select
                v-model="modifyDialogFacultyDepartmentId"
                :rules="[(v) => !!v || '请选择所属学院']"
                :items="env.department"
                item-title="department_name"
                item-value="department_id"
                label="所属学院"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="blue"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogFacultyName == '' || modifyDialogFacultyDepartmentId == undefined"
                    @click="onModifyialogSubmitClick">
                    修改
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加学院教务</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogFacultyId"
                :rules="[(v) => !!v || '请输入工号']"
                label="工号"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="addDialogFacultyName"
                :rules="[(v) => !!v || '请输入姓名']"
                label="姓名"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field
                v-model="addDialogFacultyGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男，或女']"
                label="性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field v-model="addDialogFacultyPhone" label="联系方式" variant="outlined" class="mx-2 mb-1" />
            <v-select
                v-model="addDialogFacultyDepartmentId"
                :rules="[(v) => !!v || '请选择所属学院']"
                :items="env.department"
                item-title="department_name"
                item-value="department_id"
                label="所属学院"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogFacultyId == '' ||
                        addDialogFacultyName == '' ||
                        addDialogFacultyDepartmentId == undefined
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="FacultyManagement">
    import { useEnv } from "@/stores/env"
    import type { queryFacultyResponse, facultyInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "工号", key: "faculty_id" },
        { title: "姓名", key: "faculty_name" },
        { title: "性别", key: "faculty_gender" },
        { title: "联系方式", key: "faculty_phone" },
        { title: "学院", key: "faculty_department_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()

    let faculties = ref([] as facultyInfo[])
    let tableLoading = ref(false)
    let nowPage = ref(1)
    let allPages = ref(1)

    function queryFaculty() {
        tableLoading.value = true
        callapi.get(
            "Admin",
            "queryFaculty",
            { page: nowPage.value },
            (data) => {
                const result = <queryFacultyResponse>data
                allPages.value = Math.ceil(result.count / 50)
                faculties.value = result.faculties
                tableLoading.value = false
            },
            (errCode) => {
                tableLoading.value = false
            }
        )
    }

    onMounted(() => {
        queryFaculty()
    })

    watch(nowPage, () => {
        queryFaculty()
    })

    // ===== Enable Dialog =====
    let enableDialogActive = ref(false)
    let enableDialogItem = ref({} as facultyInfo)

    function openEnableDialog(item: facultyInfo) {
        enableDialogItem.value = item
        enableDialogActive.value = true
    }

    watch(enableDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryFaculty()
        }
    })

    let enableDialogSubmitLoading = ref(false)

    function onEnableDialogSubmitClick() {
        enableDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "toggleLoginEnable",
            {
                username: enableDialogItem.value.faculty_id,
            },
            (data) => {
                emitter.emit(
                    "success_snackbar",
                    "学院教务登录权限" + (enableDialogItem.value.login_is_enable ? "停用" : "启用") + "成功"
                )
                enableDialogSubmitLoading.value = false
                enableDialogActive.value = false
            },
            (errCode) => {
                enableDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as facultyInfo)
    let modifyDialogFacultyName = ref("")
    let modifyDialogFacultyGender = ref("" as string | null)
    let modifyDialogFacultyPhone = ref("" as string | null)
    let modifyDialogFacultyDepartmentId = ref()

    function openModifyDialog(item: facultyInfo) {
        modifyDialogItem.value = item
        modifyDialogFacultyName.value = item.faculty_name
        modifyDialogFacultyGender.value = item.faculty_gender
        modifyDialogFacultyPhone.value = item.faculty_phone
        modifyDialogFacultyDepartmentId.value = item.faculty_department_id
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryFaculty()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "updateFaculty",
            {
                faculty_id: modifyDialogItem.value.faculty_id,
                faculty_name: modifyDialogFacultyName.value,
                faculty_gender: !!modifyDialogFacultyGender.value ? modifyDialogFacultyGender.value : null,
                faculty_phone: !!modifyDialogFacultyPhone.value ? modifyDialogFacultyPhone.value : null,
                faculty_department_id: modifyDialogFacultyDepartmentId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学院教务修改成功")
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
    let addDialogFacultyId = ref("")
    let addDialogFacultyName = ref("")
    let addDialogFacultyGender = ref("")
    let addDialogFacultyPhone = ref("")
    let addDialogFacultyDepartmentId = ref()

    function openAddDialog() {
        addDialogFacultyId.value = ""
        addDialogFacultyName.value = ""
        addDialogFacultyGender.value = ""
        addDialogFacultyPhone.value = ""
        addDialogFacultyDepartmentId.value = undefined
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryFaculty()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addFaculty",
            {
                faculty_id: addDialogFacultyId.value,
                faculty_name: addDialogFacultyName.value,
                faculty_gender: !!addDialogFacultyGender.value ? addDialogFacultyGender.value : null,
                faculty_phone: !!addDialogFacultyPhone.value ? addDialogFacultyPhone.value : null,
                faculty_department_id: addDialogFacultyDepartmentId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学院教务添加成功")
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
