from pydantic import BaseModel

from typing import List


class AddTemperatureRequest(BaseModel):
    temperature: float
    location: str | None


class GetTemperatureResponse(BaseModel):
    temperatures: List[float]
    location: str | None
