<template>
    <v-navigation-drawer expand-on-hover rail permanent>
        <v-list>
            <v-list-item
                prepend-avatar="favicon.ico"
                title="选课系统" />
        </v-list>

        <v-divider />

        <v-list density="compact" v-model:selected="selected" mandatory nav>
            <v-list-item prepend-icon="mdi-account-circle" title="个人中心" value="userCenter" />
        </v-list>
    </v-navigation-drawer>

    <v-app-bar density="compact" elevation="1" location="top">
        <!-- 返回按钮 -->
        <!-- <template #prepend>
            <v-btn
                v-if="$route.name == 'groupDetail' || $route.name == 'tagDetail'"
                variant="text"
                icon
                density="comfortable"
                class="ml-2"
                @click="navigateBack">
                <v-icon size="default"> mdi-arrow-left </v-icon>
            </v-btn>
        </template> -->
        <v-app-bar-title>{{ title_dict[<string>$route.name] }}</v-app-bar-title>
        <v-spacer />
        <p>{{ token.name }}</p>
        <v-btn icon @click="onLogoutClick">
            <v-icon>mdi-logout-variant</v-icon>
        </v-btn>
    </v-app-bar>

    <v-main>
        <RouterView />
    </v-main>
</template>

<script lang="ts" setup name="HomeView">
    import { useToken } from "@/stores/token"
    import { ref, watch } from "vue"
    import { RouterView, useRoute, useRouter } from "vue-router"
    const route = useRoute()
    const router = useRouter()
    const token = useToken()

    const title_dict: {
        [key: string]: string
    } = {
        userCenter: "个人中心",
    }

    let selected = ref(<string[]>[route.name])

    watch(selected, (newValue) => {
        router.push({ name: newValue[0] })
    })

    function navigateBack() {
        router.back()
    }

    function onLogoutClick() {
        token.clear()
        router.replace("/")
    }
</script>

<style scoped></style>
