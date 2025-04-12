from langchain.agents import Tool
from call_generate_schema_api import call_generate_schema_api

generate_schema_tool = Tool(
    name="GenerateRobotSchema",
    func=call_generate_schema_api,
    description="Generate a soft robot DSL schema from a natural language prompt"
)

# Export all tools as a list
tool_list = [generate_schema_tool]