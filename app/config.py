from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    instagram_access_token: str
    instagram_app_secret: str
    instagram_verify_token: str

    log_level: str = "INFO"
    database_url: str = "sqlite:///./instagram_trigger.db"


settings = Settings()
