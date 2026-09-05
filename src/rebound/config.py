from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite:///./rebound.db"
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""
    rebound_execution_mode: str = "dry_run"  # dry_run | test_mode
    rebound_enable_llm_proposer: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    api_url: str = "http://localhost:8000"
    app_url: str = "http://localhost:5173"
    policy_version: str = "mvp-v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
