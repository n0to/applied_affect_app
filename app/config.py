from pydantic import BaseSettings, FilePath
from functools import lru_cache
from loguru import logger
import os


@lru_cache()
def get_settings():
    deployment_environ = os.environ.get('AA_DEPLOYMENT_ENV', 'test')
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    file = "{}/{}.env".format(curr_dir, deployment_environ)
    if deployment_environ == 'test':
        file = "test.env"
    logger.info(f"Processing configuration file:{file}")
    return Settings(_env_file=file, _env_file_encoding='utf-8')


@lru_cache()
def get_settings_from_file(file: FilePath):
    logger.info(f"Processing configuration file:{file}")
    return Settings(_env_file=file, _env_file_encoding='utf-8')


class Settings(BaseSettings):
    app_name: str = "Applied Affect API"
    logging_level: str
    environment: str
    mongo_conn_str: str
    mongo_dbname: str
    mongo_username: str
    mongo_password: str
    mongo_host: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
