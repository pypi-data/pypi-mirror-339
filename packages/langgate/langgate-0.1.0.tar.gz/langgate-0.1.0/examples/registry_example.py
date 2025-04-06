"""Example demonstrating the use of the LocalRegistryClient."""

import asyncio
from pprint import pprint

from langgate.registry import LocalRegistryClient


async def main():
    """Demonstrate usage of the LocalRegistryClient."""
    print("=== Registry Example ===")

    # Initialize the registry client
    client = LocalRegistryClient()

    # List available models
    models = await client.list_models()
    print(f"Available models: {len(models)}")
    for model in models:
        print(f"- {model.id}: {model.name}")

    # Get detailed information about a specific model
    if models:
        model_info = await client.get_model_info(models[0].id)
        print("\nDetailed model information:")
        pprint(model_info.model_dump())


if __name__ == "__main__":
    asyncio.run(main())
