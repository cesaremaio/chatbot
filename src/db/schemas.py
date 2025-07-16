from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    plain_password: str

class UserUpdate(UserBase):
    hashed_password: str

## this is correct later
class UserRead(UserBase):
    id: int
    class Config:
        from_attributes = True


# just for debugging
# class UserRead(UserCreate):
#     id: int
#     class Config:
#         from_attributes = True