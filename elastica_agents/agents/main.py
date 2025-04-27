import asyncio
import random
import time
import logging

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.orchestrator.orchestrator import Orchestrator
from mcp_agent.workflows.llm.augmented_llm import RequestParams

app = MCPApp(name="rock_paper_scissors")


def my_rps_choice() -> str:
    """
    Returns a random choice from rock, paper, or scissors.
    """
    choice = random.choice(["rock", "paper", "scissors"])
    # logger.info(f"Agent picked: {choice}")
    return choice


async def example_usage():
    async with app.run() as agent_app:
        logger = agent_app.logger
        context = agent_app.context

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

        orchestrator = Orchestrator(
            llm_factory=OpenAIAugmentedLLM,
            available_agents=[
                agent_1,
                agent_2,
            ],
            # We will let the orchestrator iteratively plan the task at every step
            plan_type="full",
        )

        # Let the judge LLM coordinate the game
        response = await orchestrator.generate_str(
            message="""
                You are the referee of a rock-paper-scissors match.
                Ask `agent_1` and `agent_2` to make their moves by sending them messages.
                Once you have both moves, determine who wins based on the standard rock-paper-scissors rules.
            """,
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
        logger.info(f"Running with prompt: {prompt}")

        # Check if required packages are installed
        try:
            # This would be the actual implementation
            logger.info("Agent processing the design request...")
            # TODO: Implement the actual agent logic using mcp-agent

        except Exception as e:
            logger.error(f"Error running agents: {e}")
            logger.error("Make sure all dependencies are installed with 'uv sync'")
            sys.exit(1)

        logger.info("Design processing complete")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(example_usage())
    end = time.time()
    print(f"\nTotal run time: {end - start:.2f}s")
