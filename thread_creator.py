from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.tools import RunContext
import asyncio


class TwitterThread(BaseModel):
    tweet1: str
    tweet2: str
    tweet3: str


ollama_model = OpenAIModel(
    model_name="llama3.1:8b",
    provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
)

agent = Agent(
    "openai:gpt-4o-mini",
    # ollama_model,
    system_prompt=("You are a helpful assistant that creates Twitter threads."),
)


async def generate_twitter_thread(data: str) -> TwitterThread:
    prompt = f"""
    Write a Twitter thread about '{data}' in exactly 3 tweets. The data is about a transaction on the blockchain you must ALWAYS follow the instructions provided bellow.

    Requirements:
    - No hashtags
    - Use bullet points (•) for better readability
    - Each bullet point should be on its own line
    - NO markdown formatting (no backticks, no asterisks for bold)
    - For technical data like addresses, use clear labels: "From:  `0x123...`" not "**From**: 0x123..."
    - Easy-to-read content with clear keywords and concise language
    - Natural flow between tweets, the transition between tweets should be seamless
    - Include a link to the block explorer with the transaction hash in the last tweet
    - Each Tweet should be about the same length and try to be as concise as possible
    - Twitter has character limits, so keep each tweet under 280 characters
    - Use proper spacing between sentences
    - Format numbers with commas for better readability (e.g., "1,234,567" not "1234567")
    - Use proper units (e.g., "ETH" for Ether values)
    - Keep technical details clear but concise

    Be sure to use the correct block explorer link for the chain, this is the list of the most common ones:
    - Ethereum: https://etherscan.io/tx/
    - Base: https://basescan.org/tx/
    - Polygon: https://polygonscan.com/tx/
    - Arbitrum: https://arbiscan.io/tx/
    - Optimism: https://optimistic.etherscan.io/tx/
    - Avalanche: https://snowtrace.io/tx/
    - Binance: https://bscscan.com/tx/
    - BSC: https://bscscan.com/tx/
    - Fantom: https://ftmscan.com/tx/
    - Gnosis: https://gnosisscan.io/tx/
    
    

    Format:
    Return the thread as plain text with each tweet on a new line, separated by line breaks:

    Tweet 1: [First tweet content]

    Tweet 2: [Second tweet content]

    Tweet 3: [Third tweet content with block explorer link]

    Example format:
    Tweet 1: There are the details of the transaction. Hash: 0x123...abc. Block: 7,985,824.

    Tweet 2: • From: 0xdf8...200
    • To: 0x023...5f0
    • Value: 0 ETH
    • Gas Used: 108,152
    • Gas Price: 18.19 Gwei

    Tweet 3: • Transaction Type: 2 (EIP-1559)
    • Status: Success
    • Block Hash: 0xa02...b8c
    • View on explorer: https://sepolia.etherscan.io/tx/0x123...abc
    """

    result = await agent.run(prompt)
    raw_text = result.data

    # Parse the three tweets from the raw text
    tweets = []
    current_tweet = []
    for line in raw_text.split("\n"):
        line = line.strip()
        if line.startswith("Tweet ") and ":" in line:
            # If we find a new tweet and already have content, add the previous tweet
            if current_tweet:
                tweets.append("\n".join(current_tweet))
                current_tweet = []

            # Extract just the content after "Tweet N: "
            current_tweet = [line.split(":", 1)[1].strip()]
        elif line and current_tweet:
            # Append additional lines to the current tweet
            current_tweet.append(line)

    # Add the last tweet if it exists
    if current_tweet:
        tweets.append("\n".join(current_tweet))

    # Clean up any remaining markdown artifacts
    cleaned_tweets = []
    for tweet in tweets:
        # Remove any backticks
        tweet = tweet.replace("`", "")
        # Remove any asterisks used for bold/italic
        tweet = tweet.replace("**", "").replace("*", "")
        # Ensure proper spacing after bullet points
        tweet = tweet.replace("•", " • ").replace("  •  ", " • ")
        # Fix any double spaces while preserving line breaks
        lines = tweet.split("\n")
        cleaned_lines = [" ".join(line.split()) for line in lines]
        cleaned_tweet = "\n".join(cleaned_lines)
        cleaned_tweets.append(cleaned_tweet)

    # Ensure we have exactly 3 tweets
    while len(cleaned_tweets) < 3:
        cleaned_tweets.append("")

    # Return as TwitterThread object
    return TwitterThread(
        tweet1=cleaned_tweets[0], tweet2=cleaned_tweets[1], tweet3=cleaned_tweets[2]
    )


async def main():
    data = """

    Here are the details of the transaction with hash `0x4db65f81c76a596073d1eddefd592d0c3f2ef3d80f49dafee445d37e5444a3ad` on the Base blockchain:

    - **Chain ID**: 8453
    - **Block Number**: 28,453,333
    - **Block Hash**: `0xc704ac399c4877dfa68362dc6a43f5f54460f22caa52589aade40ce97c1d0ee8`
    - **Block Timestamp**: April 15, 2023 (Unix Time: 1743696013)
    - **Nonce**: 76,543
    - **Transaction Index**: 235
    - **From Address**: `0x7b323b7f681d29d477fa33b68758880dd7cff62b`
    - **To Address**: `0xbf784c4a1867fa07bfc508631aa50d298d2fe12d`
    - **Value**: 0 (no cryptocurrency was transferred)
    - **Gas Used**: 131,092
    - **Cumulative Gas Used**: 75,788,381
    - **Gas Limit**: 133,300
    - **Gas Price**: 1,492,317 wei
    - **Effective Gas Price**: 1,492,317 wei
    - **Max Fee per Gas**: 1,787,824 wei
    - **Max Priority Fee per Gas**: 60 wei
    - **Status**: Success (1)
    
    ### Function Call
    - **Function Selector**: `0x84bb1e42`
    
    ### Access List
    - **Access List**: `[]` (no specific access was granted)

    ### Signature
    - **r**: `27617788292242542892152170095433375627332590156656369708067324830522136550774`
    - **s**: `1798737749988432757948751640890963851136467122978047170069194466133803161674`
    - **v**: `1`

    #### Additional Information
    - The transaction did not involve a transfer of tokens, as the value is 0, and it likely pertained to a contract interaction based on the function selector provided.
    """
    thread = await generate_twitter_thread(data)
    print(thread.tweet1)
    print(thread.tweet2)
    print(thread.tweet3)


if __name__ == "__main__":
    asyncio.run(main())
