<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">登录审计信息</p>

        <v-data-table :headers="loginHeaders" :items="loginAudits" disable-sort sticky items-per-page="50">
            <template v-slot:item.login_audit_result_string="{ item }">
                {{
                    item.login_audit_result === 0
                        ? "成功"
                        : item.login_audit_result === 1
                        ? "无此用户"
                        : item.login_audit_result === 2
                        ? "密码错误"
                        : item.login_audit_result === 3
                        ? "用户已被禁止登录"
                        : "其他结果"
                }}
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowLoginPage" :length="allLoginPages"></v-pagination>
                </div>
            </template>
        </v-data-table>

        <p class="text-h4 mt-6 mb-4">选课审计信息</p>

        <v-data-table :headers="selectionHeaders" :items="selectionAudits" disable-sort sticky items-per-page="50">
            <template v-slot:item.selection_audit_type_string="{ item }">
                {{
                    item.selection_audit_type === 0
                        ? "预选阶段预选"
                        : item.selection_audit_type === 1
                        ? "预选阶段退选"
                        : item.selection_audit_type === 2
                        ? "抽签中选"
                        : item.selection_audit_type === 3
                        ? "抽签落选"
                        : item.selection_audit_type === 4
                        ? "退改阶段选课或被选中"
                        : item.selection_audit_type === 5
                        ? "退改阶段退课"
                        : "其他操作"
                }}
            </template>

            <template v-slot:bottom>
                <div class="text-center mt-2">
                    <v-pagination v-model="nowSelectionPage" :length="allSelectionPages"></v-pagination>
                </div>
            </template>
        </v-data-table>
    </v-container>
</template>

<script lang="ts" setup name="AuditCenter">
    import type {
        loginAuditInfo,
        queryLoginAuditResponse,
        querySelectionAuditResponse,
        selectionAuditInfo,
    } from "@/types"
    import { callapi } from "@/utils/callapi"
    import { onMounted, ref, watch } from "vue"

    const loginHeaders = [
        { title: "审计信息编号", key: "login_audit_id" },
        { title: "尝试登录的用户名", key: "login_audit_claim" },
        { title: "登录时间", key: "login_audit_time" },
        { title: "登录结果", key: "login_audit_result_string" },
    ]

    let loginAudits = ref([] as loginAuditInfo[])
    let nowLoginPage = ref(1)
    let allLoginPages = ref(1)

    function queryLoginAudit() {
        callapi.get("Audit", "queryLoginAudit", { page: nowLoginPage.value }, (data) => {
            const result = <queryLoginAuditResponse>data
            allLoginPages.value = Math.ceil(result.count / 50)
            loginAudits.value = result.audits
        })
    }

    onMounted(() => {
        queryLoginAudit()
    })

    watch(nowLoginPage, () => {
        queryLoginAudit()
    })

    const selectionHeaders = [
        { title: "审计信息编号", key: "selection_audit_id" },
        { title: "学生学号", key: "selection_audit_operator_id" },
        { title: "教学班编号", key: "selection_audit_curriculum_id" },
        { title: "课程编号", key: "curriculum_course_id" },
        { title: "课程名称", key: "course_name"},
        { title: "教学班老师", key: "curriculum_teacher_name" },
        { title: "操作", key: "selection_audit_type_string" },
        { title: "操作时间", key: "selection_audit_time" },
        { title: "操作人", key: "selection_audit_operator_id" },
    ]

    let selectionAudits = ref([] as selectionAuditInfo[])
    let nowSelectionPage = ref(1)
    let allSelectionPages = ref(1)

    function querySelectionAudit() {
        callapi.get("Audit", "querySelectionAudit", { page: nowSelectionPage.value }, (data) => {
            const result = <querySelectionAuditResponse>data
            allSelectionPages.value = Math.ceil(result.count / 50)
            selectionAudits.value = result.audits
        })
    }

    onMounted(() => {
        querySelectionAudit()
    })

    watch(nowSelectionPage, () => {
        querySelectionAudit()
    })
</script>

<style scoped></style>
