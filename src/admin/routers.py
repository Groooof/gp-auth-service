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
                     con: asyncpg.Connection = Depends(get_db_connection),
                     session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    secret = crypto.generate_random_string(config.APP_SECRET_LEN)
    app = dto.App.Create(secret=secret, owner_id=user_id, **body.dict())
    app_id = await crud.App.create(app, con)
    response.status_code = 201
    return sch.CreateApp.Response.Body(app_id=app_id)


@router.delete('/apps/{app_id}')
async def delete_app(app_id: uuid.UUID,
                     response: Response,
                     con: asyncpg.Connection = Depends(get_db_connection),
                     session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    app = dto.App.Delete(id=app_id, owner_id=user_id)
    app_id = await crud.App.delete(app, con)
    if app_id is None:
        raise HTTPException(status_code=404, detail='app_does_not_exist')
    response.status_code = 200


@router.post('/apps/{app_id}/users')
async def create_app_user(app_id: uuid.UUID,
                          body: sch.CreateAppUser.Request.Body,
                          response: Response,
                          con: asyncpg.Connection = Depends(get_db_connection),
                          session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    
    if not await crud.AppUser.is_owner(app_id, user_id, con):
        raise HTTPException(status_code=404, detail='app_does_not_exist')
    
    app_user = dto.AppUser.Create(app_id=app_id,
                                 username=body.username,
                                 password=body.password,
                                 sym_key=config.postgres_env.SECRET)
    try:
        app_user_id = await crud.AppUser.create(app_user, con)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail='user_already_exists')
        
    response.status_code = 201
    return sch.CreateAppUser.Response.Body(app_user_id=app_user_id)


@router.delete('/apps/{app_id}/users')
async def delete_app_user(app_id: uuid.UUID,
                          response: Response,
                          query = Depends(sch.DeleteAppUser.Request.Query),
                          con: asyncpg.Connection = Depends(get_db_connection),
                          session_data: str = Depends(SessionCookie())):
    
    session, user_id = session_data
    
    if not await crud.AppUser.is_owner(app_id, user_id, con):
        raise HTTPException(status_code=404, detail='app_does_not_exist')

    app_user = dto.AppUser.Delete(username=query.username, app_id=app_id)
    app_user_id = await crud.AppUser.delete(app_user, con)
    if app_user_id is None:
        raise HTTPException(status_code=404, detail='user_does_not_exist')
    response.status_code = 200
