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
    prefix="/Student",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/queryScores")
async def query_score(student_id: str):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 600101,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM student_score_view WHERE student_id=%s;", (student_id,))
    scores = cursor.fetchall()
    cursor.execute("SELECT gpa, average, weighted_average FROM student_score_stat WHERE student_id=%s;", (student_id,))
    stat = cursor.fetchone()
    if not stat:
        return {
            'success': True,
            'errCode': OK,
            'data': {
                'scores': [],
                'gpa': None,
                'average': None,
                'weighted_average': None
            }
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'scores': scores,
            **stat
        }
    }

class update_evaluation_req(BaseModel):
    curriculum_id: int
    student_id: str
    evaluation: float

@router.post("/updateEvaluation")
async def update_evaluation(req: update_evaluation_req):
    curriculum_id, student_id, evaluation = req.curriculum_id, req.student_id, req.evaluation
    if not check_curriculum_id_exist(curriculum_id):
        return {
            'success': False,
            'errCode': 600201,
            'data': {}
        }
    if not check_is_student_in_curriculum(student_id, curriculum_id):
        return {
            'success': False,
            'errCode': 600202,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        UPDATE attendance_table
        SET attendance_evaluation=%s
        WHERE attendance_student_id=%s AND attendance_curriculum_id=%s;
        """, (evaluation, student_id, curriculum_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

@router.get("/queryEvaluations")
async def query_evaluation(student_id: str):
    if not check_student_id_exist(student_id):
        return {
            'success': False,
            'errCode': 600301,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("""
        SELECT * FROM queryEvaluations
        WHERE attendance_student_id=%s;
        """, (student_id,))
    evaluations = cursor.fetchall()
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'evaluations': evaluations
        }
    }
    


