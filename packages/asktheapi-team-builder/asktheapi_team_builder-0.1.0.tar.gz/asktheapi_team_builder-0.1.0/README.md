# AutoGen Team Builder

[![PyPI version](https://badge.fury.io/py/asktheapi-team-builder.svg)](https://badge.fury.io/py/asktheapi-team-builder)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/asktheapi-team-builder.svg)](https://pypi.org/project/asktheapi-team-builder/)

A high-level Python library for easily building and managing teams of AutoGen agents. This package provides a clean, type-safe interface for creating, configuring, and running teams of agents that can work together to solve complex tasks.

## Features

- 🚀 Easy creation of individual agents with custom tools and capabilities
- 🤝 Team building with automatic coordination through a planning agent
- 📡 Support for streaming agent interactions
- 🔧 Built-in HTTP client for tool implementation
- ✨ Pydantic models for type safety and validation
- 🎯 Clean, intuitive API design

## Installation

```bash
pip install asktheapi-team-builder
```

## Quick Start

Here's how to use the package:



# 1. Create agents from OpenAPI spec
```python
from asktheapi_team_builder import TeamBuilder, Agent, Tool, Message, APISpecHandler
from typing import List
async def create_agents_from_spec():
    # Initialize handlers
    api_spec_handler = APISpecHandler(llm_service)  # llm_service is your LLM provider
    
    # Download and parse OpenAPI spec
    spec_content = await api_spec_handler.download_url_spec("https://api.example.com/openapi.json")
    
    # Classify endpoints into logical groups
    classification_result = await api_spec_handler.classify_spec(
        spec_content,
        system_prompt="Classify these API endpoints into logical groups",
        user_prompt="Please analyze the API spec and group related endpoints"
    )
    
    # Generate agents for each group
    agents = []
    for group_spec in classification_result.specs:
        agent_result = await api_spec_handler.generate_agent_for_group(
            group_spec,
            spec_content,
            system_prompt="Generate an agent for this group of endpoints",
            user_prompt="Create an agent that can effectively use these endpoints"
        )
        agents.append(agent_result)
    
    return agents

# 3. Build and run a team
async def run_agent_team(agents: List[Agent], query: str):
    # Initialize team builder
    team_builder = TeamBuilder(
        model="gpt-4",
        model_config={"temperature": 0.7}
    )
    
    # Build the team
    team = await team_builder.build_team(agents)
    
    # Create messages
    messages = [
        Message(
            role="user",
            content=query
        )
    ]
    
    # Run the team with streaming
    async for event in team_builder.run_team(team, messages, stream=True):
        if isinstance(event, ChatMessage):
            print(f"{event.source}: {event.content}")
        
# Example usage
async def main():
    # Create agents from spec
    api_agents = await create_agents_from_spec()
    
    # Combine with manual agents
    all_agents = [weather_agent] + api_agents
    
    # Run the team
    await run_agent_team(
        all_agents,
        "What's the weather like in London and how might it affect local businesses?"
    )

## Custom Headers and Configuration

You can configure the team builder with custom headers and model settings:

```python
team_builder = TeamBuilder(
    model="gpt-4",
    model_config={
        "temperature": 0.7,
        "default_headers": {
            "Authorization": "Bearer your-token",
            "Custom-Header": "custom-value"
        }
    }
)

# Run team with extra headers for specific requests
team = await team_builder.build_team(agents)
result = await team_builder.run_team(
    team,
    messages,
    extra_headers={"Request-ID": "123"}
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/alexalbala/asktheapi-team-builder.git
cd asktheapi-team-builder

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [Microsoft's AutoGen](https://github.com/microsoft/autogen)
- Inspired by the need for a higher-level interface for agent team management 