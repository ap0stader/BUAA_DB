<template>
    <div class="login-background">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1903 556">
            <path
                class="svg-banner-shape"
                d="M753.1,434.2c110.6,63.7,277.7,70.6,373.4,15.4L1905,0v555.9H0V0.2L753.1,434.2z" />
        </svg>
    </div>
    <v-main>
        <v-container fluid class="fill-height">
            <v-row justify="center" class="w-100">
                <v-col>
                    <v-img src="/logo.png" max-height="80px" />
                    <v-card class="elevation-5 px-2 py-4" max-width="480px" location="center">
                        <v-card-title class="text-center card-title"> 选课系统 </v-card-title>
                        <RouterView />
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<script lang="ts" setup name="AuthView">
    import { useToken } from "@/stores/token"
    import { callapi } from "@/utils/callapi"
    import { onMounted } from "vue"
    import { useRouter, RouterView } from "vue-router"
    const router = useRouter()
    const token = useToken()

    onMounted(() => {
        if (token.isInit) {
            // 没有登录信息则导航到登录界面
            router.replace({ name: "login" })
        } else {
            // 有登录信息则检验登录信息是否有效
            callapi.get(
                "Auth",
                "verify",
                {
                    token: token.token,
                },
                (data) => {
                    router.replace("/home")
                },
                (errCode) => {
                    token.$reset()
                    router.replace({ name: "login" })
                }
            )
        }
    })
</script>

<style scoped>
    .login-background {
        position: absolute;
        width: 100%;
        height: 100%;
        min-height: 200px;
        max-height: 600px;
        background: linear-gradient(90deg, #021048, #1e38a3);
    }

    .login-background svg {
        position: absolute;
        bottom: -1px;
        fill: white;
    }

    .card-title {
        font-size: 28px;
        color: #142149;
    }
</style>
