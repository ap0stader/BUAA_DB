<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">学生管理</p>
        <p class="text-subtitle-2 mb-4">查看和管理学生</p>

        <v-data-table
            :headers="headers"
            :items="students"
            :loading="tableLoading"
            disable-sort
            sticky
            items-per-page="50"
            loading-text="加载中">
            <template v-slot:item.student_gender="{ item }">
                {{ item.student_gender ? item.student_gender : "无" }}
            </template>
            <template v-slot:item.student_phone="{ item }">
                {{ item.student_phone ? item.student_phone : "无" }}
            </template>
            <template v-slot:item.student_major_name="{ item }">
                {{ env.getMajorInfo(item.student_major_id)?.major_name }}
            </template>
            <template v-slot:item.student_department_name="{ item }">
                {{ env.getDepartmentInfo(item.student_department_id)?.department_name }}
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
        v-if="token.isSuperAdmin"
        color="purple"
        prepend-icon="mdi-plus-box-multiple-outline"
        location="top end"
        size="x-large"
        position="sticky"
        text="批量添加学生"
        extended
        app
        @click="openAddBatchDialog"
        class="mt-4" />

    <v-fab
        v-if="token.isSuperAdmin"
        color="primary"
        prepend-icon="mdi-plus"
        location="bottom end"
        size="x-large"
        position="sticky"
        text="添加学生"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="enableDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="enableDialogActive = false" />
                <v-toolbar-title>{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}学生登录权限</v-toolbar-title>
            </v-toolbar>
            <v-card-item>
                确定要{{ enableDialogItem.login_is_enable ? "暂停" : "启用" }}学生“{{
                    enableDialogItem.student_name
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

    <v-dialog max-width="500px" v-model="addBatchDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addBatchDialogActive = false" />
                <v-toolbar-title>批量添加学生</v-toolbar-title>
            </v-toolbar>
            <v-file-input
                v-model="addBatchDialogFile"
                :rules="[(v) => !!v.length || '请选择文件']"
                accept=".xlsx"
                label="请选择填写后的批量添加学生模板文件"
                variant="outlined"
                clearable
                class="ma-2 mb-1" />

            <v-list v-if="addBatchDialogFailedInfo.length > 0" lines="two" density="compact" slim class="ma-2 mt-0">
                <v-list-subheader color="red">以下学生的数据存在问题：</v-list-subheader>
                <v-list-item
                    v-for="item in addBatchDialogFailedInfo"
                    :key="item.student_id"
                    :title="item.student_id"
                    :subtitle="
                        item.reason === 1 ? '有同学工号的人员' : item.reason === 2 ? '无此班级号对应的班级' : '未知原因'
                    " />
            </v-list>

            <template v-slot:actions>
                <v-btn @click="addBatchDialogActive = false">取消</v-btn>
                <v-btn
                    color="purple"
                    :loading="addBatchDialogSubmitLoading"
                    :disabled="addBatchDialogFile == null"
                    @click="onAddBatchDialogSubmitClick">
                    上传
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="modifyDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="modifyDialogActive = false" />
                <v-toolbar-title>修改学生信息</v-toolbar-title>
            </v-toolbar>
            <v-card-item> 学生学号：{{ modifyDialogItem.student_id }} </v-card-item>
            <v-text-field
                v-model="modifyDialogStudentName"
                :rules="[(v) => !!v || '请输入修改后的学生姓名']"
                label="修改后的学生姓名"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="modifyDialogStudentGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男或女']"
                label="修改后的学生性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field
                v-model="modifyDialogStudentPhone"
                label="修改后的学生联系方式"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-select
                v-model="modifyDialogStudentClassId"
                :rules="[(v) => !!v || '请选择修改后的学生所属班级']"
                :items="
                    token.isFaculty
                        ? env.class.filter((item) => item.class_department_id == token.getDepartmentId)
                        : env.class
                "
                item-title="class_id"
                item-value="class_id"
                label="修改后的学生所属班级"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="modifyDialogActive = false">取消</v-btn>
                <v-btn
                    color="red"
                    :loading="modifyDialogSubmitLoading"
                    :disabled="modifyDialogStudentName == '' || modifyDialogStudentClassId == undefined"
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
                <v-toolbar-title>添加学生</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogStudentId"
                :rules="[(v) => !!v || '请输入新学生学号']"
                label="新学生学号"
                variant="outlined"
                class="ma-2 mb-1" />
            <v-text-field
                v-model="addDialogStudentName"
                :rules="[(v) => !!v || '请输入新学生姓名']"
                label="新学生姓名"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field
                v-model="addDialogStudentGender"
                :rules="[(v) => !v || ['男', '女'].includes(v) || '性别必须为男，或女']"
                label="新学生性别"
                variant="outlined"
                class="mx-2 mb-1" />
            <v-text-field v-model="addDialogStudentPhone" label="新学生联系方式" variant="outlined" class="mx-2 mb-1" />
            <v-select
                v-model="addDialogStudentClassId"
                :rules="[(v) => !!v || '请选择新学生所属班级']"
                :items="env.class"
                item-title="class_id"
                item-value="class_id"
                label="新学生所属班级"
                variant="outlined"
                clearable
                class="mx-2 mb-1" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :loading="addDialogSubmitLoading"
                    :disabled="
                        addDialogStudentId == '' || addDialogStudentName == '' || addDialogStudentClassId == undefined
                    "
                    @click="onAddDialogSubmitClick">
                    添加
                </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="StudentManagement">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import type { addStudentBatchFailedInfo, addStudentBatchResponse, queryStudentResponse, studentInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "学号", key: "student_id" },
        { title: "姓名", key: "student_name" },
        { title: "性别", key: "student_gender" },
        { title: "联系方式", key: "student_phone" },
        { title: "班级", key: "student_class_id" },
        { title: "专业", key: "student_major_name" },
        { title: "学院", key: "student_department_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()
    const token = useToken()

    let students = ref([] as studentInfo[])
    let tableLoading = ref(false)
    let nowPage = ref(1)
    let allPages = ref(1)

    function queryStudent() {
        tableLoading.value = true
        callapi.get(
            "Admin",
            "queryStudent",
            { page: nowPage.value, department_id: token.getDepartmentId },
            (data) => {
                const result = <queryStudentResponse>data
                allPages.value = Math.ceil(result.count / 50)
                students.value = result.students
                tableLoading.value = false
            },
            (errCode) => {
                tableLoading.value = false
            }
        )
    }

    onMounted(() => {
        queryStudent()
    })

    watch(nowPage, () => {
        queryStudent()
    })

    // ===== Enable Dialog =====
    let enableDialogActive = ref(false)
    let enableDialogItem = ref({} as studentInfo)

    function openEnableDialog(item: studentInfo) {
        enableDialogItem.value = item
        enableDialogActive.value = true
    }

    watch(enableDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryStudent()
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
                username: enableDialogItem.value.student_id,
            },
            (data) => {
                emitter.emit(
                    "success_snackbar",
                    "学生登录权限" + (enableDialogItem.value.login_is_enable ? "停用" : "启用") + "成功"
                )
                enableDialogSubmitLoading.value = false
                enableDialogActive.value = false
            },
            (errCode) => {
                enableDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Add Batch Dialog =====
    let addBatchDialogActive = ref(false)
    let addBatchDialogFile = ref()

    function openAddBatchDialog() {
        addBatchDialogFile.value = undefined
        addBatchDialogActive.value = true
    }

    let addBatchDialogSubmitLoading = ref(false)
    let addBatchDialogFailedInfo = ref([] as addStudentBatchFailedInfo[])

    function onAddBatchDialogSubmitClick() {
        addBatchDialogSubmitLoading.value = true
        addBatchDialogFailedInfo.value = []
        callapi.post(
            "form-data",
            "Admin",
            "addStudentBatch",
            {
                file: addBatchDialogFile.value,
            },
            (data) => {
                const result = <addStudentBatchResponse>data
                addBatchDialogFailedInfo.value = result.failed_info
                if (result.failed_info.length > 0) {
                    emitter.emit("normalerror", "学生批量添加失败")
                } else {
                    emitter.emit("success_snackbar", "学生批量添加成功")
                    addBatchDialogActive.value = false
                }
                addBatchDialogSubmitLoading.value = false
            },
            (errCode) => {
                addBatchDialogSubmitLoading.value = false
            }
        )
    }

    // ===== Modify Dialog =====
    let modifyDialogActive = ref(false)
    let modifyDialogItem = ref({} as studentInfo)
    let modifyDialogStudentName = ref("")
    let modifyDialogStudentGender = ref("" as string | null)
    let modifyDialogStudentPhone = ref("" as string | null)
    let modifyDialogStudentClassId = ref()

    function openModifyDialog(item: studentInfo) {
        modifyDialogItem.value = item
        modifyDialogStudentName.value = item.student_name
        modifyDialogStudentGender.value = item.student_gender
        modifyDialogStudentPhone.value = item.student_phone
        modifyDialogStudentClassId.value = item.student_class_id
        modifyDialogActive.value = true
    }

    watch(modifyDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryStudent()
        }
    })

    let modifyDialogSubmitLoading = ref(false)

    function onModifyialogSubmitClick() {
        modifyDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "updateStudent",
            {
                student_id: modifyDialogItem.value.student_id,
                student_name: modifyDialogStudentName.value,
                student_gender: !!modifyDialogStudentGender.value ? modifyDialogStudentGender.value : null,
                student_phone: !!modifyDialogStudentPhone.value ? modifyDialogStudentPhone.value : null,
                student_class_id: modifyDialogStudentClassId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学生修改成功")
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
    let addDialogStudentId = ref("")
    let addDialogStudentName = ref("")
    let addDialogStudentGender = ref("")
    let addDialogStudentPhone = ref("")
    let addDialogStudentClassId = ref()

    function openAddDialog() {
        addDialogStudentId.value = ""
        addDialogStudentName.value = ""
        addDialogStudentGender.value = ""
        addDialogStudentPhone.value = ""
        addDialogStudentClassId.value = undefined
        addDialogActive.value = true
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            queryStudent()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addStudent",
            {
                student_id: addDialogStudentId.value,
                student_name: addDialogStudentName.value,
                student_gender: !!addDialogStudentGender.value ? addDialogStudentGender.value : null,
                student_phone: !!addDialogStudentPhone.value ? addDialogStudentPhone.value : null,
                student_class_id: addDialogStudentClassId.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "学生添加成功")
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
