<template>
    <v-dialog :activator="activator" max-width="500px" v-model="isDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="isDialogActive = false" />
                <v-toolbar-title>修改密码</v-toolbar-title>
            </v-toolbar>
            <v-text-field
                v-model="oldPassword"
                :rules="[(v) => !!v || '请输入旧密码']"
                label="旧密码"
                variant="outlined"
                class="ma-2 mb-1"
                prepend-inner-icon="mdi-lock"
                :type="passwordVisible ? 'text' : 'password'"
                :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="passwordVisible = !passwordVisible" />
            <v-text-field
                v-model="newPassword"
                :rules="[(v) => !!v || '请输入新密码']"
                label="新密码"
                variant="outlined"
                class="mx-2 mb-1"
                prepend-inner-icon="mdi-lock-outline"
                :type="passwordVisible ? 'text' : 'password'"
                :append-inner-icon="passwordVisible ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append-inner="passwordVisible = !passwordVisible" />
            <template v-slot:actions>
                <v-btn @click="isDialogActive = false">取消</v-btn>
                <v-btn
                    color="primary"
                    :disabled="oldPassword == '' || newPassword == ''"
                    :loading="submitLoading"
                    @click="onChangePasswordClick"
                    >修改密码</v-btn
                >
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="ChangePassword">
    import { useToken } from "@/stores/token"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import CryptoJS from "crypto-js"
    import { ref } from "vue"
    import { useRouter } from "vue-router"

    defineProps(["activator"])

    const router = useRouter()
    const token = useToken()

    let isDialogActive = ref(false)

    let oldPassword = ref("")
    let newPassword = ref("")
    let passwordVisible = ref(false)
    let submitLoading = ref(false)

    function onChangePasswordClick() {
        submitLoading.value = true
        callapi.post(
            "json",
            "Auth",
            "updatePassword",
            {
                username: token.id,
                old_password: CryptoJS.SHA512(oldPassword.value).toString(),
                new_password: CryptoJS.SHA512(newPassword.value).toString(),
            },
            (data) => {
                oldPassword.value = ""
                newPassword.value = ""
                submitLoading.value = false
                emitter.emit("success_snackbar", "修改密码成功，请重新登录")
                isDialogActive.value = false
                token.$reset()
                router.replace("/")
            },
            (errCode) => {
                submitLoading.value = false
            }
        )
    }
</script>
