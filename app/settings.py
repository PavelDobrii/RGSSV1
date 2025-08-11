from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    app_env: str = Field('dev', alias='APP_ENV')
    api_key: str = Field('devkey', alias='API_KEY')
    google_maps_api_key: str = Field('', alias='GOOGLE_MAPS_API_KEY')
    default_language: str = Field('en-US', alias='DEFAULT_LANGUAGE')
    default_voice: str = Field('', alias='DEFAULT_VOICE')
    cors_origins: list[str] = Field(default_factory=lambda: ['*'])

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)


settings = Settings()
