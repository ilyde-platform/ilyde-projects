# coding: utf-8

from decouple import config
import os

BASE_DIR = os.path.dirname(__file__)
DEBUG = config('DEBUG', default=False, cast=bool)

MONGO_DATABASE_URL = config('MONGO_DATABASE_URL')
MONGO_USER = config('MONGO_USER')
MONGO_PASSWORD = config('MONGO_PASSWORD')

KEYCLOAK_CLIENT_ID = config('KEYCLOAK_CLIENT_ID')
KEYCLOAK_CLIENT_SECRET = config('KEYCLOAK_CLIENT_SECRET')
KEYCLOAK_IDENTITY_OPENID_CONFIG_URL = config('KEYCLOAK_IDENTITY_OPENID_CONFIG_URL')
MINIO_STS = config('MINIO_STS')
MINIO_ENDPOINT = config('MINIO_ENDPOINT')