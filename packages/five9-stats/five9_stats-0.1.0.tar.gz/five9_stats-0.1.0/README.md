# Five9 Statistics API Client Library

A Python client library for the Five9 Statistics APIs, providing asynchronous access to both the Interval Statistics API and the Real-time Stats Snapshot API.

## Features

- Asynchronous API clients using `aiohttp`
- Pydantic models for request and response data
- Support for both Interval Statistics API and Real-time Stats Snapshot API
- Automatic retry mechanism for rate limiting and service unavailability
- Comprehensive error handling

## Installation

```bash
pip install five9-stats
```

Or install from source:

```bash
git clone https://github.com/james-smart/five9-stats.git
cd five9-stats
pip install -e .
```

## Requirements

- Python 3.7+
- aiohttp
- pydantic

## Usage

See the included exmple.py script for a complete example of how to use the library.

### Interval Statistics API

The Interval Statistics API provides historical statistics for domains, agents, campaigns, and ACD.

```python
import asyncio
from five9_stats.api.interval import IntervalStatsClient

async def main():
    # Initialize the client
    client = IntervalStatsClient(
        username="your_username",
        password="your_password",
        base_url="https://api.prod.us.five9.net"  # Optional, defaults to US production
    )
    
    # Use the client as an async context manager
    async with client:
        # Get statistics metadata
        metadata = await client.get_statistics_metadata(domain_id="your_domain_id")
        print(f"Available statistics types: {[m.statistics_type for m in metadata.items]}")
        
        # Get agent statistics
        agent_stats = await client.get_agent_statistics(
            domain_id="your_domain_id",
            media_types="VOICE,CHAT,EMAIL",
            time_period="LAST_15_MINUTES"
        )
        
        # Print agent statistics
        for agent in agent_stats.data:
            print(f"Agent ID: {agent.id}")
            print(f"Total calls handled: {agent.total_calls_handled}")
            print(f"Total chats handled: {agent.total_chats_handled}")
            print(f"Total emails handled: {agent.total_emails_handled}")
            print("---")

# Run the async function
asyncio.run(main())
```

### Real-time Stats Snapshot API

The Real-time Stats Snapshot API provides real-time statistics for domains, agents, interactions, campaigns, and utilization thresholds.

```python
import asyncio
from five9_stats.api.snapshot import SnapshotStatsClient

async def main():
    # Initialize the client
    client = SnapshotStatsClient(
        username="your_username",
        password="your_password",
        base_url="https://api.prod.us.five9.net"  # Optional, defaults to US production
    )
    
    # Use the client as an async context manager
    async with client:
        # Get ACD status
        acd_status = await client.get_acd_status(
            domain_id="your_domain_id",
            media_types="VOICE,CHAT,EMAIL"
        )
        
        # Print ACD status
        for skill in acd_status.data:
            print(f"Skill ID: {skill.id}")
            print(f"Active calls: {skill.active_calls}")
            print(f"Agents active: {skill.agents_active}")
            print(f"Agents on call: {skill.agents_on_call}")
            print(f"Calls in queue: {skill.calls_in_queue}")
            print("---")
        
        # Get agent state
        agent_state = await client.get_agent_state(
            domain_id="your_domain_id",
            media_types="VOICE,CHAT,EMAIL"
        )
        
        # Print agent state
        for agent in agent_state.data:
            print(f"Agent ID: {agent.id}")
            print(f"Presence state: {agent.presence_state}")
            print(f"Voice interaction state: {agent.voice_interaction_state}")
            print(f"Chat interaction state: {agent.chat_interaction_state}")
            print(f"Email interaction state: {agent.email_interaction_state}")
            print("---")

# Run the async function
asyncio.run(main())
```

## Error Handling

The library provides comprehensive error handling for API errors:

```python
import asyncio
from five9_stats.api.interval import IntervalStatsClient

async def main():
    client = IntervalStatsClient(username="your_username", password="your_password")
    
    async with client:
        try:
            # Try to get statistics for a non-existent domain
            stats = await client.get_agent_statistics(domain_id="invalid_domain_id")
        except ValueError as e:
            print(f"API error: {e}")

asyncio.run(main())
```

## Advanced Usage

### Custom Retry Logic

You can customize the retry behavior:

```python
client = IntervalStatsClient(
    username="your_username",
    password="your_password",
    max_retries=5,       # Maximum number of retries
    retry_delay=2        # Initial delay between retries in seconds (will use exponential backoff)
)
```

### Using Different Regional Endpoints

Five9 provides different regional endpoints:

```python
# US production
client = IntervalStatsClient(
    username="your_username",
    password="your_password",
    base_url="https://api.prod.us.five9.net"
)

# EU production
client = IntervalStatsClient(
    username="your_username",
    password="your_password",
    base_url="https://api.prod.eu.five9.net"
)

# CA production
client = IntervalStatsClient(
    username="your_username",
    password="your_password",
    base_url="https://api.prod.ca.five9.net"
)
```

## License

MIT