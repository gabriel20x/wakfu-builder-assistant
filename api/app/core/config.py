from pydantic_settings import BaseSettings
from typing import List, Union
from pydantic import field_validator

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://wakfu:wakfu123@db:5432/wakfu_builder"
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:3000,http://localhost:5173"
    GAMEDATA_PATH: str = "/wakfu_data/gamedata_1.90.1.43"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
    
    # Solver parameters
    MAX_EPIC_ITEMS: int = 1
    MAX_RELIC_ITEMS: int = 1
    
    # Difficulty thresholds for build types
    EASY_DIFFICULTY_MAX: float = 40.0
    MEDIUM_DIFFICULTY_MAX: float = 70.0
    HARD_DIFFICULTY_MAX: float = 100.0
    
    # Lambda weights for solver (balancing stats vs difficulty)
    EASY_LAMBDA: float = 2.0  # High penalty for difficulty
    MEDIUM_LAMBDA: float = 1.0  # Balanced
    HARD_LAMBDA: float = 0.1  # Low penalty for difficulty
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

