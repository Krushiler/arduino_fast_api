from pydantic import BaseModel


class SetActiveConfigRequest(BaseModel):
    config_id: int
    device_id: int


class CreateConfigRequest(BaseModel):
    value: str
