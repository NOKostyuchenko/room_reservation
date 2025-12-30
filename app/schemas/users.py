from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str


class UserInBD(BaseModel):
    id: UUID
    first_name: str
    last_name: str


    class Config:
        orm_mode = True
    

class Credentials(BaseModel):
    login: str
    password: str
