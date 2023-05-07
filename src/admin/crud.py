import typing as tp
import asyncpg
from uuid import UUID

from src.admin import dto


class App:
    async def create(app: dto.App.Create, con: asyncpg.Connection) -> tp.Optional[UUID]:
        query = f'''
        INSERT INTO apps ({app.fields}) VALUES ({app.values_enum}) RETURNING id
        '''
        res = await con.fetchval(query, *app.values_list)
        return res
    
    async def delete(app: dto.App.Delete, con: asyncpg.Connection) -> tp.Optional[UUID]:
        query = f'''
        DELETE FROM apps WHERE id = $1 AND owner_id=$2 RETURNING id
        '''
        res = await con.fetchval(query, app.id, app.owner_id)
        return res
    
    
class AppUser:
    async def create(app_user: dto.AppUser.Create, con: asyncpg.Connection) -> tp.Optional[UUID]:
        # шифрования сюды
        query = f'''
        INSERT INTO apps_users (username, encrypted_password, app_id)
        VALUES ($1, pgp_sym_encrypt(crypt($2, gen_salt('bf', 10)), $4), $3)
        RETURNING id
        '''
        res = await con.fetchval(query, *app_user.values_list)
        return res
    
    async def delete(app_user: dto.AppUser.Delete, con: asyncpg.Connection) -> tp.Optional[UUID]:
        query = f'''
        DELETE FROM apps_users au WHERE au.username = $1 AND au.app_id = $2 RETURNING id
        '''
        res = await con.fetchval(query, *app_user.values_list)
        return res
        
    
    async def is_owner(app_id: UUID, user_id: UUID, con: asyncpg.Connection) -> bool:
        query = '''
        SELECT EXISTS (SELECT 1 FROM apps WHERE id = $1 AND owner_id = $2)
        '''
        res = await con.fetchval(query, app_id, user_id)
        return res
        