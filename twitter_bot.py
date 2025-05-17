import tweepy
from dotenv import load_dotenv
import os
import time
import asyncio

from basic_agent import agent as blockchain_agent
from thread_creator import generate_twitter_thread, TwitterThread

load_dotenv()

# Keys and tokens
API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


# Authenticate to Twitter using v2 API
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    bearer_token=BEARER_TOKEN,
)


# Function to post a tweet
def post_tweet(tweet_text):
    return client.create_tweet(text=tweet_text)


# Function to post a reply to a tweet
def post_reply(tweet_text, tweet_id):
    return client.create_tweet(text=tweet_text, in_reply_to_tweet_id=tweet_id)


# Function to get recent mentions
def get_recent_mentions():
    # Get authenticated user ID
    me = client.get_me()
    user_id = me.data.id

    # Get recent mentions (minimum 5 required by Twitter API)
    mentions = client.get_users_mentions(
        id=user_id,
        max_results=5,  # API requires minimum of 5
        expansions=["referenced_tweets.id"],
        tweet_fields=["created_at", "text"],
    )

    return mentions.data if mentions.data else []


async def process_mention(mention):
    print(f"Processing mention: {mention.text}")

    try:
        # Pass the exact mention text to the blockchain agent
        result = await blockchain_agent.run(mention.text)
        tx_data = result.data

        # Generate a Twitter thread using the transaction data
        thread = await generate_twitter_thread(tx_data)

        # Post the thread as replies
        original_tweet_id = mention.id

        # Post first tweet as reply to the mention
        tweet1 = post_reply(thread.tweet1, original_tweet_id)
        print(f"Posted first tweet: {thread.tweet1[:30]}...")

        # Post second tweet as reply to the first tweet
        tweet2 = post_reply(thread.tweet2, tweet1.data.id)
        print(f"Posted second tweet: {thread.tweet2[:30]}...")

        # Post third tweet as reply to the second tweet
        tweet3 = post_reply(thread.tweet3, tweet2.data.id)
        print(f"Posted third tweet: {thread.tweet3[:30]}...")

        print(f"Thread posted successfully in response to mention {mention.id}")

    except Exception as e:
        print(f"Error processing mention: {e}")


async def main():
    print("Starting Twitter bot...")

    # Get the initial mention as reference point
    initial_mentions = get_recent_mentions()

    # Store initial mention ID to ignore on first run
    last_processed_id = None
    if initial_mentions:
        # Get the most recent mention (first in the list)
        last_processed_id = initial_mentions[0].id
        print(
            f"Initial mention ID recorded: {last_processed_id}. Will only process new mentions."
        )

    while True:
        try:
            mentions = get_recent_mentions()

            if mentions and last_processed_id != mentions[0].id:
                # Only process the most recent mention (first in the list)
                mention = mentions[0]
                print(f"New mention found: {mention.id}")

                await process_mention(mention)
                last_processed_id = mention.id
            else:
                print("No new mentions found")

            # Wait 15 minutes before checking again
            print("Waiting 15 minutes before checking for new mentions...")
            time.sleep(15 * 60)

        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    asyncio.run(main())
