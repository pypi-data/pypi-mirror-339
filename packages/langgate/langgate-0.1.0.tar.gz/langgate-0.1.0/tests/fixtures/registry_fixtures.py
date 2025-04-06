"""Registry API fixtures."""

import json
import os
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from unittest import mock

import pytest
import pytest_asyncio
import yaml
from httpx import ASGITransport, AsyncClient

from langgate.core.models import LLMInfo
from langgate.registry.models import ModelRegistry
from langgate.server.core.config import settings
from langgate.server.main import app
from tests.factories.models import LLMInfoFactory


@pytest.fixture
def mock_models_json(tmp_path: Path) -> Generator[Path]:
    """Create a mock langgate_models.json file for testing."""
    models_data = {
        "openai/gpt-4o": {
            "name": "GPT-4o",
            "mode": "chat",
            "service_provider": "openai",
            "model_provider": "openai",
            "model_provider_name": "OpenAI",
            "capabilities": {
                "supports_tools": True,
                "supports_parallel_tool_calls": True,
                "supports_vision": True,
                "supports_prompt_caching": True,
                "supports_response_schema": True,
                "supports_system_messages": True,
                "supports_tool_choice": True,
            },
            "context": {"max_input_tokens": 128000, "max_output_tokens": 16384},
            "costs": {
                "input_cost_per_token": "0.0000025",
                "output_cost_per_token": "0.00001",
                "input_cost_per_token_batches": "0.00000125",
                "output_cost_per_token_batches": "0.000005",
                "cache_read_input_token_cost": "0.00000125",
                "input_cost_per_image": "0.003613",
            },
            "description": "OpenAI's GP model",
            "_last_updated": "2025-03-21T21:40:54.742453+00:00",
            "_data_source": "openrouter",
            "_last_updated_from_id": "openai/gpt-4o",
        },
        "anthropic/claude-3-7-sonnet-latest": {
            "name": "Claude-3.7 Sonnet",
            "mode": "chat",
            "service_provider": "anthropic",
            "model_provider": "anthropic",
            "model_provider_name": "Anthropic",
            "capabilities": {
                "supports_tools": True,
                "supports_vision": True,
                "supports_prompt_caching": True,
                "supports_response_schema": True,
                "supports_assistant_prefill": True,
                "supports_tool_choice": True,
            },
            "context": {"max_input_tokens": 200000, "max_output_tokens": 128000},
            "costs": {
                "input_cost_per_token": "0.000003",
                "output_cost_per_token": "0.000015",
                "cache_read_input_token_cost": "3E-7",
                "cache_creation_input_token_cost": "0.00000375",
                "input_cost_per_image": "0.0048",
            },
            "description": "Anthropic's Claude 3.7 Sonnet model",
            "openrouter_model_id": "anthropic/claude-3.7-sonnet",
            "_last_updated": "2025-03-21T21:40:54.743326+00:00",
            "_data_source": "openrouter",
            "_last_updated_from_id": "anthropic/claude-3.7-sonnet",
        },
    }
    models_json_path = tmp_path / "langgate_models.json"
    with open(models_json_path, "w") as f:
        json.dump(models_data, f)

    yield models_json_path


@pytest.fixture
def mock_config_yaml(tmp_path: Path) -> Generator[Path]:
    """Create a mock langgate_config.yaml file for testing."""
    config_data = {
        "app_config": {
            "PROJECT_NAME": "LangGate Test",
            "CORS_ORIGINS": ["http://localhost"],
            "HTTPS": False,
        },
        "default_params": {
            "temperature": 0.7,
        },
        "services": {
            "openai": {
                "api_key": "${OPENAI_API_KEY}",
                "base_url": "https://api.openai.com/v1",
                "default_params": {
                    "max_tokens": 1000,
                },
            },
            "anthropic": {
                "api_key": "${ANTHROPIC_API_KEY}",
                "base_url": "https://api.anthropic.com",
                "default_params": {
                    "max_tokens": 2000,
                },
                "model_patterns": {
                    "reasoning": {
                        "override_params": {
                            "max_tokens": 2048,
                            "thinking": {
                                "type": "enabled",
                            },
                        },
                        "remove_params": ["temperature"],
                    }
                },
            },
        },
        "models": [
            {
                "id": "gpt-4o",
                "name": "GPT-4o",
                "service": {
                    "provider": "openai",
                    "model_id": "gpt-4o",
                },
            },
            {
                "id": "anthropic/claude-3-7-sonnet",
                "name": "Claude-3.7 Sonnet",
                "service": {
                    "provider": "anthropic",
                    "model_id": "claude-3-7-sonnet-20250219",
                },
            },
            {
                "id": "anthropic/claude-3-7-sonnet-reasoning",
                "name": "Claude-3.7 Sonnet R",
                "description": "Claude 3.7 Sonnet with reasoning",
                "service": {
                    "provider": "anthropic",
                    "model_id": "claude-3-7-sonnet-20250219",
                },
                "override_params": {
                    "thinking": {
                        "budget_tokens": 1024,
                    }
                },
            },
        ],
    }
    config_yaml_path = tmp_path / "langgate_config.yaml"
    with open(config_yaml_path, "w") as f:
        yaml.dump(config_data, f)

    yield config_yaml_path


