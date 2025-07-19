import json
import logging
import os
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from tasks_backend.utils.utils import get_env_var


@lru_cache()
def get_jwt_secret_key():
    if "AWS_LAMBDA_FUNCTION_NAME" in os.environ:
        secrets_client = boto3.client("secretsmanager")
        secret_id = get_env_var("JWTSecretKeySecretArn")

        try:
            get_secret_value_response = secrets_client.get_secret_value(SecretId=secret_id)
        except ClientError as e:
            logging.error(f"Error retrieving JWTSecretKeySecret: {e}")
        logging.info("Retrieved JWT secret key from Secrets Manager")

        jwt_secret = json.loads(get_secret_value_response["SecretString"])
        jwt_secret_key = jwt_secret["jwt-secret-key"]

    else:
        jwt_secret_key = get_env_var("JWT_SECRET_KEY")

    return jwt_secret_key
