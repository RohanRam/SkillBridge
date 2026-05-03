from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    MONITORING_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

import sys
try:
    settings = Settings()
except Exception as e:
    print("\n" + "="*50)
    print("🚨 ENVIRONMENT VARIABLES MISSING OR INCORRECT 🚨")
    print("="*50)
    print("Please add the following variables in the Render Dashboard:")
    print("- DATABASE_URL")
    print("- JWT_SECRET")
    print("- MONITORING_API_KEY")
    print("\nError Details:")
    print(str(e))
    print("="*50 + "\n")
    sys.exit(1)
