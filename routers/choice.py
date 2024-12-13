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
    prefix="/Choice",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


order_limit = [3, 3, 5, 5, 1]

class add_choice_req(BaseModel):
    student_id: str
    curriculum_id: int
    order: int
    introduction: str | None

@router.post("/addChoice")
async def add_choice(req: add_choice_req):
    student_id, curriculum_id, order, introduction = req.student_id, req.curriculum_id, req.order, req.introduction
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400101,
            'data': {}
        }
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 400102,
            'data': {}
        }
    if check_choice_curriculum_is_exist(student_id, curriculum_id):
        return {
            'success': False,
            'errCode': 400103,
            'data': {}
        }
    if check_choice_order_is_exist(student_id, curriculum_id, order):
        return {
            'success': False,
            'errCode': 400104,
            'data': {}
        }
    course_type = get_curriculum_course_type(curriculum_id)
    if order > order_limit[course_type]:
        return {
            'success': False,
            'errCode': 400105,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO choice_table (choice_student_id, choice_curriculum_id, choice_order, choice_introduction) VALUES (%s, %s, %s, %s)", (student_id, curriculum_id, order, introduction))
    conn.commit()
    add_selection_audit(student_id, curriculum_id, 0, student_id)
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class delete_choice_req(BaseModel):
    student_id: str
    curriculum_id: int

@router.post("/deleteChoice")
async def delete_choice(req: delete_choice_req):
    student_id, curriculum_id = req.student_id, req.curriculum_id
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400201,
            'data': {}
        }
    if not check_choice_curriculum_is_exist(student_id, curriculum_id):
        return {
            'success': False,
            'errCode': 400202,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("DELETE FROM choice_table WHERE choice_student_id=%s AND choice_curriculum_id=%s", (student_id, curriculum_id))
    conn.commit()
    add_selection_audit(student_id, curriculum_id, 1, student_id)
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.get("/queryStudentChoices")
async def query_student_choices(student_id: str):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400301,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM queryStudentChoices 
        WHERE choice_student_id=%s;
        """, (student_id,))
    result = cursor.fetchall()
    choices = []
    for row in result:
        choices.append({
            **row,
            'curriculum_choice_number': get_curriculum_choice_count(row['choice_curriculum_id']),
            'curriculum_utilization_resources': ResourceManager(row['curriculum_utilization_string']).list
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'choices': choices
        }
    }

class drawing_course_req(BaseModel):
    course_id: str
    semester_id: int

@router.post("/drawingCourse")
async def drawing_course(req: drawing_course_req):
    course_id, semester_id = req.course_id, req.semester_id
    if not check_course_id_exist(course_id):
        return {
            'success': False,
            'errCode': 400401,
            'data': {}
        }
    if not check_course_id_exist(course_id):
        return {
            'success': False,
            'errCode': 400402,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("CALL drawingCourse(%s, %s)", (course_id, semester_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class add_attendance_req(BaseModel):
    student_id: str
    curriculum_id: int
    operator_id: str

@router.post("/addAttendance")
async def add_attendance(req: add_attendance_req):
    student_id, curriculum_id, operator_id = req.student_id, req.curriculum_id, req.operator_id
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400501,
            'data': {}
        }
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 400502,
            'data': {}
        }
    course_id = get_curriculum_course_id(curriculum_id)
    if check_attendance_course_is_chosen(student_id, course_id):
        return {
            'success': False,
            'errCode': 400503,
            'data': {}
        }
    curriculum_capacity = get_curriculum_capacity(curriculum_id)
    curriculum_chosen_count = get_attendance_curriculum_chosen_count(curriculum_id)
    if curriculum_chosen_count >= curriculum_capacity:
        return {
            'success': False,
            'errCode': 400504,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO attendance_table (attendance_student_id, attendance_curriculum_id) VALUES (%s, %s)", (student_id, curriculum_id))
    cursor.execute("DELETE FROM choice_table WHERE choice_student_id=%s AND choice_curriculum_id=%s", (student_id, curriculum_id))
    conn.commit()
    add_selection_audit(student_id, curriculum_id, 4, operator_id)
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class delete_attendance_req(BaseModel):
    student_id: str
    curriculum_id: int
    operator_id: str

@router.post("/deleteAttendance")
async def delete_attendance(req: delete_attendance_req):
    student_id, curriculum_id, operator_id = req.student_id, req.curriculum_id, req.operator_id
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400601,
            'data': {}
        }
    if not check_attendance_curriculum_is_chosen(student_id, curriculum_id):
        return {
            'success': False,
            'errCode': 400602,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("DELETE FROM attendance_table WHERE attendance_student_id=%s AND attendance_curriculum_id=%s", (student_id, curriculum_id))
    conn.commit()
    add_selection_audit(student_id, curriculum_id, 5, operator_id)
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.get("/queryStudentAttendances")
async def query_student_attendances(student_id: str):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400701,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM queryStudentAttendances qsa
        WHERE qsa.attendance_student_id=%s;
        """, (student_id,))
    result = cursor.fetchall()
    attendances = []
    for row in result:
        attendances.append({
            **row,
            'curriculum_attendance_number': get_curriculum_attendance_count(row['attendance_curriculum_id']),
            'curriculum_utilization_resources': ResourceManager(row['curriculum_utilization_string']).list
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'attendances': attendances
        }
    }

@router.get("/queryCurriculumChoices")
async def query_curriculum_choices(curriculum_id: int):
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 400801,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM queryCurriculumChoices qcc
        WHERE qcc.choice_curriculum_id=%s;
        """, (curriculum_id,))
    result = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'choices': result
        }
    }

@router.get("/queryCurriculumAttendances")
async def query_curriculum_attendances(curriculum_id: int):
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 400901,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM queryCurriculumAttendances qca
        WHERE qca.attendance_curriculum_id=%s;
        """, (curriculum_id,))
    result = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'attendances': result
        }
    }