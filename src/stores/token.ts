import { defineStore } from "pinia"

export const useToken = defineStore("token", {
    state: () => {
        return {
            token: "",
            type: -1,
            name: "",
        }
    },
    actions: {
        setToken(token: string, type: number) {
            this.token = token
            this.type = type
        },
        setName(name: string) {
            this.name = name
        },
        clear() {
            this.token = ""
            this.type = -1
        },
    },
    getters: {
        isInit(): boolean {
            return this.type == -1
        },
        isStudent(): boolean {
            return this.type == 0
        },
        isTeacher(): boolean {
            return this.type == 1
        },
        isFaculty(): boolean {
            return this.type == 2
        },
        isAdmin(): boolean {
            return this.type == 3
        },
    },
    persist: true,
})
