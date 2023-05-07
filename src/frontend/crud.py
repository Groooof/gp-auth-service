import typing as tp
import asyncpg
from uuid import UUID

from src.frontend import dto


class User:
    @staticmethod
    async def get_apps(con: asyncpg.Connection, user_id: tp.Optional[tp.Union[str, UUID]]) -> tp.List[dto.App.FullRead]:
        query = '''
          SELECT
            a.name AS name,
            a.id AS client_id,
            a.secret AS client_secret,
            a.host AS host,
            COALESCE(NULLIF(array_agg(au.username), ARRAY[NULL]::text[]), ARRAY[]::text[]) AS users
          FROM
            users u
            JOIN apps a ON a.owner_id = u.id
            LEFT JOIN apps_users au ON au.app_id = a.id
          WHERE
            u.id = $1
          GROUP BY
            a.name,
            a.id,
            a.secret,
            a.host,
            a.created_at
          ORDER BY a.created_at DESC
        '''
        res = await con.fetch(query, user_id)
        return [dto.App.FullRead(**row) for row in res]
