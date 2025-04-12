from fastapi import FastAPI
from pydantic import BaseModel
from schema_parser import instruction_to_schema

# for Fast API implementatation
app = FastAPI()

# python class for Input/Output Jason structure for FastAPI 
class Instruction(BaseModel):
    instruction: str

class RawText(BaseModel):
    schema: str

@app.post("/generate-schema", response_model=RawText)
def generate_schema(instruction: Instruction):
    schema_text = instruction_to_schema(instruction.instruction)
    return {"schema": schema_text}