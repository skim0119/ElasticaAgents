import os
import sys
import click

from elastica_agents.agents import ElasticaAgents


@click.command()
@click.option("-m", "--message", required=True, help="Design prompt for the agents")
@click.option(
    "--workdir", type=click.Path(), default=".", help="Working directory for outputs"
)
@click.option("--verbose", is_flag=True, help="Enable verbose output")
@click.option("--model", default="gpt-4o-mini", help="LLM model to use.")
@click.option(
    "--temperature", default=0.1, type=float, help="Temperature for LLM generation"
)
def main(message: str, workdir: str, verbose: bool, model: str, temperature: float):
    """ElasticaAgents CLI tool for soft robotics design"""
    os.makedirs(workdir, exist_ok=True)

    agents = ElasticaAgents(workdir=workdir, verbose=verbose).config(
        model=model, temperature=temperature
    )
    agents.run(message)
