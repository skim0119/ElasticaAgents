"""
Environment wrapper for existing simulation.
"""

from typing import Any, Protocol

import time
import numpy as np

class SimulationEnvironmentProtocol(Protocol):
    def build(self, simulation_schema: dict[str, Any]) -> None:
        ...

    def run(self, simulation_time: float) -> dict[str, Any]:
        ...

    def close(self) -> None:
        ...

class MockEnvWrapper(SimulationEnvironmentProtocol):
    """Base class for mock environments."""

    def __init__(self, uid:str, *args: Any, **kwargs: Any) -> None:
        self.uid = uid
        self.n_elem = 10

    def build(self, simulation_schema: dict[str, Any]) -> None:
        pass

    def run(self, simulation_time: float) -> dict[str, Any]:
        start_time = time.time()
        time.sleep(1.0)
        walltime = time.time() - start_time
        return {
            "walltime": walltime,
            "positions": np.random.uniform(size=(3, self.n_elem + 1)),
            "directors": np.random.uniform(size=(3, 3, self.n_elem)),
        }

    def close(self) -> None:
        pass


# Registry to store available environments
def make_env(env_id: str) -> MockEnvWrapper:
    """Create an instance of the specified environment."""
    return MockEnvWrapper(env_id)
