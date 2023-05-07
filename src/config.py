from pydantic import BaseSettings
import datetime as dt
import pathlib
import os


class BaseEnv(BaseSettings):
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class PostgresEnv(BaseEnv):
    """
    Переменные окружения.
    """
    USER: str
    PASSWORD: str
    DB: str
    HOST: str
    PORT: str
    SECRET: str

    class Config:
        env_prefix = 'POSTGRES_'
    

# gen random syms
# sudo < /dev/random tr -dc A-Za-z0-9 | head -c 32; echo

postgres_env = PostgresEnv()
POSTGRES_DSN = os.environ.get('DATABASE_URL')
REDIS_DSN = os.environ.get('REDIS_URL')

AUTHENTICATION_CODE_LEN = 64
AUTHENTICATION_CODE_LIFETIME = dt.timedelta(minutes=5)
USER_SESSION_LEN = 64
USER_SESSION_LIFETIME = dt.timedelta(minutes=999)
# USER_SESSION_LIFETIME = dt.timedelta(seconds=10)
USER_SESSION_COOKIE_NAME = 'session'
APP_SECRET_LEN = 64
GRAPHICAL_PASSWORD_SIZE = 8
