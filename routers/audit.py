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
    cursor.execute(
"""SELECT
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