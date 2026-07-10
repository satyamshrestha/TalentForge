from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    REDIS_URL: str
    TESTING: bool = False

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # File Uploads
    UPLOAD_DIR: str = "uploads/resumes"

    # Future AI Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_AI_API_KEY: str = ""

    LLM_PROVIDER: str = "openai"
    LLM_MODEL: str = "gpt-5"
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.2

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()