from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import FileResponse, StreamingResponse
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
    prefix="/Faculty",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/queryDepartmentScoreStatistics")
async def query_department_score_statistics(department_id: int):
    if not check_department_id_exist(department_id):
        return {
            'success': False,
            'errCode': 700101,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM student_score_stat sss
        WHERE sss.student_department_id=%s;
        """, (department_id,))
    statistics = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'statistics': statistics
        }
    }

@router.get("/queryMajorScoreStatistics")
async def query_major_score_statistics(major_id: int):
    if not check_major_id_exist(major_id):
        return {
            'success': False,
            'errCode': 700201,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM student_score_stat sss
        WHERE sss.student_major_id=%s;
        """, (major_id,))
    statistics = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'statistics': statistics
        }
    }

@router.get("/queryClassScoreStatistics")
async def query_class_score_statistics(class_id: int):
    if not check_class_id_exist(class_id):
        return {
            'success': False,
            'errCode': 700301,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM student_score_stat sss
        WHERE sss.student_class_id=%s;
        """, (class_id,))
    statistics = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'statistics': statistics
        }
    }

@router.get("/queryCurriculumEvaluations")
async def query_curriculum_evaluations(curriculum_id: int):
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 700401,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT attendance_evaluation
        FROM attendance_table
        WHERE attendance_curriculum_id=%s;
        """, (curriculum_id,))
    evaluations = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'evaluations': evaluations
        }
    }




