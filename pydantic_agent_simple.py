"""
Blockchain Transaction Resolution Service (Simplified Structured Version)
------------------------------------------------------------------------
This module provides tools for resolving blockchain transactions using
the thirdweb SDK with a simplified Pydantic model structure.
"""

import asyncio
import os
from datetime import datetime
from typing import Dict, Any, Optional

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from thirdweb_ai import Insight, Nebula
from thirdweb_ai.adapters.pydantic_ai import get_pydantic_ai_tools


class TransactionData(BaseModel):
    """Simplified structured representation of blockchain transaction data."""

    # Basic transaction info
    transaction_hash: str = Field(description="The hash of the transaction")
    chain_id: int = Field(
        description="The ID of the blockchain where this transaction occurred"
    )
    block_number: Optional[int] = Field(
        None, description="The block number containing this transaction"
    )
    timestamp: Optional[int] = Field(
        None, description="The Unix timestamp when the transaction was processed"
    )

    # Transaction participants
    from_address: Optional[str] = Field(
        None, description="The address that sent the transaction"
    )
    to_address: Optional[str] = Field(
        None, description="The address that received the transaction"
    )

    # Transaction economics
    value: Optional[str] = Field(
        "0", description="The value transferred in the transaction (in wei)"
    )
    gas_used: Optional[int] = Field(
        None, description="The amount of gas used by the transaction"
    )
    gas_price: Optional[int] = Field(None, description="The gas price in wei")

    # Status
    status: Optional[int] = Field(
        None, description="Transaction status (1 = success, 0 = failure)"
    )

    # Raw data (for access to all fields)
    raw_data: Dict[str, Any] = Field(
        default_factory=dict, description="The complete raw transaction data"
    )

    def get_datetime(self) -> Optional[datetime]:
        """Convert the Unix timestamp to a human-readable datetime object."""
        if self.timestamp:
            return datetime.fromtimestamp(self.timestamp)
        return None


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


@agent.tool(name="resolve_transaction")
def resolve_tx(ctx: RunContext, tx_hash: str, chain_id: int) -> TransactionData:
    """Resolve a transaction hash to get structured transaction data."""
    # Prepare API parameters
    params = {"chain": [chain_id] if not isinstance(chain_id, list) else chain_id}

    # Fetch transaction data from API
    raw_result = insight._get(f"resolve/{tx_hash}", params)

    # Create a normalized transaction data object
    tx_data = {
        "transaction_hash": tx_hash,
        "chain_id": chain_id,
        "raw_data": raw_result,
    }

    # Extract commonly used fields if they exist
    if isinstance(raw_result, dict):
        # Map common field names (handling variations)
        if "blockNumber" in raw_result:
            tx_data["block_number"] = raw_result["blockNumber"]

        if "from" in raw_result:
            tx_data["from_address"] = raw_result["from"]

        if "to" in raw_result:
            tx_data["to_address"] = raw_result["to"]

        if "value" in raw_result:
            tx_data["value"] = raw_result["value"]

        if "gasUsed" in raw_result:
            tx_data["gas_used"] = raw_result["gasUsed"]

        if "gasPrice" in raw_result:
            tx_data["gas_price"] = raw_result["gasPrice"]

        if "timestamp" in raw_result:
            tx_data["timestamp"] = raw_result["timestamp"]

        if "status" in raw_result:
            tx_data["status"] = raw_result["status"]

    # Create and return the structured model
    return TransactionData(**tx_data)


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
