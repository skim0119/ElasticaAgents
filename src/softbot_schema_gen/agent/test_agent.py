
from langchain.agents import initialize_agent
from langchain_community.chat_models import ChatOpenAI
from tools import tool_list

def main():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
    )

    agent = initialize_agent(
        tools=tool_list,
        llm=llm,
        agent_type="zero-shot-react-description",
        verbose=True
    )
    
    task = "Design a soft robot with 3 bending actuators and connect them in parallel"
    result = agent.run(task)

    print("\nOutput:\n")
    print(result)

if __name__ == "__main__":
    main()