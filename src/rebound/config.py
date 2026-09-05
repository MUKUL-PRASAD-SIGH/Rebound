from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite:///./rebound.db"
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""
    # Rebound's app-level execution setting. ``mvp_mode`` always uses Razorpay
    # Test Mode credentials; production/live execution is deliberately unsupported.
    rebound_execution_mode: Literal["dry_run", "mvp_mode"] = "dry_run"
    rebound_enable_llm_proposer: bool = False
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    # Operator endpoints stay unavailable until a local access token is set.
    # Razorpay webhooks use their own signed-request verification.
    rebound_api_token: str = ""
    # Used only to pseudonymise inbound customer references before persistence.
    rebound_pii_hash_salt: str = ""
    api_url: str = "http://localhost:8000"
    app_url: str = "http://localhost:5173"
    policy_version: str = "mvp-v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()
