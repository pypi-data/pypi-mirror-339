"""Local transformer client implementation."""

import importlib.resources
import os
from pathlib import Path
from typing import Any

import yaml
from pydantic.types import SecretStr

from langgate.core.logging import get_logger
from langgate.core.utils.config_utils import resolve_path
from langgate.transform.protocol import TransformerClientProtocol
from langgate.transform.transformer import ParamTransformer

logger = get_logger(__name__)


class LocalTransformerClient(TransformerClientProtocol):
    """
    Local transformer client for parameter transformations.

    This client handles parameter transformations based on local configuration.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Create or return the singleton instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self, config_path: Path | None = None, env_file_path: Path | None = None
    ):
        """Initialize the client.

        Args:
            config_path: Path to the configuration file
            env_file_path: Path to the environment file
        """
        if not hasattr(self, "_initialized"):
            # Set up default paths
            cwd = Path.cwd()

            core_resources = importlib.resources.files("langgate.core")
            default_config_path = Path(
                str(core_resources.joinpath("data", "default_config.yaml"))
            )
            cwd_config_path = cwd / "langgate_config.yaml"
            cwd_env_path = cwd / ".env"

            self.config_path = resolve_path(
                "LANGGATE_CONFIG",
                config_path,
                cwd_config_path if cwd_config_path.exists() else default_config_path,
                "config_path",
                logger,
            )
            self.env_file_path = resolve_path(
                "LANGGATE_ENV_FILE",
                env_file_path,
                cwd_env_path,
                "env_file_path",
                logger,
            )

            # Cache for configs
            self._global_config: dict[str, Any] = {}
            self._service_config: dict[str, dict[str, Any]] = {}
            self._model_mappings: dict[str, dict[str, Any]] = {}

            # Load configuration
            self._load_config()
            self._initialized = True
            logger.debug("initialized_local_transformer_client")

    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            with open(self.config_path) as f:
                config: dict[str, Any] = yaml.safe_load(f)
            logger.info(
                "loaded_config",
                config_path=str(self.config_path),
            )

            # Extract global defaults
            self._global_config = {
                "default_params": config.get("default_params", {}),
            }

            # Extract service provider config
            self._service_config = config.get("services", {})

            # Process model mappings
            self._process_model_mappings(config.get("models", []))

        except FileNotFoundError:
            logger.warning(
                "config_file_not_found",
                config_path=str(self.config_path),
            )
            self._global_config = {"default_params": {}}
            self._service_config = {}
            self._model_mappings = {}

    def _process_model_mappings(self, models_config: list[dict[str, Any]]) -> None:
        """Process model mappings from configuration.

        Args:
            models_config: List of model configurations from the YAML file
        """
        self._model_mappings = {}

        for model_config in models_config:
            model_id: str = model_config["id"]
            service: dict[str, Any] = model_config["service"]
            service_provider: str = service["provider"]
            service_model_id: str = service["model_id"]

            # Store mapping info
            self._model_mappings[model_id] = {
                "service_provider": service_provider,
                "service_model_id": service_model_id,
                "override_params": model_config.get("override_params", {}),
                "remove_params": model_config.get("remove_params", []),
                "rename_params": model_config.get("rename_params", {}),
            }

    async def get_params(
        self, model_id: str, input_params: dict[str, Any]
    ) -> dict[str, Any]:
        """Get transformed parameters for the specified model.

        Args:
            model_id: The ID of the model to get transformed parameters for
            input_params: The parameters to transform

        Returns:
            The transformed parameters

        Raises:
            ValueError: If the model is not found
        """
        if model_id not in self._model_mappings:
            raise ValueError(f"Model {model_id} not found")

        # Get model mapping
        mapping = self._model_mappings[model_id]
        service_provider = mapping["service_provider"]
        service_model_id = mapping["service_model_id"]

        # Create param transformer
        transformer = ParamTransformer()

        # Apply transformations in sequence:

        # Start with user params (done in transform method)
        # Apply global defaults
        transformer.with_defaults(self._global_config.get("default_params", {}))

        # Apply service provider defaults if available
        if service_provider in self._service_config:
            service_config = self._service_config[service_provider]
            transformer.with_defaults(service_config.get("default_params", {}))

            # Apply API key and base URL from service config
            api_key: str
            if "api_key" in service_config:
                api_key = service_config["api_key"]
                if api_key.startswith("${") and api_key.endswith("}"):
                    env_var = api_key[2:-1]
                    if env_var in os.environ:
                        transformer.with_overrides(
                            {"api_key": SecretStr(os.environ[env_var])}
                        )

            if "base_url" in service_config:
                transformer.with_overrides({"base_url": service_config["base_url"]})

            # Apply model pattern overrides if applicable
            pattern: str
            pattern_config: dict[str, Any]
            if "model_patterns" in service_config:
                for pattern, pattern_config in service_config["model_patterns"].items():
                    if pattern in model_id:
                        if "default_params" in pattern_config:
                            transformer.with_defaults(pattern_config["default_params"])
                        if "override_params" in pattern_config:
                            transformer.with_overrides(
                                pattern_config["override_params"]
                            )
                        if "remove_params" in pattern_config:
                            transformer.removing(pattern_config["remove_params"])
                        if "rename_params" in pattern_config:
                            transformer.renaming(pattern_config["rename_params"])

        # Apply model-specific overrides
        transformer.with_overrides(mapping.get("override_params", {}))

        # Remove any specified params
        transformer.removing(mapping.get("remove_params", []))

        # Rename any specified params
        transformer.renaming(mapping.get("rename_params", {}))

        # Set the service model ID
        transformer.with_model_id(service_model_id)

        # Substitute any environment variables
        transformer.with_env_vars()

        # Apply all transformations
        return transformer.transform(input_params)
