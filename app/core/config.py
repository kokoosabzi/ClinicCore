from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinicCore"
    database_url: str = "postgresql+psycopg://cliniccore:cliniccore@localhost:5432/cliniccore"
    secret_key: str = "change-me-in-production"
    admin_username: str = "admin"
    admin_password: str = "admin"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
