# API文档-Auth

[TOC]

**请求编码: UTF-8**

**POST请求体格式（header中的Content-Type）: 'application/json'，特殊标注除外**

**请求响应体格式（header中的Content-Type）: 'application/json'**

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

## 1. ✅login

| Method | 描述         |
| ------ | ------------ |
| POST   | 用户请求登录 |

请求内容

```javascript
{
  "username": "{username}", // 请求登录的学工号
  "password": "{password}" // 请求登录的密码密文
}
```

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

| errCode | errDescription   |
| ------- | ---------------- |
| 100101  | 学工号或密码错误 |
| 100102  | 该账户已被停用   |

## 2. ✅verify

| Method | 描述                    |
| ------ | ----------------------- |
| GET    | 客户端验证Token是否有效 |

请求参数

| Key   | Value类型 | 描述                    |
| ----- | --------- | ----------------------- |
| Token | String    | 请求验证是否有效的Token |

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

## 3. ✅updatePassword

| Method | 描述     |
| ------ | -------- |
| POST   | 修改密码 |

请求内容

```javascript
{
  "username": "{username}", // 请求修改密码的学工号
  "old_password": "{old_password}", // 原密码密文
  "new_password": "{new_password}" // 新密码密文
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription       |
| ------- | -------------------- |
| 100301  | 无此学工号对应的人员 |
| 100302  | 原密码不正确         |