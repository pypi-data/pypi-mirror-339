"""Example demonstrating the use of the HTTPRegistryClient."""

import asyncio
from pprint import pprint

from langgate.client import HTTPRegistryClient


async def main():
    """Demonstrate usage of the HTTPRegistryClient."""
    print("=== HTTP Client Example ===")

    # Initialize the HTTP client
    # Note: This requires a running LangGate service
    client = HTTPRegistryClient("http://localhost:8000/api/v1")

    try:
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

    except Exception as e:
        print(f"Error connecting to the LangGate service: {str(e)}")
        print("Note: This example requires a running LangGate service.")


if __name__ == "__main__":
    asyncio.run(main())
