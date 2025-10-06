from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

class Settings(BaseSettings):
    env: str
    mongo_url: str
    mongo_db_name: str
    mongo_pool_max_size: int
    mongo_pool_min_size: int
    mongo_idle_time_ms: int

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env", env_file_encoding="UTF-8", populate_by_name=True)

@lru_cache()
def configs() -> Settings:
    """<p>Esta funcion permite crear un singleton de las configuraciones el cual puede ser utilizado desde cualquier parte de la aplicacion.</p>"""
    return Settings() # type: ignore
