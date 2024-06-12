import os
import pydantic_settings
from granian.log import LogLevels
from sqlalchemy.engine.url import URL

from dotenv import load_dotenv

load_dotenv()

class Settings(pydantic_settings.BaseSettings):
    service_name: str = "FastAPI template"
    debug: bool = False
    log_level: LogLevels = LogLevels.info

    db_driver: str = "postgresql+asyncpg"
    db_host: str = os.getenv("DB_HOST", "db")
    db_port: int = os.getenv("DB_PORT", 5432)
    db_user: str = os.getenv("DB_USER", "postgres")
    db_password: str = os.getenv("DB_PASS", "password")
    db_database: str = os.getenv("DB_NAME", "postgres")

    db_pool_size: int = 5
    db_max_overflow: int = 0
    db_echo: bool = False

    app_port: int = 8000

    @property
    def db_dsn(self) -> URL:
        return URL.create(
            self.db_driver,
            self.db_user,
            self.db_password,
            self.db_host,
            self.db_port,
            self.db_database,
        )


settings = Settings()
