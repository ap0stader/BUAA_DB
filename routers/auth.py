from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
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

router = APIRouter(
    prefix="/Auth",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=conf.EXPIRE_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def get_user(username: str):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM login_table WHERE login_id=%s", (username,))
    result = cursor.fetchone()
    return result

def update_audit_table(username: str, result: int):
    conn, cursor = get_cursor('root')
    cursor.execute("INSERT INTO login_audit_table (login_audit_claim, login_audit_result) VALUES (%s, %s)", (username[:30], result))
    conn.commit()

class login_req(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(req: login_req):
    username, password = req.username, req.password
    user = get_user(username)
    if user is None:
        update_audit_table(username, 1)
        return {
            'success': False,
            'errCode': ERR_AUTH__LOGIN_FAILED,
            'data': {}
        }
    if user['login_password'] != password:
        update_audit_table(username, 2)
        return {
            'success': False,
            'errCode': ERR_AUTH__LOGIN_FAILED,
            'data': {}
        }
    if user['login_is_enable'] == 0:
        update_audit_table(username, 3)
        return {
            'success': False,
            'errCode': ERR_AUTH__ACOUNT_BANNED,
            'data': {}
        }
    update_audit_table(username, 0)
    role = user['login_role']
    token = create_access_token(data={"sub": user['login_id']})
    rds.set(token, user['login_id'], ex=conf.EXPIRE_TIME_MINUTES*60)
    return {
        'success': True,
        'errCode': OK,
        'data': {
            "token": token,
            "type": role
        }
    }

@router.get("/verify")
async def verify(token: str):
    if rds.get(token) is None:
        return {
            'success': False,
            'errCode': ERR_AUTH__TOKEN_EXPIRE,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }

class update_password_req(BaseModel):
    username: str
    oldPassword: str
    newPassword: str

@router.post("updatePassword")
async def updatePassword(req: update_password_req):
    username, oldPassword, newPassword = req.username, req.oldPassword, req.newPassword
    user = get_user(username)
    if user is None:
        return {
            'success': False,
            'errCode': ERR_AUTH__LOGIN_ID_NOT_FOUND,
            'data': {}
        }
    if user['login_password'] != oldPassword:
        return {
            'success': False,
            'errCode': ERR_AUTH__PASSWORD_NOT_MATCH,
            'data': {}
        }
    conn, cursor = get_cursor('root')
    cursor.execute("UPDATE login_table SET login_password=%s WHERE login_id=%s", (newPassword, username))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }
    