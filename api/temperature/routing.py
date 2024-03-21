from fastapi import APIRouter, Depends

from api.temperature.schemes import GetTemperatureResponse, AddTemperatureRequest
from di.di import get_temperature_repository

router = APIRouter()


@router.get("/all")
async def get_devices(location: str = "home", repository=Depends(get_temperature_repository)):
    values = await repository.get_temperatures(location)
    return GetTemperatureResponse(temperatures=values, location=location)


@router.post("")
async def create_device(request: AddTemperatureRequest, repository=Depends(get_temperature_repository)):
    await repository.add_temperature(request.temperature, request.location)
    return True
