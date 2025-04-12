# Natural Language to Real: Modular design for soft robotics

> dev note: use uv for package management

## Features

- Use FastAPI and MCP to expose existing python-simulation package and visualization tools for LLM
- Different LLMAgent system for prototyping and optimization
- Provide design schema and assembly instruction for soft robotics

## Dev note

### File structure

- `src`: Libraries
    - `elastica_agents`: Core library for soft robotics LLM agents
    - `simulation_api`: FastAPI server exposing PyElastica simulator
- `examples`: Examples, tutorial, scripts for demonstrations
- `tests`: Unit test for the library and API

### Testing

Run the tests to verify the client-server functionality:

```bash
uv run pytest
```

### API Endpoints

The server provides the following endpoints:

- `POST /envs/` - Create a new environment
- `POST /envs/{instance_id}/build/` - Build the environment with simulation schema
- `POST /envs/{instance_id}/run/` - Run the simulation for a specified time
- `POST /envs/{instance_id}/close/` - Close the environment
