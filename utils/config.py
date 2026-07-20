from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Core
    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    REDIS_URL: str
    TESTING: bool = False
    ALLOWED_HOSTS: list[str] = [
        "localhost",
        "127.0.0.1",
        "*.localhost",
        "testserver",
    ]

    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""

    # File Uploads
    UPLOAD_DIR: str = "uploads/resumes"
    MAX_RESUME_SIZE: int = 5 * 1024 * 1024

    # Future AI Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_AI_API_KEY: str = ""

    # AI Configuration
    LLM_PROVIDER: str = "ollama"
    LLM_MODEL: str = "llama3.2:3b"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_TIMEOUT: int = 300
    OLLAMA_RETRIES: int = 2
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.2

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()