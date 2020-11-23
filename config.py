# coding: utf-8

from decouple import config
import os

BASE_DIR = os.path.dirname(__file__)
DEBUG = config('DEBUG', default=False, cast=bool)

MONGO_DATABASE_URL = config('MONGO_DATABASE_URL')
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')
