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
    cursor.execute("SELECT * FROM login_audit_table ORDER BY login_audit_id DESC LIMIT 50 OFFSET %s;", (offset,))
    audits = cursor.fetchall()
    for i in range(len(audits)):
        audits[i]['login_audit_time'] = str(audits[i]['login_audit_time'])
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
    cursor.execute("SELECT * FROM querySelectionAudit ORDER BY selection_audit_id DESC LIMIT 50 OFFSET %s;", (offset,))
    audits = cursor.fetchall()
    for i in range(len(audits)):
        audits[i]['selection_audit_time'] = str(audits[i]['selection_audit_time'])
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
    cursor.execute("SELECT * FROM querySelectionAudit WHERE selection_audit_student_id = %s ORDER BY selection_audit_id DESC;", (student_id,))
    audits = cursor.fetchall()
    for i in range(len(audits)):
        audits[i]['selection_audit_time'] = str(audits[i]['selection_audit_time'])
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'audits': audits
        }
    }
