from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    BACKEND_PORT_1: int
    BACKEND_PORT_2: int

    @property
    def REDIS_URL(self):  # noqa
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @property
    def DB_URL(self):  # noqa
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@db:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
