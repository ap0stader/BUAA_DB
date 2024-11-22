from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import redis
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from utils.db import get_cursor
from utils.rds import rds
import conf
from utils.errno import *
from io import BytesIO
import pandas as pd

router = APIRouter(
    prefix="/Admin",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


###############################################################
#####################    Place    #############################
###############################################################

def check_place_id_exist(place_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table WHERE place_id=%s", (place_id,))
    return cursor.fetchone() is not None

def check_place_name_exist(place_name: str, ex_place_id: int = -1):
    conn, cursor = get_cursor('root')
    if ex_place_id == -1:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s", (place_name,))
    else:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s AND place_id!=%s", (place_name, ex_place_id))
    return cursor.fetchone() is not None

@router.get("/queryPlace")
async def query_place():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table")
    result = cursor.fetchall()
    places = []
    for row in result:
        places.append({
            'place_id': row['place_id'],
            'place_name': row['place_name'],
            'is_enable': row['place_is_enable']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'places': places
        }
    }

class add_place_req(BaseModel):
    place_name: str

@router.post("/addPlace")
async def add_place(req: add_place_req):
    place_name = req.place_name
    if check_place_name_exist(place_name):
        return {
            'success': False,
            'errCode': ERR_PLACE__DUPLICATE_PLACE_NAME_1,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO place_table (place_name) VALUES (%s)", (place_name,))
    conn.commit()
    place_id = cursor.lastrowid
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'place_id': place_id
        }
    }

class update_place_req(BaseModel):
    place_id: int
    place_name: str
    is_enable: int
 
@router.post("/updatePlace")
async def update_place(req: update_place_req):
    place_id, place_name, is_enable = req.place_id, req.place_name, req.is_enable
    if not check_place_id_exist(place_id):
        return {
            'success': False,
            'errCode': ERR_PLACE__PLACE_ID_NOT_FOUND,
            'data': {}
        }
    if check_place_name_exist(place_name, place_id):
        return {
            'success': False,
            'errCode': ERR_PLACE__DUPLICATE_PLACE_NAME_2,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE place_table SET place_name=%s, place_is_enable=%s WHERE place_id=%s",
                        (place_name, is_enable, place_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Department    ########################
###############################################################

def check_department_id_exist(department_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table WHERE department_id=%s", (department_id,))
    return cursor.fetchone() is not None

def check_department_name_exist(department_name: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table WHERE department_name=%s", (department_name,))
    return cursor.fetchone() is not None

@router.get("/queryDepartment")
async def query_department():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table")
    result = cursor.fetchall()
    departments = []
    for row in result:
        departments.append({
            'department_id': row['department_id'],
            'department_name': row['department_name']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'departments': departments
        }
    }

class add_department_req(BaseModel):
    department_id: int
    department_name: str

@router.post("/addDepartment")
async def add_department(department_req: add_department_req):
    department_id, department_name = department_req.department_id, department_req.department_name
    if check_department_id_exist(department_id) or check_department_name_exist(department_name):
        return {
            'success': False,
            'errCode': ERR_DEPART__DUPLICATE_DEPARTMENT_ID_NAME,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO department_table (department_id, department_name) VALUES (%s, %s)", (department_id, department_name))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Majar    ##############################
###############################################################

def check_major_id_exist(major_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table WHERE major_id=%s", (major_id,))
    return cursor.fetchone() is not None

def check_major_name_exist(major_name: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table WHERE major_name=%s", (major_name,))
    return cursor.fetchone() is not None

def check_major_department_id_exist(department_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table WHERE department_id=%s", (department_id,))
    return cursor.fetchone() is not None

@router.get("/queryMajor")
async def query_major():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table")
    result = cursor.fetchall()
    majors = []
    for row in result:
        majors.append({
            'major_id': row['major_id'],
            'major_name': row['major_name'],
            'major_department_id': row['major_department_id']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'majors': majors
        }
    }

class add_major_req(BaseModel):
    major_id: int
    major_name: str
    major_department_id: int

@router.post("/addMajor")
async def add_major(major_req: add_major_req):
    major_id, major_name, major_department_id = major_req.major_id, major_req.major_name, major_req.major_department_id
    if check_major_id_exist(major_id) or check_major_name_exist(major_name):
        return {
            'success': False,
            'errCode': ERR_MAJOR__DUPLICATE_MAJOR_ID_NAME,
            'data': {}
        }
    if not check_major_department_id_exist(major_department_id):
        return {
            'success': False,
            'errCode': ERR_MAJOR__DEPARTMENT_ID_NOT_FOUND,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO major_table (major_id, major_name, major_department_id) VALUES (%s, %s, %s)",
                        (major_id, major_name, major_department_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Class    #############################
###############################################################

def check_class_id_exist(class_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM class_table WHERE class_id=%s", (class_id,))
    return cursor.fetchone() is not None

def check_teacher_id_exist(teacher_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM teacher_table WHERE teacher_id=%s", (teacher_id,))
    return cursor.fetchone() is not None

def check_teacher_is_master(teacher_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM class_table WHERE class_teacher_id=%s", (teacher_id,))
    return cursor.fetchone() is not None

@router.get("/queryClass")
async def query_class():
    conn, cursor = get_cursor('root')
    cursor.execute(
"""SELECT
    ct.class_id,
    ct.class_major_id,
    mt.major_department_id AS class_department_id,
    ct.class_teacher_id,
    tt.teacher_name AS class_teacher_name
FROM 
    class_table ct
LEFT JOIN 
    major_table mt
ON 
    ct.class_major_id = mt.major_id
LEFT JOIN 
    teacher_table tt
ON 
    ct.class_teacher_id = tt.teacher_id;
""")
    result = cursor.fetchall()
    classes = []
    for row in result:
        classes.append({
            'class_id': row['class_id'],
            'class_major_id': row['class_major_id'],
            'class_department_id': row['class_department_id'],
            'class_teacher_id': row['class_teacher_id'],
            'class_teacher_name': row['class_teacher_name'],
        })
    # replace None in classes with null
    print(classes)
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'classes': classes
        }
    }

class add_class_req(BaseModel):
    class_id: int
    class_major_id: int

@router.post("/addClass")
async def add_class(class_req: add_class_req):
    class_id, class_major_id = class_req.class_id, class_req.class_major_id
    if check_class_id_exist(class_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__DUPLICATE_CLASS_ID,
            'data': {}
        }
    if not check_major_id_exist(class_major_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__MAJOR_ID_NOT_FOUND,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO class_table (class_id, class_major_id) VALUES (%s, %s)", (class_id, class_major_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class update_class_teacher_req(BaseModel):
    class_id: int
    class_teacher_id: int

@router.post("/updateClassTeacher")
async def update_class_teacher(req: update_class_teacher_req):
    class_id, class_teacher_id = req.class_id, req.class_teacher_id
    if not check_class_id_exist(class_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__CLASS_ID_NOT_FOUND,
            'data': {}
        }
    if not check_teacher_id_exist(class_teacher_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__TEACHER_ID_NOT_FOUND,
            'data': {}
        }
    if check_teacher_is_master(class_teacher_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__TEACHER_IS_CLASS_MASTER,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE class_table SET class_teacher_id=%s WHERE class_id=%s", (class_teacher_id, class_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Student    ###########################
###############################################################

def check_login_id_exist(id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM login_table WHERE login_id=%s", (id,))
    return cursor.fetchone() is not None

def check_student_class_id_exist(class_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM class_table WHERE class_id=%s", (class_id,))
    return cursor.fetchone() is not None

@router.get("/queryStudent")
async def query_student(page: int):
    conn, cursor = get_cursor('root')
    offset = (page - 1) * 50
    cursor.execute(
"""SELECT 
    st.student_id AS "student_id", 
    st.student_name AS "student_name", 
    st.student_gender AS "student_gender", 
    st.student_phone AS "student_phone", 
    st.student_class_id AS "student_class_id", 
    cl.class_major_id AS "student_major_id", 
    ma.major_department_id AS "student_department_id", 
    lt.login_is_enable AS "login_is_enable"
FROM 
    student_table st
JOIN 
    class_table cl ON st.student_class_id = cl.class_id
JOIN 
    major_table ma ON cl.class_major_id = ma.major_id
JOIN 
    login_table lt ON st.student_id = lt.login_id
ORDER BY
    st.student_id
LIMIT 50 OFFSET %s;
""", (offset,))
    result = cursor.fetchall()
    students = []
    for row in result:
        students.append({
            'student_id': row['student_id'],
            'student_name': row['student_name'],
            'student_gender': row['student_gender'],
            'student_phone': row['student_phone'],
            'student_class_id': row['student_class_id'],
            'student_major_id': row['student_major_id'],
            'student_department_id': row['student_department_id'],
            'login_is_enable': row['login_is_enable']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'students': students
        }
    }

class add_student_req(BaseModel):
    student_id: int
    student_name: str
    student_gender: str | None
    student_phone: str | None
    student_class_id: int

@router.post("/addStudent")
async def add_student(student_req: add_student_req):
    student_id, student_name, student_gender, student_phone, student_class_id = student_req.student_id, student_req.student_name, student_req.student_gender, student_req.student_phone, student_req.student_class_id
    if check_login_id_exist(student_id):
        return {
            'success': False,
            'errCode': ERR_STUDENT__DUPLICATE_LOGIN_ID,
            'data': {}
        }
    if not check_student_class_id_exist(student_class_id):
        return {
            'success': False,
            'errCode': ERR_STUDENT__CLASS_ID_NOT_FOUND,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (student_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 1, 1))
    cursor.execute("INSERT INTO student_table (student_id, student_name, student_gender, student_phone, student_class_id) VALUES (%s, %s, %s, %s, %s)", (student_id, student_name, student_gender, student_phone, student_class_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.post("/addStudentBatch")
async def add_student_batch(file: UploadFile = File(...)):
    DUPLICATE_LOGIN_ID = 1
    CLASSID_NOT_FOUND = 2
    UNKNOWN = 3
    try:
        if not file.filename.endswith('.xlsx'):
            raise Exception
        content = await file.read()
        df = pd.read_excel(BytesIO(content), skiprows=1, header=None)
        if len(df.columns) != 5:
            raise Exception
        failed_info = []
        for index, row in df.iterrows():
            student_id, student_name, student_gender, student_phone, student_class_id = row
            if pd.isnull(student_id) or pd.isnull(student_name) or pd.isnull(student_class_id):
                raise Exception
        conn, cursor = get_cursor('root')
        for index, row in df.iterrows():
            student_id, student_name, student_gender, student_phone, student_class_id = row
            if pd.isnull(student_gender):
                student_gender = None
            if pd.isnull(student_phone):
                student_phone = None
            if check_login_id_exist(student_id):
                failed_info.append({
                    'student_id': student_id,
                    'errCode': DUPLICATE_LOGIN_ID
                })
                continue
            if not check_class_id_exist(student_class_id):
                failed_info.append({
                    'student_id': student_id,
                    'errCode': CLASSID_NOT_FOUND
                })
                continue
            try:
                cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (student_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 1, 1))
                cursor.execute("INSERT INTO student_table (student_id, student_name, student_gender, student_phone, student_class_id) VALUES (%s, %s, %s, %s, %s)", (student_id, student_name, student_gender, student_phone, student_class_id))
            except Exception as e:
                failed_info.append({
                    'student_id': student_id,
                    'errCode': UNKNOWN
                })
                continue
        if len(failed_info) > 0:
            conn.rollback()
        else:
            conn.commit()
        return {
            'success': True,
            'errCode': OK,
            'data': {
                'failed_info': failed_info
            }
        }
    except Exception as e:
        return {
            'success': False,
            'errCode': ERR_STUDENT__UNKNOWN_ERROR,
            'data': {}
        }