import data.storage_initializer as storage
from config import DB_FILE_NAME
from fastapi import FastAPI
from api.temperature.routing import router as temperature_router
import uvicorn

storage.initialize_storage(DB_FILE_NAME)
app = FastAPI()
app.include_router(temperature_router)
uvicorn.run(app, host="172.20.10.10", port=5000)
