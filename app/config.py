from functools import lru_cache

from pydantic import computed_field
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings.

    Loads configuration from environment variables and the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
  

    app_name: str = "AI Trip Planner"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True

    
    # Database


    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "tripplanner"
    postgres_user: str = "postgres"
    postgres_password: str = "password"

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}"
            f"/{self.postgres_db}"
        )

    # Redis


    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @computed_field
    @property
    def redis_url(self) -> str:
        return (
            f"redis://"
            f"{self.redis_host}:{self.redis_port}"
            f"/{self.redis_db}"
        )

   
    # AI Gateway


    ai_provider: str = Field(
        default="ollama",
    )

    enable_fallback: bool = True

    request_timeout: int = 60

   
    # Ollama


    ollama_base_url: str = "http://localhost:11434"

    ollama_model: str = "llama3.2:latest"

 
    # OpenAI


    openai_api_key: str = ""

    openai_model: str = "gpt-4.1-mini"

    # Anthropic


    anthropic_api_key: str = ""

    anthropic_model: str = "claude-3-5-sonnet"

  
    # DeepSeek
  

    deepseek_api_key: str = ""

    deepseek_model: str = "deepseek-chat"

  
    # Twilio


    twilio_account_sid: str = ""

    twilio_auth_token: str = ""

    twilio_phone_number: str = ""

    enable_sms: bool = False

  
    # Prompt Engineering


    prompt_directory: str = "app/prompts/templates"

    active_prompt_version: str = "v1"

    enable_prompt_ab_testing: bool = True

    # Monitoring


    enable_metrics: bool = True

    metrics_path: str = "/metrics"

    log_level: str = "INFO"

   
    # Rate Limiting
    

    sms_rate_limit_per_minute: int = 10

    ai_rate_limit_per_minute: int = 50

    # Security
   

    secret_key: str = ""

    jwt_algorithm: str = "HS256"

    access_token_expire_minutes: int = 60

   
    # AI Evaluation
    

    enable_prompt_evaluation: bool = True

    evaluation_sample_size: int = 100


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    """

    return Settings()


settings = get_settings()