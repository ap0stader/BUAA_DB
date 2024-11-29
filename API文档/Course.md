# API文档-3.Course

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

## 1. addCourse

| Method | 描述     |
| ------ | -------- |
| POST   | 申报课程 |

请求内容

```javascript
{
  "course_teacher_id": "{teacher_id}", // 申报课程的老师
  "course_name": "{course_name}", // 申报课程的名称
  "course_type": 0 | 1 | 2 | 3 | 4, // 申报课程的分类，依次对应必修课、选修课、通识课、体育课、科研课
  "course_credit": course_credit, // 申报课程的学分
  "course_hours": course_hours, // 申报课程的学时
  "course_plan_filename": "{course_plan_filename}" // 申报课程的课程方案
}
```

成功返回

```javascript
{
  "data": {
    "course_id": "{course_id}" // 申报课程的课程编号。刚申报的课程是未经过审核的课程，编号统一为"T+10位十进制时间戳"
  }
}
```

错误代码

| errCode | errDescription       |
| ------- | -------------------- |
| 400101  | 无此工号对应的教师   |
| 400102  | 提供的课程信息不合法 |

## 2. uploadCoursePlan

| Method | 描述                 |
| ------ | -------------------- |
| POST   | 上传保存课程教学大纲 |

请求内容

**请求格式为`multipart/form-data`**

| Key  | Value类型 | 描述             |
| ---- | --------- | ---------------- |
| file | FIle      | 课程教学大纲文件 |

成功返回

```javascript
{
  "data": {
  	"filename": "{filename}" // 上传后进行保存的文件名，应保持文件扩展名并将文件名改为随机生成的UUID
  }
}
```

**上传成功之后，应能用`https://ecs.1230123.xyz:20080/static/upload/{filename}`访问。**

错误代码

| errCode | errDescription             |
| ------- | -------------------------- |
| 300201  | 处理上传的文件遇到未知错误 |

## 3. queryCources

| Method | 描述                                       |
| ------ | ------------------------------------------ |
| GET    | 获得所有课程（含未审核的、不再开设的课程） |

请求参数：无

成功返回

```javascript
{
  "data": {
    "courses": [
      {
        "course_id": course_id, // 课程编号
        "course_name": "{course_name}", // 课程名称
        "course_type": 0 | 1 | 2 | 3 | 4, // 课程分类，依次对应必修课、选修课、通识课、体育课、科研课
        "course_credit": course_credit, // 课程学分
        "course_hours": course_hours, // 课程学时
        "course_teacher_id": "{course_teacher_id}" | null, // 申报教师工号
        "course_taecher_name": "{course_teacher_name}" | null, // 申报教师姓名
        "course_plan_filename": "course_plan_filename", // 课程教学大纲
        "course_status": 0 | 1 | 2 // 课程状态，依次对应未审核、已审核、已不再开设
      },
      // ......
    ]
  }
}
```

错误代码：无
