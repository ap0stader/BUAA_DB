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
from utils.utils import *
from io import BytesIO
import pandas as pd

router = APIRouter(
    prefix="/Admin",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


###############################################################
#####################    Place    #############################
###############################################################

@router.get("/queryPlace")
async def query_place():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table")
    places = cursor.fetchall()
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
    place_is_enable: int
 
@router.post("/updatePlace")
async def update_place(req: update_place_req):
    place_id, place_name, place_is_enable = req.place_id, req.place_name, req.place_is_enable
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
                        (place_name, place_is_enable, place_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Department    ########################
###############################################################

@router.get("/queryDepartment")
async def query_department():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM department_table")
    departments = cursor.fetchall()
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
async def add_department(req: add_department_req):
    department_id, department_name = req.department_id, req.department_name
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

@router.get("/queryMajor")
async def query_major():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM major_table")
    majors = cursor.fetchall()
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
async def add_major(req: add_major_req):
    major_id, major_name, major_department_id = req.major_id, req.major_name, req.major_department_id
    if check_major_id_exist(major_id) or check_major_name_exist(major_name):
        return {
            'success': False,
            'errCode': ERR_MAJOR__DUPLICATE_MAJOR_ID_NAME,
            'data': {}
        }
    if not check_department_id_exist(major_department_id):
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

@router.get("/queryClass")
async def query_class():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM queryClass")
    classes = cursor.fetchall()
    # replace None in classes with null
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
async def add_class(req: add_class_req):
    class_id, class_major_id = req.class_id, req.class_major_id
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

class update_class_headmaster_req(BaseModel):
    class_id: int
    class_headmaster_id: str | None

@router.post("/updateClassHeadmaster")
async def update_class_headmaster(req: update_class_headmaster_req):
    class_id, class_headmaster_id = req.class_id, req.class_headmaster_id
    if not check_class_id_exist(class_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__CLASS_ID_NOT_FOUND,
            'data': {}
        }
    if class_headmaster_id is not None and not check_teacher_id_exist(class_headmaster_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__TEACHER_ID_NOT_FOUND,
            'data': {}
        }
    if check_teacher_is_master(class_headmaster_id):
        return {
            'success': False,
            'errCode': ERR_CLASS__TEACHER_IS_CLASS_MASTER,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE class_table SET class_headmaster_id=%s WHERE class_id=%s", (class_headmaster_id, class_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Student    ###########################
###############################################################

@router.get("/queryStudent")
async def query_student(page: int, department_id: int):
    conn, cursor = get_cursor('root')
    if department_id < 0:
        cursor.execute("SELECT * FROM queryStudent")
    else:
        cursor.execute("SELECT * FROM queryStudent WHERE student_department_id = %s", (department_id,))
    count = len(cursor.fetchall())
    offset = (page - 1) * 50
    if department_id < 0:
        cursor.execute("SELECT * FROM queryStudent ORDER BY student_id LIMIT 50 OFFSET %s;", (offset,))
    else:
        cursor.execute("SELECT * FROM queryStudent WHERE student_department_id = %s ORDER BY student_id LIMIT 50 OFFSET %s;", (department_id, offset))
    students = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'count': count,
            'students': students
        }
    }

class add_student_req(BaseModel):
    student_id: str
    student_name: str
    student_gender: str | None
    student_phone: str | None
    student_class_id: int

@router.post("/addStudent")
async def add_student(req: add_student_req):
    student_id, student_name, student_gender, student_phone, student_class_id = req.student_id, req.student_name, req.student_gender, req.student_phone, req.student_class_id
    if check_login_id_exist(student_id):
        return {
            'success': False,
            'errCode': ERR_STUDENT__DUPLICATE_LOGIN_ID,
            'data': {}
        }
    if not check_class_id_exist(student_class_id):
        return {
            'success': False,
            'errCode': ERR_STUDENT__CLASS_ID_NOT_FOUND,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (student_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 0, 1))
        cursor.execute("INSERT INTO student_table (student_id, student_name, student_gender, student_phone, student_class_id) VALUES (%s, %s, %s, %s, %s)", (student_id, student_name, student_gender, student_phone, student_class_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
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
        df = pd.read_excel(BytesIO(content), header=None)
        if len(df.columns) != 5:
            raise Exception
        failed_info = []
        for index, row in df.iterrows():
            if index == 0:
                continue
            student_id, student_name, student_gender, student_phone, student_class_id = row
            if pd.isnull(student_id) or pd.isnull(student_name) or pd.isnull(student_class_id):
                raise Exception
        conn, cursor = get_cursor('root')
        for index, row in df.iterrows():
            if index == 0:
                continue
            student_id, student_name, student_gender, student_phone, student_class_id = row
            if pd.isnull(student_gender):
                student_gender = None
            if pd.isnull(student_phone):
                student_phone = None
            if check_login_id_exist(student_id):
                failed_info.append({
                    'student_id': student_id,
                    'reason': DUPLICATE_LOGIN_ID
                })
                continue
            if not check_class_id_exist(student_class_id):
                failed_info.append({
                    'student_id': student_id,
                    'reason': CLASSID_NOT_FOUND
                })
                continue
            try:
                cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (student_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 0, 1))
                cursor.execute("INSERT INTO student_table (student_id, student_name, student_gender, student_phone, student_class_id) VALUES (%s, %s, %s, %s, %s)", (student_id, student_name, student_gender, student_phone, student_class_id))
            except Exception as e:
                failed_info.append({
                    'student_id': student_id,
                    'reason': UNKNOWN
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

class update_student_req(BaseModel):
    student_id: str
    student_name: str
    student_gender: str | None
    student_phone: str | None
    student_class_id: int

@router.post("/updateStudent")
async def update_student(req: update_student_req):
    student_id, student_name, student_gender, student_phone, student_class_id = req.student_id, req.student_name, req.student_gender, req.student_phone, req.student_class_id
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 201401,
            'data': {}
        }
    if not check_class_id_exist(student_class_id):
        return {
            'success': False,
            'errCode': 201402,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("UPDATE student_table SET student_name=%s, student_gender=%s, student_phone=%s, student_class_id=%s WHERE student_id=%s",
                        (student_name, student_gender, student_phone, student_class_id, student_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Teacher    ###########################
###############################################################

@router.get("/queryTeacher")
async def query_teacher(page: int, department_id: int):
    conn, cursor = get_cursor('root')
    if department_id < 0:
        cursor.execute("SELECT * FROM teacher_table")
    else:
        cursor.execute("SELECT * FROM teacher_table WHERE teacher_department_id = %s", (department_id,))
    count = len(cursor.fetchall())
    offset = (page - 1) * 50
    if department_id < 0:
        cursor.execute("SELECT * FROM queryTeacher ORDER BY teacher_id LIMIT 50 OFFSET %s;", (offset,))
    else:
        cursor.execute("SELECT * FROM queryTeacher WHERE teacher_department_id = %s ORDER BY teacher_id LIMIT 50 OFFSET %s;", (department_id, offset))
    teachers = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'count': count,
            'teachers': teachers
        }
    }

class add_teacher_req(BaseModel):
    teacher_id: str
    teacher_name: str
    teacher_gender: str | None
    teacher_phone: str | None
    teacher_department_id: int

@router.post("/addTeacher")
async def add_teacher(req: add_teacher_req):
    teacher_id, teacher_name, teacher_gender, teacher_phone, teacher_department_id = req.teacher_id, req.teacher_name, req.teacher_gender, req.teacher_phone, req.teacher_department_id
    if check_login_id_exist(teacher_id):
        return {
            'success': False,
            'errCode': 201601,
            'data': {}
        }
    if not check_department_id_exist(teacher_department_id):
        return {
            'success': False,
            'errCode': 201602,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (teacher_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 1, 1))
        cursor.execute("INSERT INTO teacher_table (teacher_id, teacher_name, teacher_gender, teacher_phone, teacher_department_id) VALUES (%s, %s, %s, %s, %s)", (teacher_id, teacher_name, teacher_gender, teacher_phone, teacher_department_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class update_teacher_req(BaseModel):
    teacher_id: str
    teacher_name: str
    teacher_gender: str | None
    teacher_phone: str | None
    teacher_department_id: int

@router.post("/updateTeacher")
async def update_teacher(req: update_teacher_req):
    teacher_id, teacher_name, teacher_gender, teacher_phone, teacher_department_id = req.teacher_id, req.teacher_name, req.teacher_gender, req.teacher_phone, req.teacher_department_id
    if not check_teacher_id_exist(teacher_id):
        return {
            'success': False,
            'errCode': 201701,
            'data': {}
        }
    if not check_department_id_exist(teacher_department_id):
        return {
            'success': False,
            'errCode': 201702,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("UPDATE teacher_table SET teacher_name=%s, teacher_gender=%s, teacher_phone=%s, teacher_department_id=%s WHERE teacher_id=%s", (teacher_name, teacher_gender, teacher_phone, teacher_department_id, teacher_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Faculty    ###########################
###############################################################

@router.get("/queryFaculty")
async def query_faculty(page: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM faculty_table")
    count = len(cursor.fetchall())
    offset = (page - 1) * 50
    cursor.execute("SELECT * FROM queryFaculty ORDER BY faculty_id LIMIT 50 OFFSET %s;", (offset,))
    faculties = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'count': count,
            'faculties': faculties
        }
    }

class add_faculty_req(BaseModel):
    faculty_id: str
    faculty_name: str
    faculty_gender: str | None
    faculty_phone: str | None
    faculty_department_id: int

@router.post("/addFaculty")
async def add_faculty(req: add_faculty_req):
    faculty_id, faculty_name, faculty_gender, faculty_phone, faculty_department_id = req.faculty_id, req.faculty_name, req.faculty_gender, req.faculty_phone, req.faculty_department_id
    if check_login_id_exist(faculty_id):
        return {
            'success': False,
            'errCode': 201901,
            'data': {}
        }
    if not check_department_id_exist(faculty_department_id):
        return {
            'success': False,
            'errCode': 201902,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("INSERT INTO login_table (login_id, login_password, login_role, login_is_enable) VALUES (%s, %s, %s, %s)", (faculty_id, "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413", 2, 1))
        cursor.execute("INSERT INTO faculty_table (faculty_id, faculty_name, faculty_gender, faculty_phone, faculty_department_id) VALUES (%s, %s, %s, %s, %s)", (faculty_id, faculty_name, faculty_gender, faculty_phone, faculty_department_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class update_faculty_req(BaseModel):
    faculty_id: str
    faculty_name: str
    faculty_gender: str | None
    faculty_phone: str | None
    faculty_department_id: int

@router.post("/updateFaculty")
async def update_faculty(req: update_faculty_req):
    faculty_id, faculty_name, faculty_gender, faculty_phone, faculty_department_id = req.faculty_id, req.faculty_name, req.faculty_gender, req.faculty_phone, req.faculty_department_id
    if not check_faculty_id_exist(faculty_id):
        return {
            'success': False,
            'errCode': 202001,
            'data': {}
        }
    if not check_department_id_exist(faculty_department_id):
        return {
            'success': False,
            'errCode': 202002,
            'data': {}
        }
    try:
        conn, cursor = get_cursor('root')
        cursor.execute("UPDATE faculty_table SET faculty_name=%s, faculty_gender=%s, faculty_phone=%s, faculty_department_id=%s WHERE faculty_id=%s", (faculty_name, faculty_gender, faculty_phone, faculty_department_id, faculty_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {
            'success': False,
            'errCode': ERR_UNKNOWN,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Login    #############################
###############################################################

class toggle_login_enable_req(BaseModel):
    username: str

@router.post("/toggleLoginEnable")
async def toggle_login_enable(req: toggle_login_enable_req):
    username = req.username
    if not check_login_id_exist(username):
        return {
            'success': False,
            'errCode': 202101,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT login_is_enable FROM login_table WHERE login_id=%s", (username))
    status = cursor.fetchone()['login_is_enable']
    cursor.execute("UPDATE login_table SET login_is_enable=%s WHERE login_id=%s", (0 if status else 1, username))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Environment    #######################
###############################################################

@router.get("/getEnv")
async def get_env():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM env_table et;")
    result = cursor.fetchone()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            **result
        }
    }

class set_env_step_req(BaseModel):
    step: int

@router.post("/setEnvStep")
async def set_env_step(req: set_env_step_req):
    step = req.step
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE env_table SET now_step=%s", (step,))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class set_env_semester_req(BaseModel):
    semester_id: int

@router.post("/setEnvSemester")
async def set_env_semester(req: set_env_semester_req):
    semester_id = req.semester_id
    if not check_semester_id_exist(semester_id):
        return {
            'success': False,
            'errCode': 202401,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE env_table SET now_semester_id=%s", (semester_id,))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

###############################################################
#####################    Semester    ##########################
###############################################################

@router.get("/querySemester")
async def query_semester():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM semester_table")
    result = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'semesters': result
        }
    }

class add_semester_req(BaseModel):
    semester_name: str

@router.post("/addSemester")
async def add_semester(req: add_semester_req):
    semester_name = req.semester_name
    if check_semester_name_exist(semester_name):
        return {
            'success': False,
            'errCode': 202601,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO semester_table (semester_name) VALUES (%s)", (semester_name,))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }
