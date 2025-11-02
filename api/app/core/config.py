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
    EASY_DIFFICULTY_MAX: float = 45.0  # Permite raros pero evita míticos/legendarios
    MEDIUM_DIFFICULTY_MAX: float = 70.0  # Permite míticos
    HARD_DIFFICULTY_MAX: float = 100.0  # Permite todo
    
    # Lambda weights for solver (balancing stats vs difficulty)
    # Escala de rareza: Raro(15) → Mítico(30, 2x) → Legendario(50, 4x)
    EASY_LAMBDA: float = 3.0  # Alta penalización: prefiere Raros, evita Míticos/Legendarios
    MEDIUM_LAMBDA: float = 1.5  # Balance: acepta Míticos si valen la pena
    HARD_LAMBDA: float = 0.3  # Baja penalización: prioriza stats sobre rareza
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

