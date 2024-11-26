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
| 100102  | 该账户已被停用   |

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

### 11. queryStudent

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

### 14. updateStudent

| Method | 描述         |
| ------ | ------------ |
| POST   | 更新学生信息 |

请求内容

```javascript
{
  "student_id": "{student_id}", // 修改的学生的学号
  "student_name": "{student_name}", // 修改后的学生的姓名
  "student_gender": "{student_gender}" | null, // 修改后的学生的性别
  "student_phone": "{student_phone}" | null, // 修改后的学生的手机号
  "student_class_id": student_class_id, // 修改后的学生所属的班级号
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
| 201401  | 无此班级号对应的班级 |

### 15. queryTeacher

| Method | 描述                 |
| ------ | -------------------- |
| GET    | 获取所有的教师的信息 |

请求参数

| Key  | Value类型 | 描述                 |
| ---- | --------- | -------------------- |
| page | Integer   | 结果展示第 {page} 页 |

**注：一次只返回最多50个教师信息。即查询的结果分页表示，按照工号字典序进行排列，页大小为50**

**注：前端必须提供page，默认page参数为1**

成功返回

```javascript
{
  "data": {
    "count": count, // 教师信息的总条数
    "teachers": [
      {
        "teacher_id": "{teacher_id}", // 教师的工号
        "teacher_name": "{teacher_name}", // 教师的姓名
        "teacher_gender": "{teacher_gender}" | null, // 教师的性别
        "teacher_phone": "{teacher_phone}" | null, // 教师的手机号
        "teacher_department_id": teacher_department_id, // 教师所属的院系号
        "login_is_enable": login_is_enable // 该教师是否能够登录 
      },
      // ......
    ]
  }
}
```

错误代码：无

### 16. addTeacher

| Method | 描述     |
| ------ | -------- |
| POST   | 新增教师 |

请求内容

```javascript
{
  "teacher_id": "{teacher_id}", // 新增的教师的学号
  "teacher_name": "{teacher_name}", // 新增的教师的姓名
  "teacher_gender": "{teacher_gender}" | null, // 新增的教师的性别
  "teacher_phone": "{teacher_phone}" | null, // 新增的教师的手机号
  "teacher_department_id": teacher_department_id, // 新增的教师所属的院系号
}
```

**注：添加教师同时添加登录权限，密码为默认密码`123456`，对应的密文为**

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
| 201601  | 有同学工号的人员     |
| 201602  | 无此院系号对应的院系 |

### 17. updateTeacher

| Method | 描述         |
| ------ | ------------ |
| POST   | 更新教师信息 |

请求内容

```javascript
{
  "teacher_id": "{teacher_id}", // 修改的教师的学号
  "teacher_name": "{teacher_name}", // 修改后的教师的姓名
  "teacher_gender": "{teacher_gender}" | null, // 修改后的教师的性别
  "teacher_phone": "{teacher_phone}" | null, // 修改后的教师的手机号
  "teacher_department_id": teacher_department_id, // 修改后的教师所属的院系号
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
| 201701  | 无此院系号对应的院系 |

### 18. queryFaculty

| Method | 描述                     |
| ------ | ------------------------ |
| GET    | 获取所有的学院教务的信息 |

请求参数

| Key  | Value类型 | 描述                 |
| ---- | --------- | -------------------- |
| page | Integer   | 结果展示第 {page} 页 |

**注：一次只返回最多50个学院教务信息。即查询的结果分页表示，按照工号字典序进行排列，页大小为50**

**注：前端必须提供page，默认page参数为1**

成功返回

```javascript
{
  "data": {
    "count": count, // 学院教务信息的总条数
    "faculties": [
      {
        "faculty_id": "{faculty_id}", // 学院教务的学号
        "faculty_name": "{faculty_name}", // 学院教务的姓名
        "faculty_gender": "{faculty_gender}" | null, // 学院教务的性别
        "faculty_phone": "{faculty_phone}" | null, // 学院教务的手机号
        "faculty_department_id": faculty_department_id, // 学院教务所属的院系号
        "login_is_enable": login_is_enable // 该学院教务是否能够登录 
      },
      // ......
    ]
  }
}
```

错误代码：无

### 19. addFaculty

| Method | 描述         |
| ------ | ------------ |
| POST   | 新增学院教务 |

请求内容

```javascript
{
  "faculty_id": "{faculty_id}", // 新增的学院教务的学号
  "faculty_name": "{faculty_name}", // 新增的学院教务的姓名
  "faculty_gender": "{faculty_gender}" | null, // 新增的学院教务的性别
  "faculty_phone": "{faculty_phone}" | null, // 新增的学院教务的手机号
  "faculty_department_id": faculty_department_id, // 新增的学院教务所属的院系号
}
```

**注：添加学院教务同时添加登录权限，密码为默认密码`123456`，对应的密文为**

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
| 201901  | 有同学工号的人员     |
| 201902  | 无此院系号对应的院系 |

### 20. updateFaculty

| Method | 描述             |
| ------ | ---------------- |
| POST   | 更新学院教务信息 |

请求内容

```javascript
{
  "faculty_id": "{faculty_id}", // 修改的学院教务的学号
  "faculty_name": "{faculty_name}", // 修改后的学院教务的姓名
  "faculty_gender": "{faculty_gender}" | null, // 修改后的学院教务的性别
  "faculty_phone": "{faculty_phone}" | null, // 修改后的学院教务的手机号
  "faculty_department_id": faculty_department_id, // 修改后的学院教务所属的院系号
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
| 202001  | 无此院系号对应的院系 |

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
        "course_id": course_id,
        "course_name": course_name,
        "course_type": course_type,
        "course_credit": course_credit,
        "course_hours": course_hours,
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "capacity_in": capacity_in,
        "capacity_out":capacity_out,
        "info": info,
        "time_and_place_string": time_and_place_string
      },
      // ......
    ]
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300101  | 学期号不存在   |

### 2. addChoice

| Method | 描述       |
| ------ | ---------- |
| POST   | 新增预选课 |

请求内容

```javascript
{
  "student_id": student_id,
  "curriculum_id": curriculum_id,
  "order": order, // 志愿顺序
  "introduction": introduction | null
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
| 300202  | 教学班号不存在         |
| 300203  | 志愿顺序不合法         |
| 300204  | 自我介绍长度不合法     |
| 300205  | 课程已选，无法重新选中 |

### 3. deleteChoice

| Method | 描述       |
| ------ | ---------- |
| POST   | 删除预选课 |

请求内容

```javascript
{
  "student_id": student_id,
  "curriculum_id": curriculum_id
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
| 300301  | 学号不存在               |
| 300302  | 教学班号不存在           |
| 300303  | 未选择该课程班，无法退课 |
| 300304  | 无法退课                 |

### 4. addAttendance

| Method | 描述           |
| ------ | -------------- |
| POST   | 退改时间段选课 |

请求内容

```javascript
{
  "student_id": student_id,
  "curriculum_id": curriculum_id
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
| 300401  | 学号不存在                     |
| 300402  | 教学班号不存在                 |
| 300403  | 已选该教学班，不能重复选择     |
| 300404  | 该教学班和已选教学班时间有重合 |
| 300405  | 已选同一课程的另一教学班       |
| 300406  | 该教学班已选满                 |

### 5. deleteAttendance

| Method | 描述           |
| ------ | -------------- |
| POST   | 退改时间段退课 |

请求内容

```javascript
{
  "student_id": student_id,
  "curriculum_id": curriculum_id
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
| 300501  | 学号不存在               |
| 300502  | 教学班号不存在           |
| 300503  | 未选择该课程班，无法退课 |
| 300504  | 无法退课                 |

### 6. querySelectionAudit

| Method | 描述             |
| ------ | ---------------- |
| GET    | 查看选课操作记录 |

请求内容

```javascript
{
  "student_id": student_id
}
```

成功返回

```javascript
{
  "data": {
    "audits": [
      {
        "audit_id": audit_id,
        "curriculum_id": curriculum_id,
        "course_id": course_id,
        "course_name": course_name,
        "course_type": course_type,
        "course_credit": course_credit,
        "course_hours": course_hours,
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "capacity_in": capacity_in,
        "capacity_out":capacity_out,
        "info": info,
        "time_and_place_string": time_and_place_string,
        "order": order, // 志愿顺序
        "introduction": introduction | null, // 科研课堂自我介绍
        "audit_type": audit_type,
        "audit_time": audit_time
      },
      // ......
    ]
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300601  | 学号不存在     |

### 7. queryChoice

| Method | 描述                         |
| ------ | ---------------------------- |
| GET    | 查看某个学期所有预选的教学班 |

请求内容

```javascript
{
  "student_id": student_id,
  "semester_id": semester_id
}
```

成功返回

```javascript
{
  "data": {
    "curriculums": [
      {
        "curriculum_id": curriculum_id,
        "course_id": course_id,
        "course_name": course_name,
        "course_type": course_type,
        "course_credit": course_credit,
        "course_hours": course_hours,
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "capacity_in": capacity_in,
        "capacity_out":capacity_out,
        "info": info,
        "time_and_place_string": time_and_place_string,
        "order": order, // 志愿顺序
        "introduction": introduction | null // 科研课堂自我介绍
      },
      // ......
    ]
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300701  | 学号不存在     |
| 300702  | 学期号不存在   |

### 8. queryAttendance

| Method | 描述                         |
| ------ | ---------------------------- |
| GET    | 查看某个学期所有选择的教学班 |

请求内容

```javascript
{
  "student_id": student_id,
  "semester_id": semester_id
}
```

成功返回

```javascript
{
  "data": {
    "curriculums": [
      {
        "curriculum_id": curriculum_id,
        "course_id": course_id,
        "course_name": course_name,
        "course_type": course_type,
        "course_credit": course_credit,
        "course_hours": course_hours,
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "capacity_in": capacity_in,
        "capacity_out":capacity_out,
        "info": info,
        "time_and_place_string": time_and_place_string
      },
      // ......
    ]
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300801  | 学号不存在     |
| 300802  | 学期号不存在   |

### 9.queryScore

| Method | 描述                         |
| ------ | ---------------------------- |
| GET    | 查看某个学期所有选择的教学班 |

请求内容

```javascript
{
  "student_id": student_id,
}
```

成功返回

```javascript
{
  "data": {
    "curriculums": [
      {
        "curriculum_id": curriculum_id,
        "course_id": course_id,
        "course_name": course_name,
        "course_type": course_type,
        "course_credit": course_credit,
        "course_hours": course_hours,
        "teacher_id": teacher_id,
        "teacher_name": teacher_name,
        "info": info,
        "score": score // 课程成绩
      },
      // ......
    ], 
    "gpa": gpa, 
    "average": average,
    "weighted_average": weighted_average
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 300901  | 学号不存在     |

### 10. addAttendanceEvaluation

| Method | 描述           |
| ------ | -------------- |
| POST   | 给选课增加评教 |

请求内容

```javascript
{
  "attendance_id": attendance_id,
  "evaluation": evaluation
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
| 301001  | 选课号不存在   |
| 301002  | 评教分数不合法 |
| 301003  | 重复评教       |

### 11. queryStudentInfo

| Method | 描述         |
| ------ | ------------ |
| GET    | 获取学生信息 |

请求内容

```javascript
{
  "student_id": student_id
}
```

成功返回

```javascript
{
  "data": {
    "name": name,
    "gender": gender,
    "phone": phone,
    "class_id": class_id,
    "major_id": major_id,
    "major_name": major_name,
    "department_id": department_id,
    "department_name": department_name,
    "headteacher_id": headteacher_id,
    "headteacher_name": headteacher_name
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 301101  | 学号不存在     |

### 12. updateStudentInfo

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
| 301101  | 学号不存在     |
| 301102  | 手机号码不合法 |

## 4. Teacher

### addCource

| Method | 描述     |
| ------ | -------- |
| POST   | 增开课程 |

请求内容

```javascript
{
  "teacher_id": teacher_id, // 请求修改信息的学号
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
| 301101  | 工号不存在     |
| 301102  | 手机号码不合法 |

### queryCource



### updateCource



### addCurriculum



### queryChoice



### addAttendance



### queryAttendance



### addScore



### queryCurriculumScore



### queryClassScore



### 11. queryTeacherInfo

| Method | 描述         |
| ------ | ------------ |
| GET    | 获取教师信息 |

请求内容

```javascript
{
  "teacher_id": teacher_id
}
```

成功返回

```javascript
{
  "data": {
    "name": name,
    "gender": gender,
    "phone": phone,
    "department_id": department_id,
    "department_name": department_name,
    "headteacher_of_class_id": headteacher_of_class_id
  }
}
```

错误代码

| errCode | errDescription |
| ------- | -------------- |
| 301101  | 工号不存在     |

### 12. updateTeacherInfo

| Method | 描述         |
| ------ | ------------ |
| POST   | 修改教师信息 |

请求内容

```javascript
{
  "teacher_id": teacher_id, // 请求修改信息的学号
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
| 301101  | 工号不存在     |
| 301102  | 手机号码不合法 |
