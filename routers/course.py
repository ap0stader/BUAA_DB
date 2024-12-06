from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse
from pydantic import BaseModel
import redis
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from utils.db import get_cursor
from utils.rds import rds
from io import BytesIO
import conf
import pandas as pd
from utils.errno import *
from utils.utils import *
from pathlib import Path
import os, uuid
import openpyxl
import tempfile
import random, string
from typing import List
from utils.resource import ResourceManager

router = APIRouter(
    prefix="/Course",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class add_course_req(BaseModel):
    course_teacher_id: str
    course_name: str
    course_type: int
    course_credit: float
    course_hours: int
    course_plan_filename: str

@router.post("/addCourse")
async def add_course(req: add_course_req):
    course_teacher_id, course_name, course_type, course_credit, course_hours, course_plan_filename = req.course_teacher_id, req.course_name, req.course_type, req.course_credit, req.course_hours, req.course_plan_filename
    if not check_teacher_id_exist(course_teacher_id):
        return {
            'success': False,
            'errCode': 300101,
            'data': {}
        }
    if course_type < 0 or course_type > 4:
        return {
            'success': False,
            'errCode': 300102,
            'data': {}
        }
    course_id = "T" + str(int(datetime.now().timestamp()))[2:] + ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=2))
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO course_table \
        (course_id, course_name, course_type, course_credit, course_hours, course_teacher_id, course_plan_filename, course_status) \
            VALUES \
        (%s, %s, %s, %s, %s, %s, %s, %s)",
        (course_id, course_name, course_type, course_credit, course_hours, course_teacher_id, course_plan_filename, 0)
    )
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'course_id': course_id
        }
    }

@router.post("/uploadCoursePlan")
async def upload_course_plan(file: UploadFile = File(...)):
    try:
        file_type = file.filename.split(".")[-1]
        content = await file.read()
        uuid_str = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{uuid_str}.{file_type}"
        with open(file_path, "wb") as f:
            f.write(content)
        return {
            'success': True,
            'errCode': OK,
            'data': {
                'filename': f"{uuid_str}.{file_type}"
            }
        }
    except Exception as e:
        return {
            'success': False,
            'errCode': 300201,
            'data': {}
        }

@router.get("/queryCourses")
async def query_courses():
    conn, cursor = get_cursor('root')
    cursor.execute(
"""SELECT
    ct.course_id,
    ct.course_name,
    ct.course_type,
    ct.course_credit,
    ct.course_hours,
    ct.course_teacher_id,
    tt.teacher_name AS course_teacher_name,
    ct.course_plan_filename,
    ct.course_status
FROM
    course_table as ct
LEFT JOIN
    teacher_table as tt
ON
    ct.course_teacher_id = tt.teacher_id
ORDER BY
    ct.course_id;
""")
    result = cursor.fetchall()
    courses = []
    for row in result:
        courses.append({
            'course_id': row['course_id'],
            'course_name': row['course_name'],
            'course_type': row['course_type'],
            'course_credit': row['course_credit'],
            'course_hours': row['course_hours'],
            'course_teacher_id': row['course_teacher_id'],
            'course_teacher_name': row['course_teacher_name'],
            'course_plan_filename': row['course_plan_filename'],
            'course_status': row['course_status']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'courses': courses
        }
    }

class accept_course_req(BaseModel):
    temp_course_id: str
    accept_course_id: str

