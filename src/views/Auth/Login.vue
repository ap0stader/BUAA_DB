<template>
    <v-card-subtitle class="text-center card-subtitle"> 欢迎登录选课系统 </v-card-subtitle>

    <v-card-text>
        <v-form :readonly="submitLoading" @submit.prevent="onLoginSubmit">
            <v-text-field
                label="请输入学工号"
                :rules="[(v) => !!v || '请输入学工号']"
                v-model="username"
                variant="outlined"
                color="#3073C4"
                prepend-inner-icon="mdi-account-outline"
                class="mb-3"
                type="text" />
            <v-text-field
                label="请输入密码"
                :rules="[(v) => !!v || '请输入密码']"
                v-model="password"
                variant="outlined"
                color="#3073C4"
                prepend-inner-icon="mdi-lock-outline"
                class="mb-3"
                :type="passwordVisible ? 'text' : 'password'"
                :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="passwordVisible = !passwordVisible" />
            <v-btn
                block
                variant="flat"
                color="#3073C4"
                size="x-large"
                class="mb-6"
                type="submit"
                :loading="submitLoading"
                >登录</v-btn
            >
        </v-form>
    </v-card-text>
</template>

<script lang="ts" setup name="Login">
    import { useToken } from "@/stores/token"
    import type { LoginResponse } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import CryptoJS from "crypto-js"
    import { ref } from "vue"
    import { useRouter } from "vue-router"
    const router = useRouter()
    const token = useToken()

    let username = ref("")
    let password = ref("")
    let passwordVisible = ref(false)
    let submitLoading = ref(false)

    function onLoginSubmit() {
        submitLoading.value = true
        let username_store = username.value
        if (username.value == "" || password.value == "") {
            submitLoading.value = false
        } else {
            callapi.post(
                "json",
                "Auth",
                "login",
                {
                    username: username.value,
                    password: CryptoJS.SHA512(password.value).toString(),
                },
                (data) => {
                    const result = <LoginResponse>data
                    token.setToken(result.token, result.type, username_store)
                    emitter.emit("success_snackbar", "登录成功")
                    router.replace("/home")
                },
                (errCode) => {
                    submitLoading.value = false
                }
            )
        }
    }
</script>

<style scoped>
    .card-subtitle {
        font-size: 20px;
        color: black;
    }
</style>
