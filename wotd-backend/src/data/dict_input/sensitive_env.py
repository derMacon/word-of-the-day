from enum import Enum


class SensitiveEnv(str, Enum):
    ENV_PASSWORD = 'POSTGRES_PASSWORD'
    ENV_USER = 'POSTGRES_USER'
    ENV_DB_NAME = 'POSTGRES_DB'
