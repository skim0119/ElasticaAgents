import os
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP
from schema_parser import instruction_to_schema

mcp = FastMCP("generate_schema_with_validation")

# Input schema using Pydantic
class Instruction(BaseModel):
    instruction: str

# Output schema using Pydantic
class RawSchema(BaseModel):
    schema: str

@mcp.tool()
def generate_schema(instruction: str) -> RawSchema:
    """
    Generate a soft robot schema from a natural language instruction using OpenAI API.

    Args:
        data (Instruction): An object containing a single field:
            - instruction (str): A natural language description of the soft robot design,
              such as "make a robot that slithers like a snake".

    Returns:
        RawSchema: An object containing a single field:
            - schema (str): The resulting text-based robot schema representing actuators,
              connections, and actuation groups.
    """
    validated = Instruction(instruction=instruction)
    schema_text = instruction_to_schema(instruction)
    return RawSchema(schema=schema_text)

if __name__ == "__main__":
    mcp.run(transport="stdio")