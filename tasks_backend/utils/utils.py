import os
from datetime import UTC, datetime


def get_current_utc_time():
    return datetime.now(UTC)


def get_env_var(env_var_name: str) -> str:
    env_var_value = os.getenv(env_var_name, None)
    if not env_var_value:
        raise ValueError(f"Environment variable {env_var_name} is not set.")
    return env_var_value
