from config import DB_FILE_NAME
from data.repository.temperature_repository import TemperatureRepository


def get_temperature_repository():
    repository = TemperatureRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()
