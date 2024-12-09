import axios from "axios"
import emitter from "./emitter"

const baseURL = "https://ecs.1230123.xyz:20080/api/v1"

interface errDescription {
    [key: number]: string
}

const errDescription: errDescription = {
    99999: "未知错误",
    100101: "账号或密码错误",
    100201: "登录信息已经失效",
    100301: "无此学工号对应的人员",
    100302: "原密码不正确",
}

interface APIResponse {
    success: boolean
    errCode: number
    data: object
}

const callapi = {
    get: async function (
        module: string,
        method: string,
        params?: object | null,
        success?: (data: object) => any,
        error?: (errCode: number) => any
    ) {
        const url = "/" + module + "/" + method
        axios({
            method: "get",
            baseURL: baseURL,
            url: url,
            params: params,
            responseType: "json",
            responseEncoding: "utf8",
        })
            .then((response) => {
                const isAPIResponse = (data: any): data is APIResponse => {
                    return (
                        typeof data.success == "boolean" &&
                        typeof data.errCode == "number" &&
                        typeof data.data == "object"
                    )
                }
                if (response.status == 200 && isAPIResponse(response.data)) {
                    const result = <APIResponse>response.data
                    if (result.success) {
                        if (success != undefined) {
                            success(result.data)
                        }
                    } else {
                        emitter.emit("apierror", errDescription[result.errCode])
                        if (error != undefined) {
                            error(result.errCode)
                        }
                    }
                } else {
                    emitter.emit("fatalerror", "网络错误：返回类型错误。请手动刷新页面")
                }
            })
            .catch((error) => {
                console.log(error)
                emitter.emit("fatalerror", "网络错误：" + error.code + "。请手动刷新页面")
            })
    },

    post: async function (
        module: string,
        method: string,
        body?: object | null,
        success?: (data: object) => any,
        error?: (errCode: number) => any
    ) {
        const url = "/" + module + "/" + method
        axios({
            method: "post",
            baseURL: baseURL,
            url: url,
            headers: {
                "Content-Type": "application/json",
            },
            data: body,
            responseType: "json",
            responseEncoding: "utf8",
        })
            .then((response) => {
                const isAPIResponse = (data: any): data is APIResponse => {
                    return (
                        typeof data.success == "boolean" &&
                        typeof data.errCode == "number" &&
                        typeof data.data == "object"
                    )
                }
                if (response.status == 200 && isAPIResponse(response.data)) {
                    const result = <APIResponse>response.data
                    if (result.success) {
                        if (success != undefined) {
                            success(result.data)
                        }
                    } else {
                        emitter.emit("apierror", errDescription[result.errCode])
                        if (error != undefined) {
                            error(result.errCode)
                        }
                    }
                } else {
                    emitter.emit("fatalerror", "网络错误：返回类型错误。请手动刷新页面")
                }
            })
            .catch((error) => {
                console.log(error)
                emitter.emit("fatalerror", "网络错误：" + error.code + "。请手动刷新页面")
            })
    },
}

export { callapi }
