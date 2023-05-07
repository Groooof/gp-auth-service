import typing as tp
from uuid import UUID
import re

import pydantic as pd


def validate_url_structure(v):
    regex = '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'
    if not re.match(regex, v):
        raise ValueError
    return v


class Authenticate:
    class Request:
        class Query(pd.BaseModel):
            response_type: str
            client_id: UUID
            state: str
            nonce: str
            redirect_uri: str
            
            # _redirect_uri_validator = pd.validator('redirect_uri')(validate_url_structure)
            
        class Body(pd.BaseModel):
            username: str
            step_2_selection: str
            step_3_selection: str
            step_1_images: tp.List[tp.List[str]]
            step_2_images: tp.List[tp.List[str]]
            step_3_images: tp.List[tp.List[str]]
        
    
class Token:
    class Request:
        class Body(pd.BaseModel):
            client_secret: str
            client_id: UUID
            redirect_uri: str
            grant_type: str
            code: str
            
    class Response:
        class Body(pd.BaseModel):
            user_id: UUID
            nonce: str
