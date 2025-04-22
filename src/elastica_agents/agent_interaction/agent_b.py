import random

from dotenv import load_dotenv
from fastapi import Body, FastAPI
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()


@app.post("/judge")
def judge(data: dict = Body(...)):
    move_a = data["agent_a_move"]
    move_b = random.choice(["rock", "paper", "scissors"])

    prompt = f"Agent A chose {move_a}. Agent B chose {move_b}. Who wins and why?"

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    result = llm.invoke(prompt)

    return {"agent_b_move": move_b, "judgment": result.content.strip()}
