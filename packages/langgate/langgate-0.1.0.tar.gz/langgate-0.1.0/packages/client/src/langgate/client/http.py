"""HTTP client for LangGate API."""

from typing import Generic, get_args

import httpx
from pydantic import SecretStr

from langgate.client.protocol import BaseRegistryClient, LLMInfoT
from langgate.core.logging import get_logger
from langgate.core.models import LLMInfo

logger = get_logger(__name__)


class BaseHTTPRegistryClient(BaseRegistryClient[LLMInfoT], Generic[LLMInfoT]):
    """
    Base HTTP client for the Model Registry API.

    This class is designed to be subclassed with a specific LLMInfo type.

    Type Parameters:
        LLMInfoT: The LLMInfo-derived model class to use for responses
    """

    __orig_bases__: tuple
    model_info_cls: type[LLMInfoT]

    def __init__(
        self,
        base_url: str,
        api_key: SecretStr | None = None,
        model_info_cls: type[LLMInfoT] | None = None,
    ):
        """Initialize the client.
        Args:
            base_url: The base URL of the registry service
            api_key: Registry server API key for authentication
        """
        super().__init__()
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

        # Set model_info_cls if provided, otherwise it is inferred from the class
        if model_info_cls is not None:
            self.model_info_cls = model_info_cls

        logger.debug(
            "initialized_base_http_registry_client",
            base_url=self.base_url,
            api_key=self.api_key,
            model_info_cls=self.model_info_cls,
        )

    def __init_subclass__(cls, **kwargs):
        """Set up model class when this class is subclassed."""
        super().__init_subclass__(**kwargs)

        # Extract the model class from generic parameters
        if not hasattr(cls, "model_info_cls"):
            cls.model_info_cls = cls._get_model_info_class()

    @classmethod
    def _get_model_info_class(cls) -> type[LLMInfoT]:
        """Extract the model class from generic type parameters."""
        return get_args(cls.__orig_bases__[0])[0]

    async def _fetch_model_info(self, model_id: str) -> LLMInfoT:
        """Get information about a model from remote API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/models/{model_id}")
            response.raise_for_status()
            return self.model_info_cls.model_validate(response.json())

    async def _fetch_all_models(self) -> list[LLMInfoT]:
        """Fetch all models from the remote API."""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/models")
            response.raise_for_status()
            return [
                self.model_info_cls.model_validate(model) for model in response.json()
            ]


class HTTPRegistryClient(BaseHTTPRegistryClient[LLMInfo]):
    """HTTP client singleton for the Model Registry API using the default LLMInfo schema."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            logger.debug("creating_http_registry_client_singleton")
        return cls._instance

    def __init__(self, base_url: str, api_key: SecretStr | None = None):
        if not hasattr(self, "_initialized"):
            super().__init__(base_url, api_key)
            self._initialized = True
            logger.debug("initialized_http_registry_client_singleton")
