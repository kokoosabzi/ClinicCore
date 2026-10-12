from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ClinicCore"
    # SQLite is the supported local database for this phase.
    database_url: str = "sqlite:///./data/cliniccore.db"
    secret_key: str = "change-me-in-production"
    admin_username: str = "admin"
    admin_password: str = "admin"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    def model_post_init(self, __context) -> None:
        if not self.database_url.startswith("sqlite:"):
            raise ValueError("ClinicCore currently supports SQLite only; set DATABASE_URL to a sqlite:/// URL.")


settings = Settings()
