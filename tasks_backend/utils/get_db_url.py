import json
import logging
import os

import boto3
from botocore.exceptions import ClientError

from tasks_backend.utils.utils import get_env_var


def _get_db_credentials() -> tuple[str, str]:
    secrets_client = boto3.client("secretsmanager")
    secret_id = get_env_var("DBSecretArn")

    try:
        logging.info("Getting DBSecret from Secrets Manager...")
        get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        logging.error(f"Error retrieving DBSecret: {e}")
    logging.info("Retrieved DB credentials from Secrets Manager")

    db_secret = json.loads(get_secret_value_response["SecretString"])
    return db_secret["username"], db_secret["password"]


def get_db_url() -> str:
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        username, password = _get_db_credentials()
        db_host = get_env_var("DBClusterEndpoint")
        db_name = get_env_var("DBName")
        db_url = f"postgresql://{username}:{password}@{db_host}/{db_name}"
    else:
        db_url = get_env_var("DB_URL")
    logging.info(f"DB URL: {db_url}")
    return db_url
