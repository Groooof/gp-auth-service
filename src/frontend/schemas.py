from uuid import UUID
import re

import pydantic as pd


def validate_url_structure(v):
    regex = '^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$'
    if not re.match(regex, v):
        raise ValueError
    return v


class GetAppsAuthPage:
    class Request:
        class Query(pd.BaseModel):
            response_type: str
            client_id: UUID
            state: str
            nonce: str
            redirect_uri: str
            
            # _redirect_uri_validator = pd.validator('redirect_uri')(validate_url_structure)