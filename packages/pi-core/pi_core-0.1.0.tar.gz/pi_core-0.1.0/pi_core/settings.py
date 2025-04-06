from pydantic import BaseSettings

class CoreSettings(BaseSettings):
    project_name: str = "PI Core"
    environment: str = "development"
    debug: bool = False

    class Config:
        env_file = ".env"
