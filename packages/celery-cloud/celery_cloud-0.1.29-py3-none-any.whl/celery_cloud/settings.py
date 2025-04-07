import json
import os
from typing import Any

from dotenv import load_dotenv

# Load variables from dotenv file
load_dotenv()


class Settings:
    """Settings class"""

    def __init__(self):
        """Init configuration forn environmnent variables"""

        self.CELERY_BACKEND_TABLE: str = self.get_env_variable(
            "CELERY_BACKEND_TABLE", "celery"
        )
        self.CELERY_BACKEND_REGION: str = self.get_env_variable(
            "CELERY_BACKEND_REGION", "eu-west-1"
        )

        self.LOG_LEVEL: str = self.get_env_variable("LOG_LEVEL", "INFO")
        self.LOG_FORMAT: str = self.get_env_variable(
            "LOG_FORMAT",
            (
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
                "| <level>{level: <8}</level> | trace_id={extra[trace_id]} "
                "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:"
                "<cyan>{line}</cyan> - <level>{message}</level>"
            ),
        )

        self.LOG_ENQUEUE: bool = self.get_env_variable("LOG_ENQUEUE", False)

        # Circuit breaker and retries config
        self.CB_FAIL_MAX: int = self.get_env_variable("CB_FAIL_MAX", 5)
        self.CB_RESET_TIMEOUT: int = self.get_env_variable("CB_RESET_TIMEOUT", 60)
        self.MAX_ATTEMPTS: int = self.get_env_variable("MAX_ATTEMPTS", 5)
        self.MAX_RETRIES: int = self.get_env_variable("MAX_RETRIES", 5)

        self.SERVER_DEBUG_PORT: int = self.get_env_variable("SERVER_DEBUG_PORT", 5890)
        self.DEBUG_MODE: bool = self.get_env_variable("DEBUG_MODE", False)

        self.TASKS: dict[str, str] = json.loads(self.get_env_variable("TASKS", "{}"))

    @staticmethod
    def get_env_variable(var_name: str, default: Any = None) -> Any:
        """Get environment variable or default value

        Args:
            var_name (str): _description_
            default (str, optional): _description_. Defaults to None.

        Raises:
            EnvironmentError: _description_

        Returns:
            str: _description_
        """

        value: Any = os.getenv(var_name, default)
        if value is None:
            raise OSError(
                f"Environment variable '{var_name}' "
                f"is not defined and does not have default value."
            )
        return value


settings = Settings()
