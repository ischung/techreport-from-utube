from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    llm_provider: str = Field(
        default="claude", description="LLM provider key: claude | openai | ollama"
    )
    anthropic_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")
    ollama_base_url: str = Field(default="http://localhost:11434")
    youtube_api_key: str = Field(default="")
    reports_dir: str = Field(default="./reports")


def get_settings() -> Settings:
    return Settings()
