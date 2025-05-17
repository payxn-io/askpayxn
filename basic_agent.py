"""
Blockchain Transaction Resolution Service
----------------------------------------
This module provides tools for resolving blockchain transactions using the thirdweb SDK.
"""

import asyncio
import os
from pydantic_ai import Agent, RunContext
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.pydantic_ai import get_pydantic_ai_tools


def initialize_services():
    """Initialize thirdweb services and AI agent."""
    insight = Insight(secret_key=os.getenv("THIRDWEB_SECRET_KEY"), chain_id=1)
    nebula = Nebula(secret_key=os.getenv("THIRDWEB_SECRET_KEY"))
    blockchain_tools = get_pydantic_ai_tools(insight.get_tools() + nebula.get_tools())

    agent = Agent(
        "openai:gpt-4o-mini",
        tools=blockchain_tools,
        system_prompt=(
            "You are a helpful blockchain assistant. You can use the thirdweb tools "
            "to interact with the blockchain and provide insights about transactions."
        ),
    )
    return insight, nebula, agent


# Initialize services
insight, nebula, agent = initialize_services()


@agent.tool(name="analyze_transaction")
def analyze_tx(ctx: RunContext, tx_hash: str, chain_id: int) -> dict:
    """Analyze a transaction hash to get raw transaction data."""
    params = {"chain": [chain_id] if not isinstance(chain_id, list) else chain_id}
    return insight._get(f"resolve/{tx_hash}", params)


async def main():
    """Example of using thirdweb_ai with Pydantic AI."""
    queries = [
        "Can you analyze this transaction 0x4db65f81c76a596073d1eddefd592d0c3f2ef3d80f49dafee445d37e5444a3ad in Base?",
    ]

    for query in queries:
        print(f"\n\nQuery: {query}")
        print("-" * 50)
        result = await agent.run(query)
        print("\nResult:")
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())
