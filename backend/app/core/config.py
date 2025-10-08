from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    
    # JWT settings
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Supabase settings
    supabase_url: str = ""
    service_role: str = ""  # Changed from supabase_service_role_key
    bucket_name: str = "invoices"  # Changed from supabase_bucket_name
    
    class Config:
        env_file = ".env"

settings = Settings()
