import typing as tp

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import Response
import aioredis
import asyncpg

from src.dependencies import get_db_connection, get_redis_client, SessionCookie
from src.utils.crypto import generate_random_string
from src.internal_auth import schemas as sch
from src.internal_auth import crud
from src import config


router = APIRouter(tags=['internal_auth'])


@router.post('/register')
async def register(response: Response,
                   body: sch.Register.Request.Body,
                   con: asyncpg.Connection = Depends(get_db_connection)):
    
    try:
        await crud.User.create(con, body.username, body.password)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail='user_already_exists')
    response.status_code = 201


@router.post('/login')
async def login(response: Response,
                body: sch.Login.Request.Body,
                con: asyncpg.Connection = Depends(get_db_connection),
                redis: aioredis.Redis = Depends(get_redis_client)):
    
    user_id = await crud.User.verify(con, body.username, body.password)
    if user_id is None:
        raise HTTPException(status_code=400, detail='invalid_client')
    
    session = generate_random_string(config.USER_SESSION_LEN)
    await redis.set(session, str(user_id), ex=int(config.USER_SESSION_LIFETIME.total_seconds()))
    response.set_cookie(config.USER_SESSION_COOKIE_NAME, 
                        session,
                        max_age=int(config.USER_SESSION_LIFETIME.total_seconds()),
                        secure=True,
                        httponly=True)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    response.status_code = 200


@router.post('/logout')
async def logout(response: Response,
                 redis: aioredis.Redis = Depends(get_redis_client),
                 session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    await redis.delete(session)
    response.delete_cookie(config.USER_SESSION_COOKIE_NAME)
    response.status_code = 200
