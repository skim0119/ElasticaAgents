from typing import Any

import sys
import json
import logging

import uuid
import numpy as np

from pydantic import BaseModel
from fastapi import FastAPI, Request, Response, HTTPException

import uvicorn
import click

from .environment import make_env, SimulationEnvironmentProtocol


class SimulationEnvs:
    """
    Environment manager for this server.
    All environments is stored under a 8-character identifier.
    """

    def __init__(self) -> None:
        self.envs: dict[str, SimulationEnvironmentProtocol] = {}
        self._id_len = 8

    def _lookup_env(self, instance_id: str) -> SimulationEnvironmentProtocol:
        try:
            return self.envs[instance_id]
        except KeyError:
            raise HTTPException(
                status_code=400, detail=f"Instance_id {instance_id} unknown"
            )

    def _remove_env(self, instance_id: str) -> None:
        try:
            del self.envs[instance_id]
        except KeyError:
            raise HTTPException(
                status_code=400, detail=f"Instance_id {instance_id} unknown"
            )

    def create(self) -> str:
        try:
            instance_id = str(uuid.uuid4().hex)[: self._id_len]
            env = make_env(instance_id)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Attempted to look up malformed environment ID '{instance_id}'",
            )
        self.envs[instance_id] = env
        return instance_id

    def build(self, instance_id: str, schema: dict[str, Any]) -> None:
        env = self._lookup_env(instance_id)
        env.build(schema)

    def run(self, instance_id: str, simulation_time: float) -> dict[str, Any]:
        env = self._lookup_env(instance_id)
        result = env.run(simulation_time)
        return result

    def env_close(self, instance_id: str) -> None:
        env = self._lookup_env(instance_id)
        env.close()
        self._remove_env(instance_id)


########## API models ##########
class EnvCreateRequest(BaseModel):
    env_id: str


class EnvCreateResponse(BaseModel):
    instance_id: str


class EnvListResponse(BaseModel):
    all_envs: dict[str, str]


class EnvRunRequest(BaseModel):
    simulation_time: float


class EnvRunResponse(BaseModel):
    result: Any


class EnvBuildRequest(BaseModel):
    simulation_schema: dict[str, Any]


# App setup
app = FastAPI(title="Simulation Server API")
envs = SimulationEnvs()


# API route definitions
@app.post("/envs/", response_model=EnvCreateResponse)
async def env_create(request: EnvCreateRequest):
    """
    Create an instance of the specified environment

    Returns:
        - instance_id: a string identifier for the created environment instance.
        The instance_id is used in future API calls to identify the environment to be
        manipulated.
    """
    instance_id = envs.create()
    return {"instance_id": instance_id}



@app.post("/envs/{instance_id}/build/")
async def env_build(instance_id: str, request: EnvBuildRequest):
    """
    Build the environment with the given simulation schema.
    """
    envs.build(instance_id, request.simulation_schema)


@app.post("/envs/{instance_id}/run/", response_model=EnvRunResponse)
async def env_run(instance_id: str, request: EnvRunRequest):
    """
    Run the environment for a given amount of time.
    """
    result = envs.run(instance_id, request.simulation_time)
    return result


@app.post("/envs/{instance_id}/close/", status_code=204)
async def env_close(instance_id: str):
    """
    Manually close an environment
    """
    envs.env_close(instance_id)
    return Response(status_code=204)


def get_application():
    """Retriece the FastAPI application."""
    return app


@click.command()
@click.option("--host", "-h", default="127.0.0.1", help="Listening address")
@click.option("--port", "-p", default=5000, type=int, help="Binding port")
def main(host, port):
    """Start the HTTP API server"""
    logger = logging.getLogger(__name__)
    logger.info(f"Server starting at: http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
