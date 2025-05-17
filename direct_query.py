#!/usr/bin/env python3
"""
Direct Query to Twitter Thread
-----------------------------
This script allows users to directly query the blockchain agent with natural language
and post the results as a Twitter thread, without waiting for mentions.
"""

import asyncio
import sys

import basic_agent
import thread_creator
from thread_creator import TwitterThread, generate_twitter_thread
from twitter_bot import client
from pydantic_ai.tools import RunContext


def post_thread(thread, reply_to_id=None):
    """
    Post a thread of tweets, either as standalone or as a reply.

    Args:
        thread: The TwitterThread object containing the tweets
        reply_to_id: Optional ID of tweet to reply to, or None for standalone thread
    """
    print("\nPosting thread to Twitter...")

    # Post the first tweet (either standalone or as a reply)
    response1 = client.create_tweet(
        text=thread.tweet1, in_reply_to_tweet_id=reply_to_id
    )
    print(f"Posted first tweet: {thread.tweet1}")

    # Post the second tweet as a reply to the first
    response2 = client.create_tweet(
        text=thread.tweet2, in_reply_to_tweet_id=response1.data["id"]
    )
    print(f"Posted second tweet: {thread.tweet2}")

    # Post the third tweet as a reply to the second
    response3 = client.create_tweet(
        text=thread.tweet3, in_reply_to_tweet_id=response2.data["id"]
    )
    print(f"Posted third tweet: {thread.tweet3}")

    return response1.data["id"]


async def query_agent(query: str) -> str:
    """
    Send a query to the blockchain agent and get the response.

    Args:
        query: The question to ask the agent

    Returns:
        The formatted response from the agent
    """
    print(f"Querying agent: {query}")

    try:
        # Get the agent result
        result = await basic_agent.agent.run(query)
        agent_result = result.data

        print("Agent response received")
        return agent_result
    except RuntimeError as e:
        if "This event loop is already running" in str(e):
            # We're being called from a context where there's already an event loop
            # Use run_sync instead which is designed for this case
            print("Using synchronous agent call instead...")
            result = basic_agent.agent.run_sync(query)
            return result.data
        else:
            # Re-raise if it's a different RuntimeError
            raise


async def safe_generate_thread(agent_result: str) -> TwitterThread:
    """
    Generate a Twitter thread using the thread generator.

    Args:
        agent_result: The raw text from the agent response

    Returns:
        A TwitterThread object
    """
    # No need for RunContext as the generate_twitter_thread function
    # only takes the data parameter
    return await generate_twitter_thread(agent_result)


async def main():
    try:
        # Simple banner
        print("\n=== Blockchain Twitter Bot - Direct Query ===\n")

        # Just ask for the prompt directly
        print("Enter your blockchain question:")
        query = input("> ").strip()

        # Make sure we got the full input
        print(f'\nYou asked: "{query}"')
        confirm = input("Is this correct? (y/n): ").lower().strip()

        if not confirm.startswith("y"):
            print("Let's try again with your complete question.")
            print("Enter your complete blockchain question:")
            query = input("> ").strip()
            print(f'\nYou asked: "{query}"')

        # Ask if they want to reply to a tweet (optional)
        reply_choice = (
            input("\nDo you want to reply to an existing tweet? (y/n): ")
            .lower()
            .strip()
        )
        reply_to = None
        if reply_choice.startswith("y"):
            reply_to = input("Enter the tweet ID to reply to: ").strip()

        # Ask if they want to post to Twitter
        post_choice = (
            input("\nDo you want to post this to Twitter? (y/n): ").lower().strip()
        )
        dry_run = not post_choice.startswith("y")

        # Query the agent with the natural language prompt
        print("\nSending your question to the blockchain agent...")
        try:
            agent_result = await query_agent(query)

            if not agent_result:
                print(
                    "\n⚠️ Warning: Agent returned an empty response. Please try a different query."
                )
                return

        except Exception as e:
            print(f"\n❌ Error querying agent: {e}")
            print("Please check your question and try again.")
            return

        # Generate the Twitter thread
        print("\nGenerating Twitter thread...")
        try:
            thread = await safe_generate_thread(agent_result)
        except Exception as e:
            print(f"\n❌ Error generating thread: {e}")
            print("Agent response received but could not generate a thread.")
            print("Raw agent response:")
            print("-" * 50)
            print(agent_result)
            print("-" * 50)
            return

        # Print the generated thread
        print("\nGenerated Twitter Thread:")
        print("-" * 50)
        print(f"{thread.tweet1}")
        print(f"\n{thread.tweet2}")
        print(f"\n{thread.tweet3}")
        print("-" * 50)

        # Post the thread if not a dry run
        if not dry_run:
            try:
                thread_id = post_thread(thread, reply_to)
                print(f"\n✅ Thread posted successfully! First tweet ID: {thread_id}")
            except Exception as e:
                print(f"\n❌ Error posting to Twitter: {e}")
                print("Thread was generated but could not be posted.")
        else:
            print("\nDry run - thread not posted to Twitter")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
