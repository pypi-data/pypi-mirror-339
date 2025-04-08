#!/usr/bin/env python
"""
OpenRouter Integration Example

This example demonstrates how to use OpenRouter models with GameByte Agent.
It shows different ways to specify models and configure the agent.
"""

import asyncio
from gamebyte_agent.core.fastagent import FastAgent

# Create the application
fast = FastAgent("OpenRouter Integration Example")


@fast.agent(
    name="llama_scout",
    instruction="""You are a helpful AI assistant powered by Meta's Llama 4 Scout model.
    When asked about your capabilities, mention that you're running on Meta's Llama 4 Scout model via OpenRouter.
    Be concise and helpful in your responses.""",
    model="llama-scout"  # Using the alias for openrouter:meta-llama/llama-4-scout:free
)
@fast.agent(
    name="llama_maverick",
    instruction="""You are a helpful AI assistant powered by Meta's Llama 4 Maverick model.
    When asked about your capabilities, mention that you're running on Meta's Llama 4 Maverick model via OpenRouter.
    Be detailed and thorough in your responses.""",
    model="llama-maverick"  # Using the alias for openrouter:meta-llama/llama-4-maverick:free
)
@fast.agent(
    name="reka_flash",
    instruction="""You are a helpful AI assistant powered by Reka's Flash model.
    When asked about your capabilities, mention that you're running on Reka Flash 3 model via OpenRouter.
    Be creative and insightful in your responses.""",
    model="reka-flash"  # Using the alias for openrouter:rekaai/reka-flash-3:free
)
@fast.agent(
    name="direct_openrouter",
    instruction="""You are a helpful AI assistant.
    When asked about your capabilities, mention that you're running on a model via OpenRouter's direct specification.
    Be helpful and informative in your responses.""",
    model="openrouter:meta-llama/llama-4-scout:free"  # Direct specification without alias
)
@fast.chain(
    name="model_comparison",
    sequence=["llama_scout", "llama_maverick", "reka_flash"],
)
async def main():
    """Main function to demonstrate OpenRouter integration."""
    async with fast.run() as agent:
        print("\n=== Using Llama 4 Scout model ===")
        response = await agent.llama_scout("What are your capabilities as an AI assistant?")
        print(f"Response: {response}")
        
        print("\n=== Using Llama 4 Maverick model ===")
        response = await agent.llama_maverick("What are your capabilities as an AI assistant?")
        print(f"Response: {response}")
        
        print("\n=== Using Reka Flash model ===")
        response = await agent.reka_flash("What are your capabilities as an AI assistant?")
        print(f"Response: {response}")
        
        print("\n=== Using direct OpenRouter specification ===")
        response = await agent.direct_openrouter("What are your capabilities as an AI assistant?")
        print(f"Response: {response}")
        
        print("\n=== Using model comparison chain ===")
        print("This will run the same prompt through multiple models for comparison")
        response = await agent.model_comparison("Explain the concept of recursion in programming.")
        print(f"Chain Response: {response}")
        
        # Uncomment to start an interactive session with a specific model
        # await agent.llama_maverick.interactive()


if __name__ == "__main__":
    asyncio.run(main())
