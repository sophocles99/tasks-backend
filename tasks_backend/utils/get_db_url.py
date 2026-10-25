import json
import logging
import os

from tasks_backend.utils.utils import get_env_var

logger = logging.getLogger(__name__)


def _get_db_credentials() -> tuple[str, str]:
    import boto3

    secrets_client = boto3.client("secretsmanager")
    secret_id = get_env_var("DBSecretArn")

    logger.info("Getting DBSecret from Secrets Manager...")
    get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_id)

    db_secret = json.loads(get_secret_value_response["SecretString"])
    logger.info("Retrieved DB credentials from Secrets Manager")

    return db_secret["username"], db_secret["password"]


def get_db_url() -> str:
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        username, password = _get_db_credentials()
        db_host = get_env_var("DBClusterEndpoint")
        db_name = get_env_var("DBName")
        db_url = f"postgresql+psycopg://{username}:{password}@{db_host}/{db_name}"
        logger.info(f"Database URL configured via AWS Secrets Manager (Host: {db_host}, DB: {db_name}).")
    else:
        db_url = get_env_var("DB_URL")
        logger.info("Database URL configured via environment variable.")
    return db_url
