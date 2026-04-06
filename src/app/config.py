from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_env: str = Field(default="dev", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    db_path: str = Field(default="./data/maeto.db", alias="DB_PATH")
    base_url: str = Field(
        default="https://www.lojamaeto.com",
        alias="BASE_URL",
    )

    http_timeout: int = Field(default=20, alias="HTTP_TIMEOUT")
    user_agent: str = Field(
        default="Mozilla/5.0 (compatible; LojaMaetoWebscraper/1.0)",
        alias="USER_AGENT",
    )

    @property
    def database_url(self) -> str:
        return f"sqlite:///{self.db_path}"


config = Config()
