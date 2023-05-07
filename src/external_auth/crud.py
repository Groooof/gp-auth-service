import typing as tp
from uuid import UUID

import asyncpg


class App:
    @staticmethod
    async def get_domain(con: asyncpg.Connection, app_id: str) -> tp.Optional[str]:
        query = '''
        SELECT host FROM apps WHERE id = $1
        '''
        return await con.fetchval(query, app_id)
    
    @staticmethod
    async def get_client_secret(con: asyncpg.Connection, app_id: str) -> tp.Optional[str]:
        query = '''
        SELECT secret FROM apps WHERE id = $1
        '''
        return await con.fetchval(query, app_id)


class AppUser:
    @staticmethod
    async def verify(con: asyncpg.Connection, app_id: str, username: str, password: str, sym_key: str) -> tp.Optional[UUID]:
        query = '''
        SELECT
          au.id
        FROM
          apps a
          JOIN apps_users au ON au.app_id = a.id
        WHERE
          a.id = $1
          AND au.username = $2
          AND pgp_sym_decrypt(au.encrypted_password, $4) = crypt($3, pgp_sym_decrypt(au.encrypted_password, $4))
        '''
        return await con.fetchval(query, app_id, username, password, sym_key)
