import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://daily_wisdom_user:daily_wisdom_user@localhost:5432/daily_wisdom")
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "info")
    
    @property
    def effective_database_url(self) -> str:
        """Use daily_wisdom schema for all queries"""
        if "daily_wisdom" in self.database_url:
            return self.database_url
        return f"{self.database_url}?options=-csearch_path%3Ddaily_wisdom"

settings = Settings()
