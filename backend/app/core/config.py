from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str

    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    REDIS_URL: str

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET: str
    AWS_REGION: str

    STRIPE_SECRET_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()
