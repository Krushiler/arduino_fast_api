import data.storage_initializer as storage
from config import DB_FILE_NAME
from fastapi import FastAPI
from data.api.temperature.routing import router as temperature_router
from data.api.led.routing import router as led_router
import uvicorn

storage.initialize_storage(DB_FILE_NAME)
app = FastAPI()
app.include_router(temperature_router, prefix="/temperature")
app.include_router(led_router, prefix="/led")
uvicorn.run(app, host="192.168.159.157", port=5000)
