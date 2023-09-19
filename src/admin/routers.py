import typing as tp
import asyncpg
import uuid

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException

from src.dependencies import get_db_connection, SessionCookie
from src.admin import schemas as sch
from src.utils import crypto
from src.admin import crud
from src.admin import dto
from src import config


router = APIRouter(prefix='/admin' ,tags=['admin'])


@router.post('/apps')
async def create_app(body: sch.CreateApp.Request.Body,
                     response: Response,
                     con = Depends(get_db_connection),
                     session_data: str = Depends(SessionCookie())):
    '''
    Метод, выполняющий создание объекта клиентского приложения
    '''
    # получение сессионного токена и id пользователя
    session, user_id = session_data
    # генерация секрутного ключа для приложения
    secret = crypto.generate_random_string(config.APP_SECRET_LEN)
    # подготовка данных о приложении для записи в бд
    app = dto.App.Create(secret=secret,
                         owner_id=user_id,
                         **body.dict())
    # запись данных в бд и получение id приложения
    app_id = await crud.App.create(app, con)
    response.status_code = 201
    # id созданного приложения возвращается в ответе
    return sch.CreateApp.Response.Body(app_id=app_id)


@router.delete('/apps/{app_id}')
async def delete_app(app_id: uuid.UUID,
                     response: Response,
                     con = Depends(get_db_connection),
                     session_data: str = Depends(SessionCookie())):
    '''
    Метод, выполняющий удаление клиентского приложения
    '''
    # получение сессионного токена и id пользователя
    session, user_id = session_data
    # подготовка данных о приложении для обращения к бд
    app = dto.App.Delete(id=app_id, owner_id=user_id)
    # запрос к бд на удаление
    app_id = await crud.App.delete(app, con)
    # если приложения с указанным id не существует -
    # вызывается ошибка
    if app_id is None:
        raise HTTPException(status_code=404,
                            detail='app_does_not_exist')
    response.status_code = 200


@router.post('/apps/{app_id}/users')
async def create_app_user(app_id: uuid.UUID,
                          body: sch.CreateAppUser.Request.Body,
                          response: Response,
                          con = Depends(get_db_connection),
                          session_data: str = Depends(SessionCookie())):
    '''
    Метод, выполняющий регистрацию пользователя в клиентском приложении
    '''
    # получение сессионного токена и id пользователя
    session, user_id = session_data
    # если пользователь, выполняющий запрос не является владельцем
    # указанного приложения - вызывается ошибка
    if not await crud.AppUser.is_owner(app_id, user_id, con):
        raise HTTPException(status_code=404,
                            detail='app_does_not_exist')
    # подготовка данных для создания пользователя приложения
    app_user = dto.AppUser.Create(
                            app_id=app_id,
                            username=body.username,
                            password=body.password,
                            sym_key=config.postgres_env.SECRET)
    # запрос к бд на создание пользователя
    try:
        app_user_id = await crud.AppUser.create(app_user, con)
        # если пользователь с таким именем уже существует - ошибка
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409,
                            detail='user_already_exists')
        
    response.status_code = 201
    # id созданного пользователя возвращается в ответе
    return sch.CreateAppUser.Response.Body(app_user_id=app_user_id)


@router.delete('/apps/{app_id}/users')
async def delete_app_user(app_id: uuid.UUID,
                          response: Response,
                          query = Depends(
                              sch.DeleteAppUser.Request.Query
                          ),
                          con = Depends(get_db_connection),
                          session_data: str = Depends(SessionCookie())):
    '''
    Метод, выполняющий удаление пользователя в клиентском приложении
    '''
    # получение сессионного токена и id пользователя
    session, user_id = session_data
    # если пользователь, выполняющий запрос не является владельцем
    # указанного приложения - вызывается ошибка
    if not await crud.AppUser.is_owner(app_id, user_id, con):
        raise HTTPException(status_code=404,
                            detail='app_does_not_exist')
    # подготовка данных для удаления
    app_user = dto.AppUser.Delete(username=query.username,
                                  app_id=app_id)
    # запрос к бд на удаление
    app_user_id = await crud.AppUser.delete(app_user, con)
    # если пользователь с указанным именем не найден - ошибка
    if app_user_id is None:
        raise HTTPException(status_code=404,
                            detail='user_does_not_exist')
    response.status_code = 200
