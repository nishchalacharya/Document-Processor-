from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    embedding_model: str = "all-MiniLM-L6-v2"  # Default value
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# Create the settings instance
settings = Settings()