import datetime as dt
import typing as tp
from uuid import UUID

import asyncpg


class User:
    @staticmethod
    async def create(con: asyncpg.Connection, username: str, password: str) -> tp.Optional[UUID]:
        query = '''
        INSERT INTO users (username, hashed_password) VALUES ($1, crypt($2, gen_salt('bf', 10))) RETURNING id;
        '''
        return await con.fetchval(query, username, password)


    @staticmethod
    async def verify(con: asyncpg.Connection, username: str,  password: str) -> tp.Optional[UUID]:
        query = '''
        SELECT id FROM users WHERE username=$1 AND hashed_password = crypt($2, hashed_password);
        '''
        return await con.fetchval(query, username, password)
