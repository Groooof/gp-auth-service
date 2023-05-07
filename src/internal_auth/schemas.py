import pydantic as pd

    
class Register:
    class Request:
        class Body(pd.BaseModel):
            username: str = pd.Field(min_length=1)
            password: str = pd.Field(min_length=8)


class Login:
    class Request:
        class Body(Register.Request.Body):
            ...
