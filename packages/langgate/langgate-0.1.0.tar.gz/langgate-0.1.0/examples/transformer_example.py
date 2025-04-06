"""Example demonstrating the use of the LocalTransformerClient."""

import asyncio
from pprint import pprint

from langgate.transform import LocalTransformerClient


async def main():
    """Demonstrate usage of the LocalTransformerClient."""
    print("=== Parameter Transformation Example ===")

    # Initialize the transformer client
    transformer = LocalTransformerClient()

    # Sample user parameters
    input_params = {
        "temperature": 0.7,
        "max_tokens": 1000,
        "stream": True,
    }

    # Transform parameters for a specific model
    try:
        model_id = "anthropic/claude-3-opus"
        transformed = await transformer.get_params(model_id, input_params)

        print(f"Original parameters for {model_id}:")
        pprint(input_params)

        print("\nTransformed parameters:")
        pprint(transformed)
    except ValueError as e:
        print(f"Error: {str(e)}")
        print(
            "Note: You need to have a valid langgate_config.yaml file with the model configuration."
        )


if __name__ == "__main__":
    asyncio.run(main())
