import random
from typing import List

from fastapi import APIRouter, Depends

from data.api.led.schemes import SetActiveConfigRequest, CreateConfigRequest, RegisterUserRequest, RegisterDeviceRequest
from di.di import get_led_repository, get_user_repository, get_device_repository
from domain.led_configuration import LedConfiguration

router = APIRouter()


@router.post("/user/register", response_model=int | None)
async def get_led_configurations(request: RegisterUserRequest, repository=Depends(get_user_repository)):
    values = await repository.register(request.login, request.password)
    return values


@router.post("/device/register")
async def get_led_configurations(request: RegisterDeviceRequest, repository=Depends(get_device_repository)):
    await repository.add_device(request.user_id, request.device_id)
    return True


@router.get("/all", response_model=List[LedConfiguration])
async def get_led_configurations(user_id: int = 1, repository=Depends(get_led_repository)):
    values = await repository.get_configs(user_id)
    return values


@router.patch("/active")
async def set_active_led_configuration(request: SetActiveConfigRequest, repository=Depends(get_led_repository)):
    await repository.set_active_config(request.config_id, request.device_id)
    return True


@router.get("/active", response_model=LedConfiguration)
async def get_active_led_configuration(device_id: str, repository=Depends(get_led_repository)):
    values = await repository.get_active_config(device_id)
    return values


@router.post("", response_model=LedConfiguration)
async def create_led_configuration(request: CreateConfigRequest, repository=Depends(get_led_repository)):
    return await repository.add_config(request.value, request.user_id)


@router.get('/generate')
def generate_color_combination(pixel_count: int) -> str:
    colors = list()
    pixel_color = random.randint(1, 3)
    value = random.randint(0, 120)
    if len(str(value)) == 2:
        value = "0" + str(value)
    if len(str(value)) == 1:
        value = "00" + str(value)
    series = (255 - int(value)) // pixel_count
    value = int(value)
    for i in range(pixel_count):
        value += series
        if pixel_color == 1:
            colors.append(str(value) + "000000")  # red
        if pixel_color == 2:
            colors.append("000" + str(value) + "000")  # green
        if pixel_color == 3:
            colors.append("000000" + str(value))  # blue
    return ''.join(colors)
