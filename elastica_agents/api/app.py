"""
FastAPI application for ElasticaAgents simulation server.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("elastica_agents.api")

# Create FastAPI app
app = FastAPI(
    title="ElasticaAgents API",
    description="API for soft robotics simulation using PyElastica",
    version="0.1.0",
)


class SimulationStatus(BaseModel):
    """Status response for the simulation API."""

    status: str
    version: str


@app.get("/", response_model=SimulationStatus)
async def root():
    """Get the status of the simulation server."""
    return SimulationStatus(
        status="running",
        version="0.1.0",
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


# Import and include routers
# Import this after app creation to avoid circular imports
from elastica_agents.api import simulation

app.include_router(simulation.router, prefix="/simulation", tags=["simulation"])
