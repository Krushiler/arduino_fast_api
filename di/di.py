from config import DB_FILE_NAME
from data.repository.led_repository import LedRepository
from data.repository.temperature_repository import TemperatureRepository


def get_temperature_repository() -> TemperatureRepository:
    repository = TemperatureRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()


def get_led_repository() -> LedRepository:
    repository = LedRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()
