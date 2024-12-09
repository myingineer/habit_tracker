from pydantic_settings import BaseSettings

# environment variables
class Settings(BaseSettings):
    DB_URL: str
    DB_PORT: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_ADDRESS: str
    EMAIL_APP_PASSWORD: str

    class ConfigDict:
        env_file = ".env"


settings = Settings()