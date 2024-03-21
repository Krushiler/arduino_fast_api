from pydantic import BaseModel


class LedConfiguration(BaseModel):
    id: int
    value: str
