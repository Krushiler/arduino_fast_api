from typing import List

from fastapi import APIRouter, Depends

from data.api.led.schemes import SetActiveConfigRequest, CreateConfigRequest
from di.di import get_led_repository
from domain.led_configuration import LedConfiguration

router = APIRouter()


@router.get("/all", response_model=List[LedConfiguration])
async def get_led_configurations(repository=Depends(get_led_repository)):
    values = await repository.get_configs()
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
    return await repository.add_config(request.value)
