from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    STORY_GENERATOR_URL: str = "http://localhost:5002/api/generate"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MODEL_NAME: str = "llama3.2"
    
    class Config:
        env_file = ".env"

settings = Settings()

