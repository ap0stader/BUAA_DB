# API文档

**请求编码: UTF-8**

**请求响应格式（header中Content-Type）: 'application/json'**

**请求地址格式: "http://ecs.1230123.xyz:20080/api/v1/*{Module}/{Method}*"**

所有的请求，凡是经过了代码逻辑捕获处理的，HTTP状态码均为200。不通过HTTP状态码表示请求是否成功。

所有成功的请求，按如下格式返回，下文中所示JSON无特殊说明均省略"success"和"errCode"，只表示data成员的要求。

```javascript
{
  "success": true,
  "errCode": 0,
  "data": {
    // 填充对应的数据
    // 其中字符串形式"{DATA}_EMPTY"表示该字符串可为空串，但是必须存在该成员。其余的不能为空串
  }
}
```

所有错误的请求，按如下格式返回，下文中将以表格形式说明错误码对应的含义。

```javascript
{
  "success": false,
  "errCode": 99999, // 仅为示例，应替换为对应的错误码，类型为整型数字，不是字符串
  "data": {} // 仍要存在data成员，类型为空对象
}
```

| errCode（后端与前端交换的数据） | errDescription（前端展示解释） |
| ------------------------------- | ------------------------------ |
| 99999                           | 未知错误                       |

## 1. Auth

### 1. login

| Method | Content-Type        | 描述         |
| ------ | ------------------- | ------------ |
| POST   | multipart/form-data | 用户请求登录 |

表单内容**（注：Value类型并非Content Type，下同）**

| Key      | Value类型 | 描述         |
| -------- | --------- | ------------ |
| username | String    | 用户名       |
| password | String    | 密码**密文** |

成功返回

```javascript
{
  "data": {
    "token": "{token}", // 返回已在Redis中保存的token
    "type": 0 | 1 | 2 | 3 // 用户角色，0为学生、1为教师、2为学院教务，3为学校管理员
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 100101  | 账号或密码错误 |

### 2. verify

| Method | Content-Type        | 描述                    |
| ------ | ------------------- | ----------------------- |
| POST   | multipart/form-data | 客户端验证Token是否有效 |

表单内容**（注：Value类型并非Content Type，下同）**

| Key   | Value类型 | 描述      |
| ----- | --------- | --------- |
| Token | String    | 鉴权Token |

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 100201  | Token已经失效  |

### 
