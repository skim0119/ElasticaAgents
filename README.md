# ElasticaAgents: Modular design for soft robotics and simulation

**ElasticaAgents** is an open-source framework for translating high-level design instructions into modular soft-robotic assemblies. It leverages LLM-driven multi-agents, the PyElastica physics engine, and FastAPI to enable end-to-end prototyping and optimization of soft-robotic designs.

> dev note: use uv for package management

---

## Features

- **LLM-Powered Design Agents**
  Multiple agent architectures for design prototyping, parameter tuning, and assembly planning.

- **Simulation API**
  A FastAPI server wrapping the PyElastica simulator for real-time physics validation and visualization.

- **Schema-Driven Assemblies**
  JSON/YAML schemas to describe modular soft-robotic components and their interconnections.

- **Extensible Toolchain**
  Plug-in support for new actuation models, material properties, and visualization back-ends.

---

## Installation

```bash
uv sync
```

---

## Quick Start

1. **Set up your environment**
   ```bash
   export OPENAI_API_KEY="your-openai-key"
   ```

2. **Launch the Simulation Server**
   ```bash
   elastica-mcp-server --host 0.0.0.0 --port 8000
   ```

3. **Control from Python**
   ```python
   from elastica_agents import ElasticaAgents

   agents = ElasticaAgents(workdir=".", verbose=True).config(
       model="gpt-4o-mini", temp=0.1,
   )
   agents.run(prompt)
   ```

4. **CLI**
   ```bash
   elastica-agents -m "design a snake-robot with 3 actuators."
   ```

---

## Testing

Automated tests cover both library modules and API endpoints:

```bash
pytest
```

---

## Self-hosting Tools

### Elastica Simulation Server

```bash
elastica-mcp-server --host 0.0.0.0 --port 8000
```