class Config:
    """
    Flask configuration file
    """
    FLASK_ENV = 'develop'
    TESTING = True

    # provide default connection variables need to be overwritten by actual configuration
    P2REST_DB_HOST = 'localhost'
    P2REST_DB_PORT = 5432
    P2REST_DB_NAME = 'postgres'
    P2REST_DB_USER = 'postgres'
    P2REST_DB_PASSWORD = 'postgres'
    P2REST_MAX_RESULTS = 10000


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    ENV = 'production'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    ENV = 'development'


class TestConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    ENV = 'testing'


config_by_name = dict(
    dev=DevConfig,
    test=TestConfig,
    prod=ProdConfig
)
