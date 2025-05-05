import os
import sys
import asyncio
import random
import time
import logging
from pathlib import Path

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.llm.augmented_llm import RequestParams

from .settings import get_settings
from ..tool.rendering import render_design
from ..prompts.designer import design_instructions
from ..prompts.rendering import rendering_instructions


def assert_api_key_exist(logger: logging.Logger):
    if not os.environ.get("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY environment variable is not set.")
        logger.info("Please set it with: export OPENAI_API_KEY='your-openai-key'")
        sys.exit()


async def run_agents(app: MCPApp, agents: list[Agent], prompt: str):
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context

        orchestrator = Orchestrator(
            llm_factory=OpenAIAugmentedLLM,
            context=context,
            available_agents=agents,
            # We will let the orchestrator iteratively plan the task at every step
            plan_type="full",
        )

        # Let the judge LLM coordinate the game
        response = await orchestrator.generate_str(
            message=prompt,
            request_params=RequestParams(model="gpt-4o-mini"),
        )

        logger.info(f"Expert math result: {response}")


class ElasticaAgents:
    """ElasticaAgents class to handle interaction with LLM and simulation"""

    def __init__(self, workdir: str = ".", verbose: bool = False):
        """Initialize ElasticaAgents

        Args:
            workdir: Working directory for outputs
            verbose: Enable verbose output
        """

        self.logger = logging.getLogger("ElasticaAgents")
        assert_api_key_exist(self.logger)
        if verbose:
            self.logger.setLevel(logging.DEBUG)

        self.workdir = Path(workdir).resolve()
        self.verbose = verbose
        self.model = "gpt-4o-mini"

        self.logger.debug(f"Initialized ElasticaAgents with workdir: {self.workdir}")

        # Create working directory
        self.workdir.mkdir(parents=True, exist_ok=True)

    def config(self, model: str | None = None):
        """Configure the agents

        Args:
            model: LLM model to use
            temp: Temperature for LLM generation

        Returns:
            self: For method chaining
        """
        if model:
            self.model = model

        self.logger.debug(f"Configured with model={self.model}")
        return self

    def run(self, prompt: str):
        """Run the ElasticaAgents with the given prompt

        Args:
            prompt: Design prompt for the agents
        """
        self.logger.info(f"Running with prompt: {prompt}")

        self.augment_prompt(prompt)

        # Check if required packages are installed
        try:
            settings = get_settings(self.model, self.workdir.as_posix())
            app = MCPApp(name="ElasticaAgent", settings=settings)
            # This would be the actual implementation
            self.logger.info("Agent processing the design request...")
            team = self.create_team()
            start_time = time.time()
            asyncio.run(run_agents(app, team, prompt))
            end_time = time.time()
            self.logger.info(f"Agent processing time: {end_time - start_time:.2f}s")

        except Exception as e:
            self.logger.error(f"Error running agents: {e}")
            sys.exit(1)
        finally:
            app.close()

        self.logger.info("Design processing complete")

    def create_team(self) -> list[Agent]:
        design_agent = Agent(
            name="design_agent",
            instruction=design_instructions,
            server_names=["filesystem"],
        )

        rendering_agent = Agent(
            name="rendering_agent",
            instruction=rendering_instructions,
            server_names=["filesystem"],
            functions=[render_design],
        )

        return [design_agent, rendering_agent]

    def augment_prompt(self, prompt: str):
        """Augment the prompt with the design instructions and rendering instructions"""
        return f"""
        You are managing a team of agents to design a soft robot, composed of straight rods.
        The goal is to create a design in json format, and render it for visualization.

        {prompt}
        """
