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
    # EASY: Solo hasta Míticos, pero sin items muy difíciles
    # MEDIUM: Requiere 1 Épico/Reliquia + permite Legendarios
    # HARD: Todo permitido
    EASY_DIFFICULTY_MAX: float = 48.0  # Raros (35) + algunos Míticos (no todos)
    MEDIUM_DIFFICULTY_MAX: float = 85.0  # Permite Legendarios (75) + 1 Épico/Reliquia
    HARD_DIFFICULTY_MAX: float = 100.0  # Sin límite
    
    # Lambda weights for solver (balancing stats vs difficulty)
    # Escala: Raro(15) → Mítico(30, 2x) → Legendario(50, 4x) → Épico/Reliquia(65+)
    EASY_LAMBDA: float = 2.0  # Penaliza Míticos, prefiere Raros cuando sea posible
    MEDIUM_LAMBDA: float = 0.3  # ✅ FIXED - Acepta Épicos/Reliquias si aportan valor (antes 0.8)
    HARD_LAMBDA: float = 0.0  # ✅ FIXED - Sin penalización: puro stats (antes 0.1)
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

