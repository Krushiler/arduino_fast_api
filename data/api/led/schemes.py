from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    login: str
    password: str


class RegisterDeviceRequest(BaseModel):
    user_id: int
    device_id: str


class SetActiveConfigRequest(BaseModel):
    config_id: int
    device_id: str


class CreateConfigRequest(BaseModel):
    value: str
    user_id: int
