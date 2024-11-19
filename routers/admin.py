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
    prefix="/Admin",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/queryPlace")
async def query_place():
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table")
    result = cursor.fetchall()
    places = []
    for row in result:
        places.append({
            'place_id': row['place_id'],
            'place_name': row['place_name']
        })
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'places': places
        }
    }

def check_place_id_exist(place_id: int):
    conn, cursor = get_cursor('root')
    cursor.execute("SELECT * FROM place_table WHERE place_id=%s", (place_id,))
    return cursor.fetchone() is not None

def check_place_exist(place_name: str, ex_place_id: int = -1):
    conn, cursor = get_cursor('root')
    if ex_place_id == -1:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s", (place_name,))
    else:
        cursor.execute("SELECT * FROM place_table WHERE place_name=%s AND place_id!=%s", (place_name, ex_place_id))
    return cursor.fetchone() is not None

class add_place_req(BaseModel):
    place_name: str

@router.post("/addPlace")
async def add_place(req: add_place_req):
    place_name = req.place_name
    conn, cursor = get_cursor('root')
    if check_place_exist(place_name):
        return {
            'success': False,
            'errCode': ERR_PLACE_DUPLICATE_1,
            'data': {}
        }
    cursor.execute("INSERT INTO place_table (place_name) VALUES (%s)", (place_name,))
    conn.commit()
    place_id = cursor.lastrowid
    return {
        'success': True,
        'errCode': OK,
        'data': {
            'place_id': place_id
        }
    }

class update_place_req(BaseModel):
    place_id: int
    place_name: str
    is_enable: int
 
@router.post("/updatePlace")
async def update_place(req: update_place_req):
    place_id, place_name, is_enable = req.place_id, req.place_name, req.is_enable
    conn, cursor = get_cursor('root')
    if not check_place_id_exist(place_id):
        return {
            'success': False,
            'errCode': ERR_PLACE_ID_NOT_FOUND,
            'data': {}
        }
    if check_place_exist(place_name, place_id):
        return {
            'success': False,
            'errCode': ERR_PLACE_DUPLICATE_2,
            'data': {}
        }
    cursor.execute("UPDATE place_table SET place_name=%s, place_is_enable=%s WHERE place_id=%s",
                        (place_name, is_enable, place_id))
    conn.commit()
    return {
        'success': True,
        'errCode': OK,
        'data': {}
    }


