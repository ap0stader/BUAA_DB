<template>
    <v-container class="my-3">
        <v-card prepend-icon="mdi-account-circle" title="个人信息" max-width="600px" location="bottom">
            <v-divider />
            <v-row no-gutters class="mt-5">
                <v-col>
                    <v-list>
                        <v-list-item v-if="!token.isSuperAdmin" prepend-icon="mdi-card-account-details">
                            <v-list-item-title>
                                {{ token.isStudent ? "学号" : "工号" }}
                                <span class="mx-1"></span>
                                {{ token.id }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="!token.isSuperAdmin" prepend-icon="mdi-account">
                            <v-list-item-title>
                                姓名
                                <span class="mx-1"></span>
                                {{ token.getName }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="!token.isSuperAdmin" prepend-icon="mdi-bank">
                            <v-list-item-title>
                                院系
                                <span class="mx-1"></span>
                                {{ env.getDepartmentInfo(token.getDepartmentId)?.department_name }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="token.isStudent" prepend-icon="mdi-school">
                            <v-list-item-title>
                                专业
                                <span class="mx-1"></span>
                                {{ env.getMajorInfo(token.studentInfo.student_major_id)?.major_name }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="token.isStudent" prepend-icon="mdi-manjaro">
                            <v-list-item-title>
                                班级
                                <span class="mx-1"></span>
                                {{ token.studentInfo.student_class_id }}
                            </v-list-item-title>
                        </v-list-item>
                        <v-list-item v-if="token.isSuperAdmin" prepend-icon=" mdi-key">
                            <v-list-item-title>
                                身份
                                <span class="mx-1"></span>
                                学校管理员
                            </v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-col>
            </v-row>
            <v-card-actions>
                <v-btn variant="text" color="red" ref="changePasswordButton">修改密码</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>

    <ChangePassword :activator="changePasswordButton" />
</template>

<script lang="ts" setup name="UserCenter">
    import ChangePassword from "@/components/UserrCenter/ChangePassword.vue"
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import { ref } from "vue"

    const token = useToken()
    const env = useEnv()

    let changePasswordButton = ref()
</script>

<style scoped></style>
