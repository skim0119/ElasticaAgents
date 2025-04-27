from typing import Literal
from enum import Enum

import numpy as np

from pydantic import BaseModel, Field


class BendingParameter(BaseModel):
    bending_direction: tuple[float, float, float]
    max_bending_magnitude: float


class TwistingParameter(BaseModel):
    twisting_direction: Literal["CW", "CCW"]
    max_twisting_magnitude: float


class ActuatorMode(str, Enum):
    BENDING = "bending"  # Lab frame
    TWISTING_CLOCKWISE = "twisting_clockwise"
    TWISTING_COUNTER_CLOCKWISE = "twisting_counter_clockwise"


class Point3D(BaseModel):
    x: float
    y: float
    z: float


class RotationMatrix(BaseModel):
    d1: tuple[float, float, float]
    d2: tuple[float, float, float]
    d3: tuple[float, float, float]

    def Q(self) -> np.ndarray:
        return np.array([self.d1, self.d2, self.d3])


class Actuator(BaseModel):
    id: str
    mode: list[ActuatorMode]
    actuation_parameter: list[BendingParameter | TwistingParameter]
    start_point: Point3D
    end_point: Point3D
    radius: float
    orientation: RotationMatrix  # d3 should be along the actuation direction


class Connection(BaseModel):
    actuators: list[str]
    rigid_link_locations: list[Point3D]
    orientation: RotationMatrix


class ActuationGroup(BaseModel):
    name: str
    actuators_actuation: list[tuple[str, int]] = Field(
        default_factory=list
    )  # List of ActuatorIDs


class RobotDesignSchema(BaseModel):
    actuators: list[Actuator] = Field(default_factory=list)
    connections: list[Connection] = Field(default_factory=list)
    actuation_groups: list[ActuationGroup] = Field(default_factory=list)
