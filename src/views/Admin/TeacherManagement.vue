<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">教师管理</p>
        <p class="text-subtitle-2 mb-4">查看和管理教师</p>

        <v-data-table
            :headers="headers"
            :items="teachers"
            :loading="tableLoading"
            disable-sort
            sticky
            items-per-page="50"
            loading-text="加载中">
            <template v-slot:item.teacher_gender="{ item }">
                {{ item.teacher_gender ? item.teacher_gender : "无" }}
            </template>
            <template v-slot:item.teacher_phone="{ item }">
                {{ item.teacher_phone ? item.teacher_phone : "无" }}
            </template>
            <template v-slot:item.teacher_department_name="{ item }">
                {{ env.getDepartmentInfo(item.teacher_department_id)?.department_name }}
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn variant="tonal" density="comfortable" color="blue" class="me-1" @click="openModifyDialog(item)">
                    <v-icon size="default"> mdi-pencil </v-icon>
                    修改
                </v-btn>
                <v-btn
                    v-if="item.login_is_enable && token.isSuperAdmin"
                    variant="tonal"
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="openEnableDialog(item)">
                    <v-icon size="default"> mdi-close </v-icon>
                    暂停登录
                </v-btn>
                <v-btn
                    v-else-if="token.isSuperAdmin"
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
        text="添加教师"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="enableDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="enableDialogActive = false" />
                <v-toolbar-title>{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}教师登录权限</v-toolbar-title>
            </v-toolbar>
            <v-card-item>
                确定要{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}教师“{{
                    enableDialogItem.teacher_name
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
                <v-toolbar-title>修改教师信息</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 教师工号：{{ modifyDialogItem.teacher_id }} </v-card-item>
            <v-text-field
                v-model="modifyDialogTeacherName"
                :rules="[(v) => !!v || '请输入修改后的教师姓名']"
                label="修改后的教师姓名"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="modifyDialogTeacherGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男或女']"
                label="修改后的教师性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field
                v-model="modifyDialogTeacherPhone"
                label="修改后的教师联系方式"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-select
                v-model="modifyDialogTeacherDepartmentId"
                :rules="[(v) => !!v || '请选择修改后的教师所属学院']"
                :items="env.department"
                item-title="department_name"
                item-value="department_id"
                label="修改后的教师所属学院"
                variant="outlined"
                clearable
                :disabled="!token.isSuperAdmin"
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="red"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogTeacherName == '' || modifyDialogTeacherDepartmentId == undefined"
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
                <v-toolbar-title>添加教师</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogTeacherId"
                :rules="[(v) => !!v || '请输入新教师工号']"
                label="新教师工号"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="addDialogTeacherName"
                :rules="[(v) => !!v || '请输入新教师姓名']"
                label="新教师姓名"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field
                v-model="addDialogTeacherGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男，或女']"
                label="新教师性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field v-model="addDialogTeacherPhone" label="新教师联系方式" variant="outlined" class="mx-2 mb-1" />
            <v-select
                v-model="addDialogTeacherDepartmentId"
                :rules="[(v) => !!v || '请选择新教师所属专业']"
                :items="env.department"
                item-title="department_name"
                item-value="department_id"
                label="新教师所属专业"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogTeacherId == '' ||
                        addDialogTeacherName == '' ||
                        addDialogTeacherDepartmentId == undefined
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="TeacherManagement">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { queryTeacherResponse, teacherInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "工号", key: "teacher_id" },
        { title: "姓名", key: "teacher_name" },
        { title: "性别", key: "teacher_gender" },
        { title: "联系方式", key: "teacher_phone" },
        { title: "学院", key: "teacher_department_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let teachers = ref([] as teacherInfo[])
    let tableLoading = ref(false)
    let nowPage = ref(1)
    let allPages = ref(1)

    function queryTeacher() {
        tableLoading.value = true
        callapi.get(
            "Admin",
            "queryTeacher",
            { page: nowPage.value, department_id: token.getDepartmentId },
            (data) => {
                const result = <queryTeacherResponse>data
                allPages.value = Math.ceil(result.count / 50)
                teachers.value = result.teachers
                tableLoading.value = false
            },
            (errCode) => {
                tableLoading.value = false
            }
        )
    }

    onMounted(() => {
        queryTeacher()
    })

    watch(nowPage, () => {
        queryTeacher()
    })

    // ===== Enable Dialog =====
    let enableDialogActive = ref(false)
    let enableDialogItem = ref({} as teacherInfo)

    function openEnableDialog(item: teacherInfo) {
        enableDialogItem.value = item
        enableDialogActive.value = true
    }

    watch(enableDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryTeacher()
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
                username: enableDialogItem.value.teacher_id,
            },
            (data) => {
                emitter.emit(
                    "success_snackbar",
                    "教师登录权限" + (enableDialogItem.value.login_is_enable ? "停用" : "启用") + "成功"
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
    let modifyDialogItem = ref({} as teacherInfo)
    let modifyDialogTeacherName = ref("")
    let modifyDialogTeacherGender = ref("" as string | null)
    let modifyDialogTeacherPhone = ref("" as string | null)
    let modifyDialogTeacherDepartmentId = ref()

    function openModifyDialog(item: teacherInfo) {
        modifyDialogItem.value = item
        modifyDialogTeacherName.value = item.teacher_name
        modifyDialogTeacherGender.value = item.teacher_gender
        modifyDialogTeacherPhone.value = item.teacher_phone
        modifyDialogTeacherDepartmentId.value = item.teacher_department_id
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryTeacher()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "updateTeacher",
            {
                teacher_id: modifyDialogItem.value.teacher_id,
                teacher_name: modifyDialogTeacherName.value,
                teacher_gender: !!modifyDialogTeacherGender.value ? modifyDialogTeacherGender.value : null,
                teacher_phone: !!modifyDialogTeacherPhone.value ? modifyDialogTeacherPhone.value : null,
                teacher_department_id: modifyDialogTeacherDepartmentId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "教师修改成功")
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
    let addDialogTeacherId = ref("")
    let addDialogTeacherName = ref("")
    let addDialogTeacherGender = ref("")
    let addDialogTeacherPhone = ref("")
    let addDialogTeacherDepartmentId = ref()

    function openAddDialog() {
        addDialogTeacherId.value = ""
        addDialogTeacherName.value = ""
        addDialogTeacherGender.value = ""
        addDialogTeacherPhone.value = ""
        addDialogTeacherDepartmentId.value = undefined
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryTeacher()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addTeacher",
            {
                teacher_id: addDialogTeacherId.value,
                teacher_name: addDialogTeacherName.value,
                teacher_gender: !!addDialogTeacherGender.value ? addDialogTeacherGender.value : null,
                teacher_phone: !!addDialogTeacherPhone.value ? addDialogTeacherPhone.value : null,
                teacher_department_id: addDialogTeacherDepartmentId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "教师添加成功")
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
