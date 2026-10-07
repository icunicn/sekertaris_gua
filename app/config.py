from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    supabase_url: str
    supabase_secret_key: str

    telegram_bot_token: str

    orbit_api_url: str = "http://127.0.0.1:8000"

    orbit_user_id: str
    telegram_user_id: int
    orbit_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
