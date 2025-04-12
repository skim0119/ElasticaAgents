import pytest
import sys

# FIXME: Temporary solution until we have a proper package
sys.path.append(os.path.join(os.path.dirname(__file__), "../../src"))

from elastica_agents.call_generate_schema_api import call_generate_schema_api

def test_generate_schema():
    instruction = "Design a soft robot that can crawl like a worm in its simplest form"
    schema = call_generate_schema_api(instruction)

    assert isinstance(schema, str)

