import sys
import asyncio
import random
import time
import logging

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.llm.augmented_llm import RequestParams


def assert_api_key_exist(logger: logging.Logger):
    if not os.environ.get("OPENAI_API_KEY"):
        logger.warning("OPENAI_API_KEY environment variable is not set.")
        logger.info("Please set it with: export OPENAI_API_KEY='your-openai-key'")
        sys.exit()



async def example_usage(app: MCPApp, agents: list[Agent], prompt: str):
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context

        orchestrator = Orchestrator(
            llm_factory=OpenAIAugmentedLLM,
            context=context,
            available_agents=agents
            # We will let the orchestrator iteratively plan the task at every step
            plan_type="full",
        )

        # Let the judge LLM coordinate the game
        response = await orchestrator.generate_str(
            message=prompt,
            request_params=RequestParams(model="gpt-4o"),
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
        self.app = MCPApp(name="ElasticaAgent")

        self.logger = logging.getLogger("ElasticaAgents")
        assert_api_key_exist(self.logger)

        self.workdir = Path(workdir)
        self.verbose = verbose
        self.model = "gpt-4o-mini"
        self.temp = 0.1

        if verbose:
            logger.setLevel(logging.DEBUG)

        logger.debug(f"Initialized ElasticaAgents with workdir: {self.workdir}")

    def config(self, model: Optional[str] = None, temp: Optional[float] = None):
        """Configure the agents

        Args:
            model: LLM model to use
            temp: Temperature for LLM generation

        Returns:
            self: For method chaining
        """
        if model:
            self.model = model
        if temp is not None:
            self.temp = temp

        logger.debug(f"Configured with model={self.model}, temp={self.temp}")
        return self

    def run(self, prompt: str):
        """Run the ElasticaAgents with the given prompt

        Args:
            prompt: Design prompt for the agents
        """
        self.logger.info(f"Running with prompt: {prompt}")

        # Check if required packages are installed
        try:
            # This would be the actual implementation
            self.logger.info("Agent processing the design request...")
            team = self.create_team()
            start_time = time.time()
            asyncio.run(example_usage(self.app, team, prompt))
            end_time = time.time()
            self.logger.info(f"Agent processing time: {end_time - start_time:.2f}s")

        except Exception as e:
            self.logger.error(f"Error running agents: {e}")
            self.logger.error("Make sure all dependencies are installed with 'uv sync'")
            sys.exit(1)

        self.logger.info("Design processing complete")

    def create_team(self) -> list[Agent]:
        # TODO
        player_prompt = """
            You are a rock-paper-scissors player.
            When referee asks, use 'my_rps_choice' tool to pick a move. (Don't ask human!)
        """
        agent_1 = Agent(
            name="agent_1",
            instruction=player_prompt,
            functions=[my_rps_choice],
        )

        agent_2 = Agent(
            name="agent_2",
            instruction=player_prompt,
            functions=[my_rps_choice],
        )

        return [agent_1, agent_2]
