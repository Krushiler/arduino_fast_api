from typing import Annotated

from fastapi import Depends

from config import DB_FILE_NAME
from data.mqtt.led_mqtt import LedMqtt
from data.repository.device_repository import DeviceRepository
from data.repository.led_repository import LedRepository
from data.repository.temperature_repository import TemperatureRepository
from data.repository.user_repository import UserRepository


def get_temperature_repository() -> TemperatureRepository:
    repository = TemperatureRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()


def get_led_mqtt() -> LedMqtt:
    mqtt = LedMqtt()
    try:
        yield mqtt
    finally:
        mqtt.close()


def get_led_repository(led_mqtt: Annotated[LedMqtt, Depends(get_led_mqtt)]) -> LedRepository:
    repository = LedRepository(DB_FILE_NAME, led_mqtt)
    try:
        yield repository
    finally:
        repository.close()


def get_user_repository() -> UserRepository:
    repository = UserRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()


def get_device_repository() -> DeviceRepository:
    repository = DeviceRepository(DB_FILE_NAME)
    try:
        yield repository
    finally:
        repository.close()
