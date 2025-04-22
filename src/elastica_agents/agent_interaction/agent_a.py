import random

import httpx
from fastapi import FastAPI

app = FastAPI()


@app.post("/start_game")
def start_game():
    # Agent A picks a move
    move = random.choice(["rock", "paper", "scissors"])

    # Send it to Agent B
    response = httpx.post("http://localhost:8002/judge", json={"agent_a_move": move})

    return {"agent_a_move": move, "agent_b_response": response.json()}
