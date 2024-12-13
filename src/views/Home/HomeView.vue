<template>
    <v-navigation-drawer expand-on-hover rail permanent>
        <v-list>
            <v-list-item prepend-avatar="/favicon.png" title="选课系统" />
        </v-list>

        <v-divider />

        <v-list density="compact" v-model:selected="selected" mandatory nav>
            <v-list-item
                v-if="token.isSuperAdmin"
                prepend-icon="mdi-home-city"
                title="场地管理"
                value="placeManagement" />
            <v-list-item
                v-if="token.isSuperAdmin"
                prepend-icon="mdi-bank"
                title="学院管理"
                value="departmentManagement" />
            <v-list-item v-if="token.isSuperAdmin" prepend-icon="mdi-school" title="专业管理" value="majorManagement" />
            <v-list-item
                v-if="token.isSuperAdmin || token.isFaculty"
                prepend-icon="mdi-manjaro"
                title="班级管理"
                value="classManagement" />
            <v-list-item
                v-if="token.isSuperAdmin || token.isFaculty"
                prepend-icon="mdi-account-group"
                title="学生管理"
                value="studentManagement" />
            <v-list-item
                v-if="token.isSuperAdmin || token.isFaculty"
                prepend-icon="mdi-account-tie"
                title="教师管理"
                value="teacherManagement" />
            <v-list-item
                v-if="token.isSuperAdmin"
                prepend-icon="mdi-account-cog"
                title="学院教务管理"
                value="facultyManagement" />
            <v-list-item
                v-if="token.isSuperAdmin"
                prepend-icon="mdi-calendar"
                title="学期管理"
                value="semesterManagement" />
            <v-list-item v-if="token.isTeacher" prepend-icon="mdi-book-open" title="申报课程" value="teacherCourse" />
            <v-list-item
                v-if="token.isSuperAdmin"
                prepend-icon="mdi-book-open"
                title="课程管理"
                value="courseManagement" />
            <v-list-item
                v-if="token.isTeacher"
                prepend-icon="mdi-human-male-board-poll"
                title="查看教学班"
                value="teacherCurriculum" />
            <v-list-item
                v-if="token.isTeacher && env.env.now_step === 0"
                prepend-icon="mdi-domain-plus"
                title="开设教学班"
                value="addCurriculum" />
            <v-list-item
                v-if="token.isSuperAdmin || token.isFaculty"
                prepend-icon="mdi-domain"
                title="教学班管理"
                value="curriculumManagement" />
            <v-list-item
                v-if="token.isFaculty"
                prepend-icon="mdi-medal"
                title="成绩查看"
                value="facultyScore" />
            <v-list-item
                v-if="token.isStudent && [0, 1, 3, 4].includes(env.env.now_step)"
                prepend-icon="mdi-human-male-board-poll"
                title="选课"
                value="chooseCurriculum" />
            <!-- Insert Befor Here -->
            <v-list-item v-if="token.isSuperAdmin" prepend-icon="mdi-cogs" title="系统设置" value="envManagement" />
            <v-list-item v-if="token.isSuperAdmin" prepend-icon="mdi-list-box" title="审计信息" value="auditCenter" />
            <v-list-item prepend-icon="mdi-account-circle" title="个人中心" value="userCenter" />
        </v-list>
    </v-navigation-drawer>

    <v-app-bar density="compact" elevation="1" location="top">
        <!-- 返回按钮 -->
        <template #prepend>
            <!-- 添加需要返回键 -->
            <v-btn
                v-if="typeof route.name == 'string' && navigateBackPageName.includes(route.name)"
                variant="text"
                icon
                density="comfortable"
                class="ml-2"
                @click="navigateBack">
                <v-icon size="default"> mdi-arrow-left </v-icon>
            </v-btn>
        </template>
        <v-app-bar-title>{{ titleDict[<string>route.name] }}</v-app-bar-title>
        <v-spacer />
        <p>当前选课阶段：{{ env.getStepString }}</p>
        <span class="mx-3"></span>
        <p>当前学期：{{ env.getSemesterInfo(env.env.now_semester_id)?.semester_name }}</p>
        <span class="mx-3"></span>
        <p>欢迎，{{ token.getName }}</p>
        <v-btn icon @click="onLogoutClick">
            <v-icon>mdi-logout-variant</v-icon>
        </v-btn>
    </v-app-bar>

    <v-main>
        <RouterView />
    </v-main>
</template>

<script lang="ts" setup name="HomeView">
    import { useEnv } from "@/stores/env"
    import { useToken } from "@/stores/token"
    import { ref, watch } from "vue"
    import { RouterView, useRoute, useRouter } from "vue-router"

    const route = useRoute()
    const router = useRouter()
    const env = useEnv()
    const token = useToken()

    const titleDict: {
        [key: string]: string
    } = {
        userCenter: "个人中心",
        placeManagement: "场地管理",
        departmentManagement: "学院管理",
        majorManagement: "专业管理",
        classManagement: "班级管理",
        studentManagement: "学生管理",
        teacherManagement: "教师管理",
        facultyManagement: "学院教务管理",
        semesterManagement: "学期管理",
        teacherCourse: "申报课程",
        courseManagement: "课程管理",
        teacherCurriculum: "查看教学班",
        addCurriculum: "开设教学班",
        curriculumManagement: "教学班管理",
        curriculumAttendance: "选课情况",
        curriculumChoice: "预选情况",
        curriculumScore: "选课与成绩情况",
        facultyScore: "成绩查看",
        chooseCurriculum: "选课",
        // Insert Befor Here
        envManagement: "系统设置",
        auditCenter: "审计信息",
    }

    let selected = ref(<string[]>[route.name])

    watch(selected, (newValue) => {
        router.push({ name: newValue[0] })
    })

    const navigateBackPageName: string[] = ["curriculumAttendance", "curriculumChoice", "curriculumScore"]

    function navigateBack() {
        router.back()
    }

    function onLogoutClick() {
        token.$reset()
        router.replace("/")
    }
</script>

<style scoped></style>
