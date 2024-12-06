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
    course_id, course_type = get_curriculum_course_info(curriculum_id)
    if order >= order_limit[course_type]:
        return {
            'success': False,
            'errCode': 400105,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO choice_table (choice_student_id, choice_curriculum_id, choice_order, choice_introduction) VALUES (%s, %s, %s, %s)", (student_id, curriculum_id, order, introduction))
    conn.commit()
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
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.get("/queryStudentChoice")
async def query_student_choice(student_id: str, semester_id: int):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 400301,
            'data': {}
        }
    if not check_semester_id_exist(semester_id):
        return {
            'success': False,
            'errCode': 400302,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
SELECT
    ch.choice_curriculum_id,
    ct.curriculum_course_id,
    cot.course_name,
    cot.course_type,
    cot.course_credit,
    cot.course_hours,
    ct.curriculum_teacher_id,
    tt.teacher_name,
    ct.curriculum_capacity,
    ct.curriculum_info,
    cust.curriculum_utilization_string,
    ch.choice_order,
    ch.choice_introduction
FROM
    choice_table ch
JOIN
    curriculum_table ct
ON
    ch.choice_curriculum_id = ct.curriculum_id
JOIN
    course_table cot
ON
    ct.curriculum_course_id = cot.course_id
JOIN
    teacher_table tt
ON
    ct.curriculum_teacher_id = tt.teacher_id
LEFT JOIN
    curriculum_utilization_string_table cust
ON
    ct.curriculum_id = cust.curriculum_id
WHERE
    ch.choice_student_id = %s AND ct.curriculum_semester_id = %s
ORDER BY
    ct.curriculum_id, ch.choice_order;
""", (student_id, semester_id))
    result = cursor.fetchall()
    choices = []
    for row in result:
        choices.append({
            'choice_curriculum_id': row['choice_curriculum_id'],
            'curriculum_course_id': row['curriculum_course_id'],
            'course_name': row['course_name'],
            'course_type': row['course_type'],
            'course_credit': row['course_credit'],
            'course_hours': row['course_hours'],
            'curriculum_teacher_id': row['curriculum_teacher_id'],
            'teacher_name': row['teacher_name'],
            'curriculum_capacity': row['curriculum_capacity'],
            'curriculum_info': row['curriculum_info'],
            'curriculum_utilization_string': row['curriculum_utilization_string'],
            'choice_order': row['choice_order'],
            'choice_introduction': row['choice_introduction']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'choices': choices
        }
    }
