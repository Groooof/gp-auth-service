import typing as tp
from uuid import UUID

import pydantic as pd

from src.dto import CrudDTO


class App:
    class FullRead(pd.BaseModel, CrudDTO):
        name: str
        client_id: UUID
        client_secret: str
        host: str
        users: tp.List[tp.Optional[str]]
