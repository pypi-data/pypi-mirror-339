"""Example demonstrating the use of the combined LangGateLocal."""

import asyncio
from pprint import pprint

from langgate.sdk import LangGateLocal


async def main():
    """Demonstrate usage of the combined LangGateLocal."""
    print("=== Combined Client Example ===")

    # Initialize the combined client
    client = LangGateLocal()

    # List available models
    models = await client.list_models()
    print(f"Available models: {len(models)}")
    for model in models:
        print(f"- {model.id}: {model.name}")

    # Sample user parameters
    input_params = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": True,
    }

    # Get model info and transform parameters in a single workflow
    if models:
        model_id = models[0].id

        # Get model info
        model_info = await client.get_model_info(model_id)
        print(f"\nModel: {model_info.name}")
        print(f"Provider: {model_info.provider.name}")

        # Transform parameters
        transformed = await client.get_params(model_id, input_params)
        print("\nTransformed parameters:")
        pprint(transformed)


if __name__ == "__main__":
    asyncio.run(main())
