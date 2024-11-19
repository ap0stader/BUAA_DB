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

class User(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=conf.EXPIRE_TIME_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_user(user: User):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM login_table WHERE login_id=%s AND login_password=%s", (user.username, user.password))
    result = cursor.fetchone()
    cursor.execute("INSERT INTO login_audit_table (login_audit_claim, login_audit_result) VALUES (%s, %s)",
                        (user.username[:30], 1 if result is not None else 0))
    conn.commit()
    if result is None:
        return -1
    return result['login_role']

@router.post("/login")
async def login(user: User):
    role = verify_user(user)
    if role < 0:
        return {
            'success': False,
            'errCode': ERR_LOGIN_FAILED,
            'data': {}
        }
    token = create_access_token(data={"sub": user.username})
    rds.set(token, user.username, ex=conf.EXPIRE_TIME_MINUTES*60)
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
            'errCode': ERR_TOKEN_EXPIRE,
            'data': {}
        }
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }
