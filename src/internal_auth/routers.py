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
                   con = Depends(get_db_connection)):
    '''
    Регистрация пользователей сервиса
    '''
    # запрос к бд на создание пользовател
    try:
        await crud.User.create(con, body.username, body.password)
        # если пользователем с таким именем уже
        # существует - ошибка
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409,
                            detail='user_already_exists')
    response.status_code = 201


@router.post('/login')
async def login(response: Response,
                body: sch.Login.Request.Body,
                con = Depends(get_db_connection),
                redis = Depends(get_redis_client)):
    '''
    Аутентиикаци пользователей сервиса
    '''
    # проверка соответствия логина и пароля
    user_id = await crud.User.verify(con,
                                     body.username,
                                     body.password)
    # если пользователя с таким именем не существует
    # или пароль неверный - ошибка
    if user_id is None:
        raise HTTPException(status_code=400, detail='invalid_client')
    
    # генерация токена сессии
    session = generate_random_string(config.USER_SESSION_LEN)
    session_lifetime = int(config.USER_SESSION_LIFETIME.total_seconds())
    # сохранение токена в памяти
    await redis.set(session,
                    str(user_id),
                    ex=session_lifetime)
    # сохранение токена в cookies
    response.set_cookie(config.USER_SESSION_COOKIE_NAME, 
                        session,
                        max_age=session_lifetime,
                        secure=True,
                        httponly=True)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    response.status_code = 200


@router.post('/logout')
async def logout(response: Response,
                 redis: aioredis.Redis = Depends(get_redis_client),
                 session_data: str = Depends(SessionCookie())):
    '''
    Выход из системы пользователя сервиса
    '''
    # получение сессионного токена и id пользователя
    session, user_id = session_data
    # удаление токена из памяти
    await redis.delete(session)
    # удаление токена из cookies
    response.delete_cookie(config.USER_SESSION_COOKIE_NAME)
    response.status_code = 200
