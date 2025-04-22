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


if __name__ == "__main__":
    start = time.time()
    asyncio.run(example_usage())
    end = time.time()
    print(f"\nTotal run time: {end - start:.2f}s")
