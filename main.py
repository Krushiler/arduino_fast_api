import data.storage_initializer as storage
from config import DB_FILE_NAME
from fastapi import FastAPI
from api.temperature.routing import router as temperature_router

if __name__ == '__main__':
    storage.initialize_storage(DB_FILE_NAME)
    fastapi = FastAPI()
    fastapi.include_router(temperature_router)
