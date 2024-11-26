# API文档

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

## 1. Auth

### 1. login

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

### 2. verify

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

### 3. updatePassword

| Method | 描述     |
| ------ | -------- |
| POST   | 修改密码 |

请求内容

```javascript
{
  "login_id": login_id, // 请求修改密码的学工号
  "login_password": "{login_password}", // 原密码
  "new_login_password": "{new_login_password}" // 新密码
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

## 2.Admin

### 1. queryPlace

| Method | 描述               |
| ------ | ------------------ |
| GET    | 返回所有的场地信息 |

请求参数：无

成功返回

```javascript
{
  "data": {
    "places": [
      {
        "place_id": place_id, // 场地编号
        "place_name": "{place_name}", // 场地名称
        "place_is_enable": place_is_enable // 场地是否被禁用
      },
      // ......
    ]
  }
}
```

错误代码：无

### 2. addPlace

| Method | 描述     |
| ------ | -------- |
| POST   | 新增场地 |

请求内容

```javascript
{
  "place_name": "{place_name}", // 新增的场地的场地名称
}
```

成功返回

```javascript
{
  "data": {
    "place_id": place_id // 新增的场地的场地编号
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 200201  | 有同名的场地   |

### 3. updatePlace

| Method | 描述         |
| ------ | ------------ |
| POST   | 更新场地信息 |

请求内容

```javascript
{
  "place_id": place_id, // 修改的场地的场地编号
  "place_name": "{place_name}", // 修改后的场地名称
  "place_is_enable": place_is_enable // 修改后的场地是否禁用
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription         |
| ------- | ---------------------- |
| 200301  | 有同名的场地           |
| 200302  | 无此场地编号对应的场地 |

### 4. queryDepartment

| Method | 描述               |
| ------ | ------------------ |
| GET    | 返回所有的院系信息 |

请求参数：无

成功返回

```javascript
{
  "data": {
    "departments": [
      {
        "department_id": department_id, // 院系编号
        "department_name": "{department_name}", // 院系名称
      },
      // ......
    ]
  }
}
```

错误代码：无

### 5. addDepartment

| Method | 描述     |
| ------ | -------- |
| POST   | 新增院系 |

请求内容

```javascript
{
  "department_id": department_id, // 新增的院系的院系号
  "department_name": "{department_name}", // 新增的院系的院系名称
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription           |
| ------- | ------------------------ |
| 200501  | 有同院系号或者同名的院系 |

### 6. queryMajor

| Method | 描述               |
| ------ | ------------------ |
| GET    | 返回所有的专业信息 |

请求参数：无

成功返回

```javascript
{
  "data": {
    "majors": [
      {
        "major_id": major_id, // 专业编号
        "major_name": "{major_name}", // 专业名称
        "major_department_id": major_department_id // 专业所属院系号
      },
      // ......
    ]
  }
}
```

错误代码：无

### 7. addMajor

| Method | 描述     |
| ------ | -------- |
| POST   | 新增专业 |

请求内容

```javascript
{
  "major_id": major_id, // 新增的专业的的专业号
  "major_name": "{major_name}", // 新增的专业的专业名称
  "major_department_id": major_department_id // 新增的专业所属院系号
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription           |
| ------- | ------------------------ |
| 200701  | 有同专业号或者同名的专业 |
| 200702  | 无此院系号对应的院系     |

### 8. queryClass

| Method | 描述               |
| ------ | ------------------ |
| GET    | 返回所有的班级信息 |

请求参数：无

成功返回

```javascript
{
  "data": {
    "classes": [
      {
        "class_id": class_id, // 班级编号
        "class_major_id": class_major_id, // 班级所属专业号
        "class_department_id": class_department_id, // 班级所属院系号
        "class_teacher_id": class_teacher_id | null, // 班级的班主任工号
        "class_teacher_name": "{class_teacher_name}" | null // 班级的班主任姓名
      },
      // ......
    ]
  }
}
```

错误代码：无

### 9. addClass

| Method | 描述     |
| ------ | -------- |
| POST   | 新增班级 |

请求内容

```javascript
{
  "class_id": class_id, // 新增的班级的的班级号
  "class_major_id": class_major_id // 新增的班级所属专业号
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
| 200901  | 有同班级号的班级     |
| 200902  | 无此专业号对应的专业 |

### 10. updateClassTeacher

| Method | 描述             |
| ------ | ---------------- |
| POST   | 修改班级的班主任 |

请求内容

```javascript
{
  "class_id": class_id, // 修改班主任的班级的的班级号
  "class_teacher_id": class_teacher_id | null // 修改后的班级的班主任的工号
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription                 |
| ------- | ------------------------------ |
| 201001  | 无此班级编号对应的班级         |
| 201002  | 无此工号对应的教师             |
| 201003  | 该教师已经担任其他班级的班主任 |

### 11.queryStudent

| Method | 描述                 |
| ------ | -------------------- |
| GET    | 获取所有的学生的信息 |

请求参数

| Key  | Value类型 | 描述                 |
| ---- | --------- | -------------------- |
| page | Integer   | 结果展示第 {page} 页 |

**注：一次只返回最多50个学生信息。即查询的结果分页表示，按照学号字典序进行排列，页大小为50**

**注：前端必须提供page，默认page参数为1**

成功返回

```javascript
{
  "data": {
    "count": count, // 学生信息的总条数
    "students": [
      {
        "student_id": "{student_id}", // 学生的学号
        "student_name": "{student_name}", // 学生的姓名
        "student_gender": "{student_gender}" | null, // 学生的性别
        "student_phone": "{student_phone}" | null, // 学生的手机号
        "student_class_id": student_class_id, // 学生所属的班级号
        "student_major_id": student_major_id, // 学生所属的专业号
        "student_department_id": student_department_id, // 学生所属的院系号
        "login_is_enable": login_is_enable // 该学生是否能够登录 
      },
      // ......
    ]
  }
}
```

错误代码：无

### 12. addStudent

| Method | 描述     |
| ------ | -------- |
| POST   | 新增学生 |

请求内容

```javascript
{
  "student_id": "{student_id}", // 新增的学生的学号
  "student_name": "{student_name}", // 新增的学生的姓名
  "student_gender": "{student_gender}" | null, // 新增的学生的性别
  "student_phone": "{student_phone}" | null, // 新增的学生的手机号
  "student_class_id": student_class_id, // 新增的学生所属的班级号
}
```

**注：添加学生同时添加登录权限，密码为默认密码`123456`，对应的密文为**

```
ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413
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
| 201201  | 有同学工号的人员     |
| 201202  | 无此班级号对应的班级 |

### 13. addStudentBatch

| Method | 描述         |
| ------ | ------------ |
| POST   | 批量新增学生 |

请求内容

**请求格式为`multipart/form-data`**

| Key  | Value类型 | 描述                       |
| ---- | --------- | -------------------------- |
| file | FIle      | 按照模板填写的学生批量信息 |

成功返回

```javascript
{
  "data": {
    "failed_info": [
      {
        "student_id": student_id, // 添加失败的学生的学号
        "reason": 1 | 2 | 3 // 失败的原因1:有同学工号的人员 2:无此班级号对应的班级 3:未知原因（数据库插入时出错）
      },
      // ......
    ]
  }
}
```

错误代码

| errCode | errDescription             |
| ------- | -------------------------- |
| 201301  | 解析上传的文件遇到未知错误 |

## 3. Student

### 1. queryCurriculum

| Method | 描述                     |
| ------ | ------------------------ |
| GET    | 获取给定学期的所有教学班 |

请求内容

```javascript
{
  "semester_id": semester_id, // 需要获取的学期
}
```

成功返回

```javascript
{
  "data": {
    "curriculums": [
      {
        "curriculum_id": curriculum_id,
        "curriculum_course_id": curriculum_course_id,
        "curriculum_teacher_id": place_is_enable,
        "curriculum_capacity_in": curriculum_capacity_in,
        "curriculum_capacity_out":curriculum_capacity_out,
        "curriculum_info": curriculum_info
      },
      // ......
    ]
  }
}
```

### 2. addChoice

| Method | 描述       |
| ------ | ---------- |
| POST   | 新增预选课 |

请求内容

```javascript
{
  "choice_student_id": student_id,
  "choice_curriculum_id": choice_curriculum_id,
  "choice_order": choice_order,
  "choice_introduction": choice_introduction | null
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription         |
| ------- | ---------------------- |
| 300201  | 学号不存在             |
| 300202  | 课程班号不存在         |
| 300203  | 志愿顺序不合法         |
| 300204  | 自我介绍长度不合法     |
| 300205  | 课程已选，无法重新选中 |
| 300206  | 无法选中               |

### 3. deleteChoice

| Method | 描述       |
| ------ | ---------- |
| POST   | 删除预选课 |

请求内容

```javascript
{
  "choice_student_id": student_id,
  "choice_curriculum_id": choice_curriculum_id,
  "choice_order": choice_order,
  "choice_introduction": choice_introduction | null
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300301  | 学号不存在     |
| 300302  | 课程班号不存在 |

### 4. queryAttendance

### 5.queryScore

### 6. addAttendanceEvaluation



### 7. updateStudentInfo

| Method | 描述         |
| ------ | ------------ |
| POST   | 修改学生信息 |

请求内容

```javascript
{
  "student_id": student_id, // 请求修改信息的学号
  "phone": "{phone}" // 手机号码
}
```

成功返回

```javascript
{
  "data": {} // 空对象
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300701  | 学工号不存在   |
| 300702  | 手机号码不合法 |

