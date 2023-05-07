import typing as tp
import uuid

import pydantic as pd

from src.dto import CrudDTO


class App:
    class Create(pd.BaseModel, CrudDTO):
        secret: str
        host: str
        name: str
        owner_id: str

    class Read(pd.BaseModel, CrudDTO):
        id: tp.Optional[tp.Union[str, uuid.UUID]]
        secret: tp.Optional[str]
        host: tp.Optional[str]
        name: tp.Optional[str]
        owner_id: tp.Optional[str]
        
    class Delete(pd.BaseModel, CrudDTO):
        id: tp.Union[str, uuid.UUID]
        owner_id: tp.Union[str, uuid.UUID]


class AppUser:
    class Create(pd.BaseModel, CrudDTO):
        username: str
        password: str
        app_id: uuid.UUID
        sym_key: str

    class Delete(pd.BaseModel, CrudDTO):
        username: str
        app_id: uuid.UUID
