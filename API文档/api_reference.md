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
