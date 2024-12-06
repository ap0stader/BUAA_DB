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
    prefix="/Audit",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/queryLoginAudit")
async def query_login_audit(page: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM login_audit_table")
    count = len(cursor.fetchall())
    offset = (page - 1) * 50
    cursor.execute("""
SELECT
    lat.login_audit_id,
    lat.login_audit_claim,
    lat.login_audit_time,
    lat.login_audit_result
FROM
    login_audit_table lat
ORDER BY
    lat.login_audit_id DESC
LIMIT 50 OFFSET %s;
""", (offset,))
    result = cursor.fetchall()
    audits = []
    for row in result:
        audits.append({
            'login_audit_id': row['login_audit_id'],
            'login_audit_claim': row['login_audit_claim'],
            'login_audit_time': row['login_audit_time'],
            'login_audit_result': row['login_audit_result']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'count': count,
            'audits': audits
        }
    }

@router.get("/querySelectionAudit")
async def query_selection_audit(page: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM selection_audit_table")
    count = len(cursor.fetchall())
    offset = (page - 1) * 50
    cursor.execute("""
SELECT
    sat.selection_audit_id,
    sat.selection_audit_student_id,
    sat.selection_audit_operator_id,
    sat.selection_audit_curriculum_id,
    ct.curriculum_course_id,
    cot.course_name,
    cot.course_type,
    ct.curriculum_teacher_id,
    tt.teacher_name,
    ct.curriculum_semester_id,
    st.semester_name,
    ct.curriculum_info,
    cust.curriculum_utilization_string,
    sat.selection_audit_type,
    sat.selection_audit_time
FROM
    selection_audit_table sat
JOIN
    curriculum_table ct
ON
    sat.selection_audit_curriculum_id = ct.curriculum_id
JOIN
    course_table cot
ON
    ct.curriculum_course_id = cot.course_id
JOIN
    teacher_table tt
ON
    ct.curriculum_teacher_id = tt.teacher_id
JOIN
    semester_table st
ON
    ct.curriculum_semester_id = st.semester_id
LEFT JOIN
    curriculum_utilization_string_table cust
ON
    ct.curriculum_id = cust.curriculum_id
ORDER BY
    sat.selection_audit_id DESC
LIMIT 50 OFFSET %s;
""", (offset,))
    result = cursor.fetchall()
    audits = []
    for row in result:
        audits.append({
            'selection_audit_id': row['selection_audit_id'],
            'selection_audit_student_id': row['selection_audit_student_id'],
            'selection_audit_operator_id': row['selection_audit_operator_id'],
            'selection_audit_curriculum_id': row['selection_audit_curriculum_id'],
            'curriculum_course_id': row['curriculum_course_id'],
            'course_name': row['course_name'],
            'course_type': row['course_type'],
            'curriculum_teacher_id': row['curriculum_teacher_id'],
            'teacher_name': row['teacher_name'],
            'curriculum_semester_id': row['curriculum_semester_id'],
            'semester_name': row['semester_name'],
            'curriculum_info': row['curriculum_info'],
            'curriculum_utilization_string': row['curriculum_utilization_string'],
            'selection_audit_type': row['selection_audit_type'],
            'selection_audit_time': row['selection_audit_time']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'count': count,
            'audits': audits
        }
    }

@router.get("/querySelectionAuditByStudentID")
async def query_selection_audit_by_student_id(student_id: str):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 700301,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
SELECT
    sat.selection_audit_id,
    sat.selection_audit_student_id,
    sat.selection_audit_operator_id,
    sat.selection_audit_curriculum_id,
    ct.curriculum_course_id,
    cot.course_name,
    cot.course_type,
    ct.curriculum_teacher_id,
    tt.teacher_name,
    ct.curriculum_semester_id,
    st.semester_name,
    ct.curriculum_info,
    cust.curriculum_utilization_string,
    sat.selection_audit_type,
    sat.selection_audit_time
FROM
    selection_audit_table sat
JOIN
    curriculum_table ct
ON
    sat.selection_audit_curriculum_id = ct.curriculum_id
JOIN
    course_table cot
ON
    ct.curriculum_course_id = cot.course_id
JOIN
    teacher_table tt
ON
    ct.curriculum_teacher_id = tt.teacher_id
JOIN
    semester_table st
ON
    ct.curriculum_semester_id = st.semester_id
LEFT JOIN
    curriculum_utilization_string_table cust
ON
    ct.curriculum_id = cust.curriculum_id
WHERE
    sat.selection_audit_student_id = %s
ORDER BY
    sat.selection_audit_id DESC;
""", (student_id,))
    result = cursor.fetchall()
    audits = []
    for row in result:
        audits.append({
            'selection_audit_id': row['selection_audit_id'],
            'selection_audit_student_id': row['selection_audit_student_id'],
            'selection_audit_operator_id': row['selection_audit_operator_id'],
            'selection_audit_curriculum_id': row['selection_audit_curriculum_id'],
            'curriculum_course_id': row['curriculum_course_id'],
            'course_name': row['course_name'],
            'course_type': row['course_type'],
            'curriculum_teacher_id': row['curriculum_teacher_id'],
            'teacher_name': row['teacher_name'],
            'curriculum_semester_id': row['curriculum_semester_id'],
            'semester_name': row['semester_name'],
            'curriculum_info': row['curriculum_info'],
            'curriculum_utilization_string': row['curriculum_utilization_string'],
            'selection_audit_type': row['selection_audit_type'],
            'selection_audit_time': row['selection_audit_time']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'audits': audits
        }
    }
