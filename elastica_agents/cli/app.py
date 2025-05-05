import os
import sys
import click
import asyncio
import logging
from elastica_agents.agents import ElasticaAgents


@click.command()
@click.option("-m", "--message", required=True, help="Design prompt for the agents")
@click.option(
    "--workdir", type=click.Path(), default=".", help="Working directory for outputs"
)
@click.option("--model", default="gpt-4o-mini", help="LLM model to use.")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(message: str, workdir: str, verbose: bool, model: str):
    """ElasticaAgents CLI tool for soft robotics design"""

    # Run simple mcp-agent
    agents = ElasticaAgents(workdir=workdir, verbose=verbose).config(model=model)
    asyncio.run(agents.run(message))
