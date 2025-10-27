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
    service_role: str = ""
    bucket_name: str = "resumes"

    # OAuth settings
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    # Frontend URL
    frontend_url: str = ""

    # Resend Email settings
    resend_api_key: str = ""
    email_from: str = "Resumade <noreply@resumade.com>"

    # gemini ai settings
    gemini_api_key: str = ""

    # Redis settings
    upstash_redis_url: str = ""
    upstash_redis_token: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
