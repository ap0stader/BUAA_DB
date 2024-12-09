<template>
    <v-container fluid class="pa-6">
        <p class="text-h4 mt-6 mb-4">场地管理</p>
        <p class="text-subtitle-2 mb-4">查看、查看管理场地</p>

        <v-data-table :headers="headers" :items="env.places" disable-sort sticky items-per-page="50">
            <template v-slot:item.actions="{ item }">
                <v-btn
                    v-if="item.place_is_enable"
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="red"
                    class="me-1"
                    @click="openEnableDialog(item)">
                    <v-icon size="default"> mdi-close </v-icon>
                </v-btn>
                <v-btn
                    v-else
                    variant="tonal"
                    icon
                    density="comfortable"
                    color="green"
                    class="me-1"
                    @click="openEnableDialog(item)">
                    <v-icon size="default"> mdi-check </v-icon>
                </v-btn>
            </template>
        </v-data-table>
    </v-container>

    <v-fab
        color="primary"
        prepend-icon="mdi-plus"
        location="top end"
        size="x-large"
        position="sticky"
        text="添加场地"
        extended
        app
        @click="openAddDialog"
        class="mt-4" />

    <v-dialog max-width="500px" v-model="enableDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="enableDialogActive = false" />
                <v-toolbar-title>{{ enableDialogItem.place_is_enable ? "停用" : "启用" }}场地</v-toolbar-title>
            </v-toolbar>
            <v-card-item>
                确定要{{ enableDialogItem.place_is_enable ? "停用" : "启用" }}场地“{{ enableDialogItem.place_name }}”？
            </v-card-item>

            <template v-slot:actions>
                <v-btn @click="enableDialogActive = false">取消</v-btn>
                <v-btn
                    :color="enableDialogItem.place_is_enable ? 'red' : 'green'"
                    :loading="enableDialogSubmitLoading"
                    @click="onEnableDialogSubmitClick">
                    {{ enableDialogItem.place_is_enable ? "停用" : "启用" }}
                </v-btn>
            </template>
        </v-card>
    </v-dialog>

    <v-dialog max-width="500px" v-model="addDialogActive">
        <v-card>
            <v-toolbar>
                <v-btn icon="mdi-close" @click="addDialogActive = false" />
                <v-toolbar-title>添加场地</v-toolbar-title>
            </v-toolbar>

            <v-text-field
                v-model="addDialogPlaceName"
                :rules="[(v) => !!v || '请输入新场地名称']"
                label="新场地名称"
                variant="outlined"
                class="ma-2" />

            <template v-slot:actions>
                <v-btn @click="addDialogActive = false">取消</v-btn>
                <v-btn color="primary" :loading="addDialogSubmitLoading" @click="onAddDialogSubmitClick"> 添加 </v-btn>
            </template>
        </v-card>
    </v-dialog>
</template>

<script lang="ts" setup name="PlaceManagement">
    import { useEnv } from "@/stores/env"
    import type { placeInfo } from "@/types"
    import { callapi } from "@/utils/callapi"
    import emitter from "@/utils/emitter"
    import { envManager } from "@/utils/envManager"
    import { onMounted, ref, watch } from "vue"

    const headers = [
        { title: "ID", key: "place_id" },
        { title: "场地名称", key: "place_name" },
        { title: "操作", key: "actions", sortable: false },
    ]

    const env = useEnv()

    onMounted(() => {
        envManager.updatePlace()
    })

    let enableDialogActive = ref(false)
    let enableDialogItem = ref({} as placeInfo)

    function openEnableDialog(item: placeInfo) {
        enableDialogItem.value = item
        enableDialogActive.value = true
    }

    watch(enableDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updatePlace()
        }
    })

    let enableDialogSubmitLoading = ref(false)

    function onEnableDialogSubmitClick() {
        enableDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "updatePlace",
            {
                place_id: enableDialogItem.value.place_id,
                place_name: enableDialogItem.value.place_name,
                place_is_enable: enableDialogItem.value.place_is_enable ? 0 : 1,
            },
            (data) => {
                emitter.emit("success_snackbar", (enableDialogItem.value.place_is_enable ? "停用" : "启用") + "成功")
                enableDialogSubmitLoading.value = false
                enableDialogActive.value = false
            },
            (errCode) => {
                enableDialogSubmitLoading.value = false
            }
        )
    }

    let addDialogActive = ref(false)
    let addDialogPlaceName = ref("")

    function openAddDialog() {
        addDialogActive.value = true
        addDialogPlaceName.value = ""
    }

    watch(addDialogActive, (newValue, oldValue) => {
        if (oldValue && !newValue) {
            envManager.updatePlace()
        }
    })

    let addDialogSubmitLoading = ref(false)

    function onAddDialogSubmitClick() {
        addDialogSubmitLoading.value = true
        callapi.post(
            "json",
            "Admin",
            "addPlace",
            {
                place_name: addDialogPlaceName.value,
            },
            (data) => {
                emitter.emit("success_snackbar", "场地添加成功")
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
