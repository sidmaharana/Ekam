from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # The default value points to the local sqlite DB, but can be overridden by the .env file
    DATABASE_URL: str = "sqlite:///./test.db"
    GOOGLE_API_KEY: str

    # This tells pydantic to load variables from a .env file
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

# Create a single, reusable instance of the settings
settings = Settings()