@router.post("/acceptCourse")
async def accept_course(req: accept_course_req):
    temp_course_id, accept_course_id = req.temp_course_id, req.accept_course_id
    if not check_course_id_exist(temp_course_id):
        return {
            'success': False,
            'errCode': 300401,
            'data': {}
        }
    if check_course_id_exist(accept_course_id):
        return {
            'success': False,
            'errCode': 300402,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE course_table SET course_id=%s, course_status=1 WHERE course_id=%s", (accept_course_id, temp_course_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class diasble_course_req(BaseModel):
    course_id: str

@router.post("/disableCourse")
async def disable_course(req: diasble_course_req):
    course_id = req.course_id
    if not check_course_id_exist(course_id):
        return {
            'success': False,
            'errCode': 300501,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE course_table SET course_status=2 WHERE course_id=%s", (course_id,))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class add_curriculum_req(BaseModel):
    curriculum_teacher_id: str
    curriculum_course_id: str
    curriculum_semester_id: int
    curriculum_capacity: int
    curriculum_info: str | None

@router.post("/addCurriculum")
async def add_curriculum(req: add_curriculum_req):
    curriculum_teacher_id, curriculum_course_id, curriculum_semester_id, curriculum_capacity, curriculum_info = req.curriculum_teacher_id, req.curriculum_course_id, req.curriculum_semester_id, req.curriculum_capacity, req.curriculum_info
    if not check_teacher_id_exist(curriculum_teacher_id):
        return {
            'success': False,
            'errCode': 300601,
            'data': {}
        }
    if not check_course_id_exist(curriculum_course_id):
        return {
            'success': False,
            'errCode': 300602,
            'data': {}
        }
    if not check_semester_id_exist(curriculum_semester_id):
        return {
            'success': False,
            'errCode': 300603,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    if curriculum_info:
        cursor.execute("INSERT INTO curriculum_table \
            (curriculum_course_id, curriculum_teacher_id, curriculum_semester_id, curriculum_capacity, curriculum_info) \
                VALUES \
            (%s, %s, %s, %s, %s)",
            (curriculum_course_id, curriculum_teacher_id, curriculum_semester_id, curriculum_capacity, curriculum_info)
        )
    else:
        cursor.execute("INSERT INTO curriculum_table \
            (curriculum_course_id, curriculum_teacher_id, curriculum_semester_id, curriculum_capacity) \
                VALUES \
            (%s, %s, %s, %s)",
            (curriculum_course_id, curriculum_teacher_id, curriculum_semester_id, curriculum_capacity)
        )
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.get("/querySemesterCurriculums")
async def query_semester_curriculums(semester_id: int):
    if not check_semester_id_exist(semester_id):
        return {
            'success': False,
            'errCode': 300701,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute(
"""SELECT 
    ct.curriculum_id,
    ct.curriculum_course_id,
    c.course_name,
    c.course_type,
    c.course_credit,
    c.course_hours,
    ct.curriculum_teacher_id,
    t.teacher_name,
    ct.curriculum_capacity,
    ct.curriculum_info,
    cust.curriculum_utilization_string
FROM 
    curriculum_table ct
LEFT JOIN 
    course_table c ON ct.curriculum_course_id = c.course_id
LEFT JOIN 
    teacher_table t ON ct.curriculum_teacher_id = t.teacher_id
LEFT JOIN 
    curriculum_utilization_string_table cust ON ct.curriculum_id = cust.curriculum_id
WHERE 
    ct.curriculum_semester_id=%s
ORDER BY
    ct.curriculum_id;
""", (semester_id,))
    result = cursor.fetchall()
    curriculums = []
    for row in result:
        curriculums.append({
            'curriculum_id': row['curriculum_id'],
            'curriculum_course_id': row['curriculum_course_id'],
            'course_name': row['course_name'],
            'course_type': row['course_type'],
            'course_credit': row['course_credit'],
            'course_hours': row['course_hours'],
            'curriculum_teacher_id': row['curriculum_teacher_id'],
            'teacher_name': row['teacher_name'],
            'curriculum_capacity': row['curriculum_capacity'],
            'curriculum_info': row['curriculum_info'],
            'curriculum_utilization_string': row['curriculum_utilization_string']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'curriculums': curriculums
        }
    }

class set_curriculum_resource_req(BaseModel):
    curriculum_id: int
    acquire_resources: List[int]

@router.post("/setCurriculumResource")
async def set_curriculum_resource(req: set_curriculum_resource_req):
    curriculum_id, acquire_resources = req.curriculum_id, req.acquire_resources
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 300801,
            'data': {}
        }
    curriculum = get_curriculum(curriculum_id)
    acq = ResourceManager(acquire_resources)
    used_list = []
    used_str = get_curriculums_resource(curriculum['curriculum_semester_id'], curriculum_id)
    for i in used_str:
        used_list += ResourceManager(i).list
    acq_list = acq.list
    # print('used_list:', used_list)
    # print('acq_list:', acq_list)
    merge = list(set(used_list + acq_list))
    if len(merge) != len(used_list) + len(acq_list):
        return {
            'success': False,
            'errCode': 300802,
            'data': {}
        }
    # print(acq.str)
    conn, cursor = get_cursor('root')
    cursor.execute("DELETE FROM curriculum_utilization_string_table WHERE curriculum_id=%s", (curriculum_id,))
    cursor.execute("INSERT INTO curriculum_utilization_string_table (curriculum_id, curriculum_utilization_string) VALUES (%s, %s)", (curriculum_id, acq.str))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'curriculum_utilization_string': acq.str
        }
    }

class release_curriculum_resource_req(BaseModel):
    curriculum_id: int

@router.post("/releaseCurriculumResource")
async def release_curriculum_resource(req: release_curriculum_resource_req):
    curriculum_id = req.curriculum_id
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 300901,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("DELETE FROM curriculum_resource_table WHERE curriculum_id=%s", (curriculum_id,))
    cursor.execute("DELETE FROM curriculum_utilization_string_table WHERE curriculum_id=%s", (curriculum_id,))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class update_curriculum_capacity_req(BaseModel):
    curriculum_id: int
    curriculum_capacity: int

@router.post("/updateCurriculumCapacity")
async def update_curriculum_capacity(req: update_curriculum_capacity_req):
    curriculum_id, curriculum_capacity = req.curriculum_id, req.curriculum_capacity
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 301001,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE curriculum_table SET curriculum_capacity=%s WHERE curriculum_id=%s", (curriculum_capacity, curriculum_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

