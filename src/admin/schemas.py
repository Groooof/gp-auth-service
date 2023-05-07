from uuid import UUID

import pydantic as pd

    
class CreateApp:
    class Request:
        class Body(pd.BaseModel):
            host: str = pd.Field(min_length=3)
            name: str = pd.Field(min_length=1)
            
    class Response:
        class Body(pd.BaseModel):
            app_id: UUID


class CreateAppUser:
    class Request:
        class Body(pd.BaseModel):
            username: str = pd.Field(min_length=1)
            password: str = pd.Field(min_length=2)
            
    class Response:
        class Body(pd.BaseModel):
            app_user_id: UUID

            
class DeleteAppUser:
    class Request:
        class Query(pd.BaseModel):
            username: str = pd.Field(min_length=1)
