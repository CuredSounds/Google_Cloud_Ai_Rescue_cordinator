from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_ID: str = "your-project-id"
    REGION: str = "us-central1"
    SPANNER_INSTANCE: str = "survivor-network"
    SPANNER_DATABASE: str = "survivor-graph"

    class Config:
        env_file = ".env"

settings = Settings()
