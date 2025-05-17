# AskPayxn - AI Agent X Bot/Payments with AI KYC & ZK Privacy

A flexible Twitter bot powered by Base AgentKit and Pydantic AI that interacts with blockchain data. This bot can analyze on-chain transactions, respond to user queries, and automatically post real-time insights and alerts to Twitter.

## 🚀 Deployed Base Mainnet Contracts
- AI Oracle Proxy: https://basescan.org/address/0x0A0f4321214BB6C7811dD8a71cF587bdaF03f0A0
- Prompt: https://basescan.org/address/0xC20DeDbE8642b77EfDb4372915947c87b7a526bD

## 🔹 The problem AskPayxn solves
Traditional KYC/AML processes in decentralized finance (DeFi) and peer-to-peer (P2P) payments often require users to share sensitive personal information, risking privacy breaches. Meanwhile, existing compliance solutions struggle to detect suspicious activity without exposing or compromising user data. This gap creates barriers to adoption and leaves platforms vulnerable to fraud, regulatory penalties, and loss of user trust.

## 🚀 To Do
- [x] AI-enchanced KYC/AML solutions that scan user transactions while maintaining privacy
- [x] AI-based decentralized identity verification using zero-knowledge proofs
- [x] AI-generated risk scores for users to impose trust in P2P transactions


## 🚀 Features

- **Multiple Agent Examples**:
  - Basic agent for simple blockchain queries
  - Pydantic structured agent for type-safe blockchain data
  - Twitter bot for responding to mentions
  - Direct query tool for one-off analysis

- **Built-in Tools**:
  - Transaction analysis
  - Smart thread generation
  - Twitter integration

- **Developer-Friendly**:
  - Type annotations throughout
  - Modular architecture
  - Easy to customize and extend

## 📋 Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [Twitter Developer](https://developer.twitter.com/) account (optional, for Twitter integration)

## 🛠️ Installation

1. Clone the repository:
```bash
[git clone https://github.com/payxn-io/askpayxn.git](https://github.com/payxn-io/askpayxn)
cd askpayxn
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies using uv:
```bash
uv pip sync uv.lock
```

4. Copy the example environment file and fill in your API keys:
```bash
cp .env.example .env
```

## ⚙️ Configuration

Edit the `.env` file and add your API keys:

```
# Required for all agents
OPENAI_API_KEY=your_openai_api_key

# Required only for Twitter integration
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
BEARER_TOKEN=your_bearer_token
```

## 🔍 Usage

### Basic Blockchain Agent

Run the basic agent to analyze a transaction:

```bash
python basic_agent.py
```

### Structured Pydantic Agent

Use the Pydantic agent for strongly-typed blockchain data:

```bash
python pydantic_agent_simple.py
```

### Twitter Bot

Start the Twitter bot to listen for mentions:

```bash
python twitter_bot.py
```

### Direct Query

Run a one-off blockchain query and optionally post to Twitter:

```bash
python direct_query.py
```

## 📦 Project Structure

- `basic_agent.py` - Simple blockchain analysis agent
- `pydantic_agent_simple.py` - Structured blockchain data agent using Pydantic models
- `twitter_bot.py` - Twitter bot for monitoring mentions and auto-responding
- `thread_creator.py` - Twitter thread generator
- `direct_query.py` - Command-line tool for one-off blockchain queries

## 🧩 Customizing the Agents

### Adding New Capabilities

1. Add a new tool to an existing agent:

```python
@agent.tool(name="your_new_tool")
def your_new_tool(ctx: RunContext, param1: str, param2: int) -> dict:
    """Your tool description."""
    # Tool implementation
    return {"result": "data"}
```

2. Create a new agent class by extending the existing ones.

### Modifying the Twitter Thread Format

Edit the `generate_twitter_thread` function in `thread_creator.py` to customize the format of generated Twitter threads.

## 🧪 Testing

You can test your agents locally:

```bash
# Test the basic agent
python basic_agent.py

# Test the Twitter thread creator
python thread_creator.py
```

## 📚 Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [Twitter API Documentation](https://developer.twitter.com/en/docs/twitter-api)

## 📝 License

MIT

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
