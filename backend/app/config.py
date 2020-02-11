""" Provide the capability to configure the app based on target environment. """
# Flask configs: https://flask.palletsprojects.com/en/1.1.x/config/
# Flask-SqlALchemy configs: https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
# Flask-Praetorian configs: https://flask-praetorian.readthedocs.io/en/latest/notes.html#configuration-settings
import os
from typing import Dict

from dotenv import load_dotenv

DB_USERNAME: str = os.environ["RTW_PQL_USERNAME"]
DB_PASSWORD: str = os.environ["RTW_PQL_PASSWORD"]
DB_NAME: str = os.getenv("RTW_PQL_DB_NAME", "rtw")
DB_HOST: str = os.environ["RTW_PQL_DB_HOST"]
DB_PORT: str = os.environ["RTW_PQL_DB_PORT"]
DB_CONN_NAME: str = os.environ["RTW_PQL_DB_CONNECTION_NAME"]

REDIS_HOST: str = os.environ["REDISHOST"]
REDIS_PORT: str = os.getenv("REDISPORT", "6379")
REDIS_DB_IDX: str = os.getenv("REDISDB", "0")

UNDEF_DB_VARS = [
    var for var in [DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT] if not var
]


class Config:
    """ Base config. """

    HAT_TRICK_API_VERSION = "0.0.1"

    DEBUG: bool = False
    SECRET_KEY: str = "top secret"

    # Tracks modifications of objects and emit signals
    # This requires extra memory and should be disabled if not needed.
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # JWT Configs
    # The default length of time that a JWT may be used to access a protected endpoint
    JWT_ACCESS_LIFESPAN: Dict[str, int] = {"hours": 24}
    # The default length of time that a JWT may be refreshed. JWT may also not be
    # refreshed if its access lifespan is not expired.
    JWT_REFRESH_LIFESPAN: Dict[str, int] = {"days": 30}

    RESTPLUS_MASK_SWAGGER: bool = False

    STATIC_URL_PATH: str = ""
    STATIC_FOLDER: str = "../static"

    # Flask Migrate
    include_schema = True

    # SQLALCHEMY_ECHO: bool = True
    # print("SQLALCHEMY_ECHO:", SQLALCHEMY_ECHO)

    # Start Profit Expert Specific settings:
    PARALLEL = True
    OPTIMIZER_API_ENDPOINT = "http://localhost:8080/api/pe"
    STYLE_TO_STYLE_FILE = "data/pe/style_style_equivalence.json"

    PRODUCT_EQUIVALENCE_SERVICE_URL = (
        "https://prod-equiv.analytics.atd-us.org/api/optimizerExport"
    )
    ONLY_ALLOW_GO_FORWARD_EQUIVALENCES = True
    RETAIL_PRICE_FILE = "data/pe/retail_prices.csv"
    PROGRAM_FILES = [
        "data/pe/program_definitions/2020/bridgestone_barnn.json",
        "data/pe/program_definitions/2019/cooper_medallion.json",
        "data/pe/program_definitions/2020/goodyear_g3xpress.json",
        "data/pe/program_definitions/2020/hankook_one.json",
        "data/pe/program_definitions/2020/kumho_premium_fuel.json",
        "data/pe/program_definitions/2019/mastercraft_century_earnings_accelerator.json",
        "data/pe/program_definitions/2019/pirelli_fastrack.json",
        "data/pe/program_definitions/2019/tire_pros_edge.json",
        "data/pe/program_definitions/2020/continental_gold_tire_pros.json",
        "data/pe/program_definitions/2020/continental_gold.json",
        "data/pe/program_definitions/2020/falken_fanatic.json",
        "data/pe/program_definitions/2020/hercules_power_program.json",
        "data/pe/program_definitions/2020/michelin_alliance.json",
        "data/pe/program_definitions/2020/mickey_thompson_marketing_alliance.json",
        "data/pe/program_definitions/2020/nexen_level.json",
        "data/pe/program_definitions/2020/nitto_enthusiast_circuit.json",
        "data/pe/program_definitions/2020/toyo_driven.json",
        "data/pe/program_definitions/2020/atd_partner_1pct.json",
        "data/pe/program_definitions/2020/atd_partner_1p5pct.json",
        "data/pe/program_definitions/2020/atd_partner_2pct.json",
        "data/pe/program_definitions/2020/yokohama_advantage.json",
    ]

    # if the price of two styles is greater than this value (in USD), they cannot
    # be equivalent
    DEFAULT_MAX_ALLOWED_STYLE_PRICE_DIFF = 40
    PROFIT_OPTIMIZER_SCHEMA = "pe"
    # End Profit Expert Specific settings

    EXECUTOR_PROPAGATE_EXCEPTIONS = True
    # Password Policy
    MAX_PASSWORD_AGE = 45
    PASSWORD_HISTORY_REPEAT = 5
    """
        This regex will enforce these rules:
        At least one upper case English letter, (?=.*?[A-Z])
        At least one lower case English letter, (?=.*?[a-z])
        At least one digit, (?=.*?[0-9])
        At least one special character, (?=.*?[#?!@$%^&*-])
        Minimum eight in length .{8,} (with the anchors)
    """
    PASSWORD_POLICY = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    # End of Password Policy

    # Cache specific configs
    CACHE_TYPE: str = "simple"
    CACHE_DEFAULT_TIMEOUT: int = 14400
    CACHE_KEY_PREFIX: str = "coe-ht-"
    # End of cache specific configs


class TestingConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = "test_secret_key"

    #  Exceptions are propagated rather than handled by the the app’s error handlers.
    TESTING: bool = True

    # SQLAlchemy Connection string
    # using a Docker container with Postgres for testing
    DB_USERNAME: str = "coeuser"
    DB_PASSWORD: str = "test"
    DB_NAME: str = "rtw"
    DB_HOST: str = "localhost"
    DB_PORT: str = "4321"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
        + f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class LocalConfig(Config):
    """ Testing config. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = "my_precious_secret_key"

    #  Exceptions are propagated rather than handled by the the app’s error handlers.
    TESTING: bool = True

    # SQLAlchemy Connection string
    # using a Docker container with Postgres for testing
    DB_USERNAME: str = "coeuser"
    DB_PASSWORD: str = "local"
    DB_NAME: str = "rtw"
    DB_HOST: str = "localhost"
    DB_PORT: str = "4321"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
        + f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    """ A config to be used for development, use mocks so you don't need a DB. """

    # Override defaults from parent.
    #
    DEBUG: bool = True
    SECRET_KEY: str = os.getenv("SECRET_KEY", "my_precious_development_secret_key")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@"
        + f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    OPTIMIZER_API_ENDPOINT = "http://localhost:5000/api/pe"


class ProductionConfig(Config):
    """ Production config. """

    # Inherits defaults from parent.
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dc89aa6c-93e7-474d-a55a-b2113b25fc16")

    if os.environ.get("DEPLOYED"):
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = "/cloudsql/{}".format(DB_CONN_NAME)
        engine_url = (
            f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@"
            + f"/{DB_NAME}?host={unix_socket}"
        )
    else:
        DB_NAME: str = "rtw"
        engine_url = (
            f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@"
            + f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

    SQLALCHEMY_DATABASE_URI = engine_url

    # Cache specific configs
    CACHE_TYPE: str = "redis"
    CACHE_DEFAULT_TIMEOUT: int = 14400
    CACHE_KEY_PREFIX: str = "coe-ht-"
    CACHE_REDIS_URL: str = f"redis://@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_IDX}"
    # End of cache specific configs


config_by_name = dict(  # pylint: disable=invalid-name
    local=LocalConfig, dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig
)