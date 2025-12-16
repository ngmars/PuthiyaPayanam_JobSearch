from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_MINUTES: int

    # AWS access for S3 bucket
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    AWS_S3_MAIN_CV_BUCKET_NAME: str

    class Config:
        env_file = ".env"

settings = Settings()
