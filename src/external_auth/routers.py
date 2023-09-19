import asyncpg
import aioredis
from urllib.parse import urlparse

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from fastapi.responses import RedirectResponse

from src.external_auth import schemas as sch
from src.dependencies import get_db_connection, SessionCookie, get_redis_client
from src.external_auth import crud
from src.external_auth.service import GraphicalPasswordManager
from src.utils import crypto
from src import config
from pprint import pprint


router = APIRouter(tags=['external_auth'])
    

@router.post('/authorize')
async def authenticate(body: sch.Authenticate.Request.Body,
                       query = Depends(sch.Authenticate.Request.Query),
                       con = Depends(get_db_connection),
                       redis = Depends(get_redis_client)):
    '''
    Аутентификация по графическому паролю
    '''
    
    # переданное доменное имя приложения
    received_domain = urlparse(query.redirect_uri).netloc
    # хранящееся в бд доменное имя приложения
    stored_domain = await crud.App.get_domain(con, query.client_id)
    # если переданный домен не совпадает с хранящимся в бд -
    # ошибка
    if received_domain != stored_domain:
        raise HTTPException(status_code=400,
                            detail='invalid_request')
    
    gpm = GraphicalPasswordManager(config.GRAPHICAL_PASSWORD_SIZE)
    # получение исходного пароля на основе введенных пользователем
    # данных
    password = gpm.get_pass_images(body.step_2_selection,
                                   body.step_3_selection,
                                   body.step_1_images,
                                   body.step_2_images,
                                   body.step_3_images)
    # проверка полученного пароля с сохраненным в бд
    app_user_id = await crud.AppUser.verify(con,
                                            query.client_id,
                                            body.username,
                                            password,
                                            config.postgres_env.SECRET)
    # если пароли не совпадают - ошибка
    if app_user_id is None:
        raise HTTPException(status_code=400, detail='invalid_client')
    # генерация кода аутентификации
    code = crypto.generate_random_string(config.AUTHENTICATION_CODE_LEN)
    auth_data = {
        'app_id': str(query.client_id), 
        'app_user_id': str(app_user_id), 
        'nonce': query.nonce
    }
    # сохранение данных в памяти
    await redis.hmset(name=code, mapping=auth_data)
    await redis.expire(name=code, time=config.AUTHENTICATION_CODE_LIFETIME)
    # генерация ссылки для перенаправления
    client_callback_url = f'{query.redirect_uri}?code={code}&state={query.state}'
    # перенаправление браузера на страницу-обработчик клиентского приложения
    return RedirectResponse(url=client_callback_url, status_code=302)


@router.post('/token')
async def get_user_data(response: Response,
                        body: sch.Token.Request.Body,
                        con = Depends(get_db_connection),
                        redis = Depends(get_redis_client)):
    # получение из памяти данных, соответствующих полученному коду
    auth_data = await redis.hgetall(name=body.code)
    # если данные не найдены или не соответствуют переданному
    # id приложения - ошибка
    if not auth_data or auth_data['app_id'] != str(body.client_id):
        raise HTTPException(status_code=400, detail='invalid_request')
    # удаляем из памяти найденные данные
    await redis.delete(body.code)
    
    # проверяем соответствие доменов
    received_domain = urlparse(body.redirect_uri).netloc
    stored_domain = await crud.App.get_domain(con, body.client_id)
    
    if received_domain != stored_domain:
        raise HTTPException(status_code=400, detail='invalid_request')

    # проверяем соответствие секретных ключей
    stored_client_secret = await crud.App.get_client_secret(
                                                    con,
                                                    body.client_id)
    if stored_client_secret != body.client_secret:
        raise HTTPException(status_code=400, detail='invalid_request')

    response.status_code = 200
    # в ответе id аутентифицированного ползователя и код nonce
    return sch.Token.Response.Body(user_id=auth_data['app_user_id'],
                                   nonce=auth_data['nonce'])
    
    