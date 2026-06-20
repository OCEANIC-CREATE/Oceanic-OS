"""Configuration and settings management for Oceanic-OS."""

import os
from typing import Optional


class Settings:
    """Application settings from environment variables."""

    def __init__(self):
        # Application
        self.app_name = os.getenv("APP_NAME", "Oceanic-OS")
        self.app_env = os.getenv("APP_ENV", "development")
        self.app_debug = os.getenv("APP_DEBUG", "true").lower() == "true"

        # API
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_workers = int(os.getenv("API_WORKERS", "1"))

        # CORS
        self.cors_origins = os.getenv("CORS_ORIGINS", "*")
        self.cors_allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"

        # Limits
        self.max_identities = int(os.getenv("MAX_IDENTITIES", "10000"))
        self.max_events = int(os.getenv("MAX_EVENTS", "100000"))
        self.pagination_limit = int(os.getenv("PAGINATION_LIMIT", "100"))

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
