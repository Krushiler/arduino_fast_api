from pydantic import BaseModel


class User(BaseModel):
    id: int
    login: int
    password: int


class LedConfiguration(BaseModel):
    id: int
    value: str
    user_id: int
