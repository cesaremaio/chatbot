from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    plain_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
