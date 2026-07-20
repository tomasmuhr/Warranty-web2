from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from os import getenv


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # app_env: str = "production"
    # db_name: str = "warranty.db"
    # db_name_backup: str = "warranty_bkp.db"
    # db_dir: Path = Path("instance")
    # records_per_page: int = 30
    # cors_origins: str = "http://localhost:5173,http://localhost:8080"
    app_env: str = getenv("APP_ENV", "production")
    db_name: str = getenv("DB_NAME", "warranty.db")
    db_name_backup: str = getenv("DB_NAME_BACKUP", "warranty_bkp.db")
    db_dir: Path = Path(getenv("DB_DIR", "instance"))
    records_per_page: int = int(getenv("RECORDS_PER_PAGE", 30))
    cors_origins: str = getenv(
        "CORS_ORIGINS", "http://localhost:5173,http://localhost:8080"
    )

    @property
    def database_path(self) -> Path:
        return self.db_dir / self.db_name

    @property
    def database_url(self) -> str:
        self.db_dir.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{self.database_path.as_posix()}"

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip() for origin in self.cors_origins.split(",") if origin.strip()
        ]


settings = Settings()

if settings.app_env == "development":
    settings.records_per_page = 5
