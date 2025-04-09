import os
from google.api_core import retry
from google.api_core.exceptions import NotFound
from google.auth import default
from google.cloud import secretmanager
from google.oauth2 import service_account
from typing import Optional
from maleo_core.utils.logger import Logger

class GoogleSecretManager:
    _logger:Optional[Logger] = None
    _project:Optional[str] = None
    _client:Optional[secretmanager.SecretManagerServiceClient] = None

    @classmethod
    def initialize(cls, logger:Logger, project_id:Optional[str] = None) -> None:
        """Initialize the cloud storage if not already initialized."""
        cls._logger = logger
        cls._project = project_id or os.getenv("GCP_PROJECT_ID")
        if cls._project is None:
            raise ValueError("GCP_PROJECT_ID environment variable must be set if no project_id is provided")
        if cls._client is None:
            #* Setup credentials with fallback chain
            credentials = None
            credentials_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            try:
                if credentials_file:
                    credentials = service_account.Credentials.from_service_account_file(credentials_file)
                else:
                    credentials, _ = default()
            except Exception as e:
                raise ValueError(f"Failed to initialize credentials: {str(e)}")

            cls._client = secretmanager.SecretManagerServiceClient(credentials=credentials)

        logger.info("Successfully initialized Google Secret Manager client")

    @classmethod
    def dispose(cls):
        """Disposes of the Google Secret Manager client"""
        if cls._client is not None:
            cls._client = None
        if cls._project is not None:
            cls._project = None
        if cls._logger is not None:
            cls._logger = None

    @classmethod
    @retry.Retry(
        predicate=retry.if_exception_type(Exception),
        timeout=5
    )
    def get(
        cls,
        name:str,
        version:str = "latest",
    ) -> Optional[str]:
        try:
            secret_path = f"projects/{cls._project}/secrets/{name}/versions/{version}"
            request = secretmanager.AccessSecretVersionRequest(name=secret_path)
            response = cls._client.access_secret_version(request=request)
            cls._logger.info("Successfully retrieved secret '%s' of version '%s'", name, version)
            return response.payload.data.decode()
        except Exception as e:
            cls._logger.error("Exception raised while accessing secret '%s'  of version '%s':\n%s", name, version, str(e), exc_info=True)
            return None

    @classmethod
    @retry.Retry(
        predicate=retry.if_exception_type(Exception),
        timeout=5
    )
    def create(
        cls,
        name:str,
        data:str
    ) -> Optional[str]:
        parent = f"projects/{cls._project}"
        secret_path = f"{parent}/secrets/{name}"
        try:
            #* Check if the secret already exists
            request = secretmanager.GetSecretRequest(name=secret_path)
            cls._client.get_secret(request=request)
            cls._logger.info("Secret '%s' exists. Adding new version.", name)

        except NotFound:
            #* Secret does not exist, create it first
            try:
                secret = secretmanager.Secret(name=name, replication={"automatic": {}})
                request = secretmanager.CreateSecretRequest(parent=parent, secret_id=name, secret=secret)
                cls._client.create_secret(request=request)
                cls._logger.info("Secret '%s' created successfully.", name)
            except Exception as e:
                cls._logger.error("Failed to create secret '%s': %s", name, str(e))
                return None

        #* Add a new secret version
        try:
            payload = secretmanager.SecretPayload(data=data.encode())  # ✅ Fixed attribute name
            request = secretmanager.AddSecretVersionRequest(parent=secret_path, payload=payload)
            response = cls._client.add_secret_version(request=request)

            cls._logger.info("New version added for secret '%s'.", name)
            return data
        
        except Exception as e:
            cls._logger.error("Failed to add new version for secret '%s': %s", name, str(e))
            return None