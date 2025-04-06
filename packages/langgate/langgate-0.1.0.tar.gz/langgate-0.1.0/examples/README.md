# LangGate SDK Examples

This directory contains examples demonstrating how to use the various components of the LangGate SDK.

## Examples

1. **registry_example.py**: Using the LocalRegistryClient to get model information
2. **transformer_example.py**: Using the LocalTransformerClient for parameter transformation
3. **combined_example.py**: Using the combined LangGateLocal for both functionality
4. **http_client_example.py**: Using the HTTPRegistryClient to connect to a remote LangGate service

## Running Examples

Make sure you have LangGate installed:

```bash
# Install the full SDK
pip install langgate[all]

# Or install just what you need
pip install langgate[registry]  # For registry examples
pip install langgate[transform]  # For transformer examples
pip install langgate[sdk]  # For combined client examples
pip install langgate[client]  # For HTTP client examples
```

Then run any example:

```bash
python examples/registry_example.py
```

## Configuration

The examples expect a valid `langgate_config.yaml` file in the current directory. A minimal example config would look like:

```yaml
# Global default parameters
default_params:
  temperature: 0.7

# Service provider configurations
services:
  anthropic:
    api_key: "${ANTHROPIC_API_KEY}"
    base_url: "https://api.anthropic.com"

# Model-specific configurations
models:
  - id: anthropic/claude-3-7-sonnet
    service:
      provider: anthropic
      model_id: claude-3-7-sonnet-20250219
```
