'''Configuration settings for Flask API Template.'''

import os
from pathlib import Path


CUR_PATH = Path(__file__).parent

SQLITE_DEV = 'sqlite:///' + str(CUR_PATH / 'flask_api_template_dev.db')
SQLITE_TEST = 'sqlite:///' + str(CUR_PATH / 'flask_api_template_test.db')
SQLITE_PROD = 'sqlite:///' + str(CUR_PATH / 'flask_api_template_prod.db')


class Config:
    '''Basic configuration for Flask API'''

    APP_NAME = 'Flask API Template'
    SECRET_KEY = os.getenv('SECRET_KEY')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class TestingConfig(Config):
    '''Testing configuration.'''

    TESTING = True
    SQLALCHEMY_DATABASE_URI = SQLITE_TEST


class DevelopmentConfig(Config):
    '''Development configuration.'''

    TOKEN_EXPIRE_MINUTES = 15
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_DEV)


class ProductionConfig(Config):
    '''Production configuration.'''

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", SQLITE_PROD)
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
