# 系统实现报告

[TOC]

## 实现环境

使用阿里云ECS，具体环境参数如下

| 系统版本   | Ubuntu 22.04                                                 |
| ---------- | ------------------------------------------------------------ |
| MySQl版本  | mysql  Ver 8.0.40-0ubuntu0.22.04.1 for Linux on x86_64 ((Ubuntu)) |
| conda版本  | pconda 24.9.2                                                |
| Python版本 | Python 3.10.15                                               |
| redis版本  | 6.0.16                                                       |

## 系统功能结构图



## 基本表的定义，主外码等完整性约束定义，索引的定义



## 系统的安全性设计，不同人员的外模式及相关权限  



## 存储过程、触发器和函数的代码说明  



## 实现过程中主要技术和主要模块的论述  

### 后端

后端在实现过程中主要使用了以下技术：

- 使用uvicorn搭建后端服务器，接收前端请求
- 使用fastapi搭建后端处理逻辑
- 使用pymysql连接数据库，执行修改查询等操作
- 使用conda进行python环境管理
- 使用redis优化登入信息查询速度
- 使用中间件技术进行跨域管理

#### 主要模块

##### 主模块

主模块是整个系统运行入口，其主要功能有

- 负责读入配置信息，并根据配置信息设置系统参数
- 设置中间件，使跨域访问正常运行
- 将各个模块导入系统，同时进行模块管理与控制
- 启动系统

##### 功能实现子模块

功能实现子模块根据需求创建并进行合理分类，每个分类实现对应分类的api需求

##### 数据库连接子模块

负责连接数据库，系统对数据库的访问均通过该模块提供的接口实现

##### redis连接子模块

负责连接redis，系统对redis的访问均通过该模块提供的接口实现

##### 错误码管理子模块

该模块存储所有错误码，对错误码进行集中统一管理，提高系统可维护性

##### 配置信息读取子模块

负责读取配置信息

## 若干展示系统功能的运行实例  



## 源程序简要说明  

本系统文件结构：

```
backend
├── conf.json # 系统配置文件
├── conf.py # 配置信息读取子模块
├── db.json # 数据库配置文件
├── __init__.py
├── main.py # 系统主模块
├── redis.json # redis配置文件
├── routers # 功能实现子模块
│   ├── admin.py # 实现管理员相关功能
│   ├── audit.py # 实现审计信息相关功能
│   ├── auth.py # 实现身份认证相关功能
│   ├── choise.py # 实现学生选课相关功能
│   ├── course.py # 实现课程信息支持相关功能
│   ├── faculty.py # 实现职工管理相关功能
│   ├── __init__.py
│   ├── student.py # 实现学生管理相关功能
│   └── teacher.py # 实现教师管理相关功能
└── utils
    ├── db.py # 数据库连接子模块
    ├── errno.py # 错误码管理子模块
    ├── __init__.py
    ├── rds.py # redis连接子模块
    ├── resource.py # 课程占用资源转换实现库
    └── utils.py # 通用函数库
```

本系统使用的所有python库：

```
Package              Version
-------------------- -----------
annotated-types      0.7.0
anyio                4.6.2.post1
async-timeout        5.0.1
certifi              2024.8.30
cffi                 1.17.1
click                8.1.7
cryptography         43.0.3
dnspython            2.7.0
email_validator      2.2.0
et_xmlfile           2.0.0
exceptiongroup       1.2.2
fastapi              0.115.5
fastapi-cli          0.0.5
h11                  0.14.0
httpcore             1.0.6
httptools            0.6.4
httpx                0.27.2
idna                 3.10
itsdangerous         2.2.0
Jinja2               3.1.4
markdown-it-py       3.0.0
MarkupSafe           3.0.2
mdurl                0.1.2
numpy                2.1.3
openpyxl             3.1.5
orjson               3.10.11
pandas               2.2.3
pip                  24.3.1
pycparser            2.22
pydantic             2.9.2
pydantic_core        2.23.4
pydantic-extra-types 2.10.0
pydantic-settings    2.6.1
Pygments             2.18.0
PyJWT                2.9.0
PyMySQL              1.1.1
python-dateutil      2.9.0.post0
python-dotenv        1.0.1
python-multipart     0.0.17
pytz                 2024.2
PyYAML               6.0.2
redis                5.2.0
rich                 13.9.4
setuptools           75.1.0
shellingham          1.5.4
six                  1.16.0
sniffio              1.3.1
starlette            0.41.2
typer                0.13.0
typing_extensions    4.12.2
tzdata               2024.2
ujson                5.10.0
uvicorn              0.32.0
uvloop               0.21.0
watchfiles           0.24.0
websockets           14.0
wheel                0.44.0
```

运行系统流程为：

```
conda create -n backend python=3.12.7
conda activate backend
pip install fastapi uvicorn PyJWT PyMySQL redis
python main.py
```

## 收获和体会

### 董和军

在本次数据库课程的小组大作业中，我主要负责了后端代码的编写工作。在编写后端代码的过程中，我不仅深入理解了关系型数据库的理论知识，还通过实际操作加深了对数据库各类技术的认识与掌握。

我对**数据库设计**有了更清晰的理解。在项目初期，我们根据需求分析进行了数据库的建模工作，采用了**实体-关系模型（ER模型）**对数据进行抽象，并通过工具转换为具体的数据库表结构。在设计过程中，我理解到数据冗余与规范化的重要性，学会了通过**第三范式（3NF）**优化数据表结构，以确保数据存储的高效性和一致性。

在后端开发过程中，我重点使用了**SQL语言**与数据库进行交互，实现了数据的增删改查功能。通过实际编写代码，我熟练掌握了**JOIN查询**、**嵌套查询**以及**事务管理**等核心技术。例如，在实现复杂业务逻辑时，通过多表连接和子查询解决了数据分散存储的问题，而事务管理则确保了数据操作的原子性、一致性、隔离性和持久性（ACID原则），使数据库状态始终保持良好。

在开发过程中，我还遇到了一些挑战，比如如何提高数据库查询的效率。在进行代码优化时，我通过建立**索引**的方式大幅提高了数据库的查询性能，具体地我通过为频繁查询的字段添加索引，有效减少了查询耗时。同时，我还接触到了数据库的**视图**和**存储过程**等高级功能，认识到它们在简化开发和保护数据安全方面的实际价值，特别是视图在简化后端代码与增加可维护性方面的作用。

通过本次项目实践，我深刻体会到关系型数据库作为后端数据支撑的重要性。理论与实践的结合不仅帮助我掌握了数据库的基础与核心技术，还锻炼了我分析问题和解决问题的能力。在今后的学习和开发中，我将进一步深入研究数据库的优化技术，提升自己的技术水平，为成为一名合格的后端开发工程师打下坚实基础。
