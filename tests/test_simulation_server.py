import pytest

k
import sys
import os
import time
import threading
import uvicorn

# FIXME: Temporary solution until we have a proper package
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.simulation_api.client import Client
from src.simulation_api.server import app


@pytest.fixture(scope="module")
def simulation_server():
    """Start the server and provide client fixture"""
    # Local server configuration
    host = "127.0.0.1"
    port = 8000
    server_url = f"http://{host}:{port}"

    # Start server in a separate thread
    server_thread = threading.Thread(
        target=uvicorn.run,
        kwargs={"app": app, "host": host, "port": port},
        daemon=True,
    )
    server_thread.start()
    time.sleep(1)  # Wait for server to start
    client = Client(server_url)

    yield client


def test_env_create(simulation_server):
    """Test environment creation"""
    instance_id = simulation_server.env_create()

    assert isinstance(instance_id, str)
    assert len(instance_id) == 8  # IDs are 8 characters long


def test_env_build_and_run(simulation_server):
    """Test building and running a simulation"""
    # Create environment
    instance_id = simulation_server.env_create()

    # Build environment with test schema
    test_schema = {
        "elements": 15,
        "parameters": {"modulus": 1.0, "density": 1000.0},
    }
    simulation_server.env_build(instance_id, test_schema)

    # Run simulation
    simulation_time = 5.0
    result = simulation_server.env_run(instance_id, simulation_time)

    # Check result structure
    assert "walltime" in result
    assert "end_status" in result
    assert "simulation_results" in result
    # Close environment
    simulation_server.env_close(instance_id)
