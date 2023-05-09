import typing as tp

import asyncpg
import aioredis
from urllib.parse import urlparse


from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.frontend import schemas as sch
from src.frontend import crud as frontend_crud
from src.external_auth import crud as ext_auth_crud
from src.dependencies import get_db_connection, SessionCookie, get_redis_client
from src.external_auth.service import GraphicalPasswordManager
from src import config
from src.utils import crypto


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get('/admin', tags=['admin'])
async def get_admin_page(request: Request,
                         con: asyncpg.Connection = Depends(get_db_connection),
                         session_data: str = Depends(SessionCookie(raise_exc=False))):
    
    session, user_id = session_data
    if session is None:
        return RedirectResponse('/', status_code=302)
    
    gpm = GraphicalPasswordManager(config.GRAPHICAL_PASSWORD_SIZE)
    
    apps = await frontend_crud.User.get_apps(con, user_id)
    return templates.TemplateResponse('admin.html', {'request': request,
                                                     'apps': apps,
                                                     'gp_data': gpm.get_random_matrix()
                                                     })


@router.get('/', tags=['internal_auth'])
async def get_internal_auth_page(request: Request, 
                                 session_data: str = Depends(SessionCookie(raise_exc=False))):
    
    session, user_id = session_data
    if session is not None:
        return RedirectResponse('/admin', status_code=302)
    return templates.TemplateResponse("reg_log.html", {"request": request})


@router.get('/authorize', tags=['external_auth'])
async def get_external_auth_page(request: Request,
                                 query = Depends(sch.GetExternalAuthPage.Request.Query),
                                 con: asyncpg.Connection = Depends(get_db_connection)):
    
    received_domain = urlparse(query.redirect_uri).netloc
    stored_domain = await ext_auth_crud.App.get_domain(con, query.client_id)
    
    if received_domain != stored_domain:
        raise HTTPException(status_code=400, detail='invalid_request')

    gpm = GraphicalPasswordManager(config.GRAPHICAL_PASSWORD_SIZE)
    return templates.TemplateResponse("gp_log.html",
                                      {"request": request,
                                       "query_params": request.query_params, 
                                       "step_1_data": gpm.get_random_matrix(),
                                       "step_2_data": gpm.get_random_matrix(),
                                       "step_3_data": gpm.get_random_matrix()})