@pytest.fixture
def mock_env_file(tmp_path: Path) -> Generator[Path]:
    """Create a mock .env file for testing."""
    env_path = tmp_path / ".env"
    with open(env_path, "w") as f:
        f.write("OPENAI_API_KEY=sk-test-123\n")
        f.write("ANTHROPIC_API_KEY=sk-ant-test-123\n")
        f.write("SECRET_KEY=test-secret-key\n")

    yield env_path


@pytest.fixture
def mock_registry_files(
    mock_models_json: Path, mock_config_yaml: Path, mock_env_file: Path
) -> Generator[dict[str, Path]]:
    """Combine all mock registry files for testing."""
    result_dict = {
        "models_json": mock_models_json,
        "config_yaml": mock_config_yaml,
        "env_file": mock_env_file,
    }
    yield result_dict


@pytest.fixture
def mock_models_path_in_env(mock_models_json: Path) -> Generator[dict[str, str]]:
    """Mock only the langgate_models.json environment variable."""
    with mock.patch.dict(os.environ, {"LANGGATE_MODELS": str(mock_models_json)}):
        yield {"LANGGATE_MODELS": str(mock_models_json)}


@pytest.fixture
def mock_config_path_in_env(mock_config_yaml: Path) -> Generator[dict[str, str]]:
    """Mock only the langgate_config.yaml environment variable."""
    with mock.patch.dict(os.environ, {"LANGGATE_CONFIG": str(mock_config_yaml)}):
        yield {"LANGGATE_CONFIG": str(mock_config_yaml)}


@pytest.fixture
def mock_env_file_path_in_env(mock_env_file: Path) -> Generator[dict[str, str]]:
    """Mock only the .env file environment variable."""
    with mock.patch.dict(os.environ, {"LANGGATE_ENV_FILE": str(mock_env_file)}):
        yield {"LANGGATE_ENV_FILE": str(mock_env_file)}


@pytest.fixture
def mock_env_vars_from_env_file(mock_env_file: Path) -> Generator[dict[str, str]]:
    """Mock environment variables loaded from the .env file."""
    env_vars = {}
    with open(mock_env_file) as f:
        for _line in f:
            line = _line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                env_vars[key] = value

    with mock.patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_all_env_vars(
    mock_models_json: Path,
    mock_config_yaml: Path,
    mock_env_file: Path,
    mock_env_vars_from_env_file: dict[str, str],
) -> Generator[dict[str, str]]:
    """Mock all registry-related environment variables."""
    env_vars = mock_env_vars_from_env_file.copy()
    env_vars.update(
        {
            "LANGGATE_MODELS": str(mock_models_json),
            "LANGGATE_CONFIG": str(mock_config_yaml),
            "LANGGATE_ENV_FILE": str(mock_env_file),
        }
    )

    with mock.patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def model_registry(mock_all_env_vars: dict[str, str]) -> Generator[ModelRegistry]:
    """Create a ModelRegistry instance with mock files."""
    ModelRegistry._instance = None

    # Create a fresh registry instance
    registry = ModelRegistry()
    yield registry
    ModelRegistry._instance = None


@pytest.fixture
def mock_llm_info() -> LLMInfo:
    """Create a mock LLMInfo instance."""
    return LLMInfoFactory.create()


@pytest_asyncio.fixture
async def registry_client() -> AsyncGenerator[AsyncClient]:
    """Return an async client for testing the registry API."""
    # Create ASGITransport for testing
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url=f"http://{settings.TEST_SERVER_HOST}{settings.API_V1_STR}",
    ) as client:
        yield client
