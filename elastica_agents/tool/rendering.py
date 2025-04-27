from typing import Any
import os
from pathlib import Path
import importlib.resources
from abc import ABC, abstractmethod

import numpy as np
import vapory

from elastica_agents.design_schema import (
    RobotDesignSchema,
    Point3D,
)


class PVGeometry(ABC):
    pigment = vapory.Pigment("color", [0.45, 0.39, 1.0], "transmit", 0.0)
    texture = vapory.Texture(pigment, vapory.Finish("phong", 1))

    @abstractmethod
    def __call__(self):
        pass


class PVRod(PVGeometry):
    def __init__(self, start_point: Point3D, end_point: Point3D, radius: float):
        self.start_point = [start_point.x, start_point.y, start_point.z]
        self.end_point = [end_point.x, end_point.y, end_point.z]
        self.radius = radius

    def __call__(self):
        return vapory.Cylinder(
            self.start_point,
            self.end_point,
            self.radius,
            self.texture,
        )

        # FIXME: Probably need more points
        # return vapory.SphereSweep(
        #     "linear_rod",
        #     2,
        #     self.start_point,
        #     self.radius,
        #     self.end_point,
        #     self.radius,
        #     self.texture,
        # )


def extract_rods(design_schema: RobotDesignSchema) -> list[PVRod]:
    rods = []
    for actuator in design_schema.actuators:
        rod = PVRod(
            start_point=actuator.start_point,
            end_point=actuator.end_point,
            radius=actuator.radius,
        )
        rods.append(rod)
    return rods


def render_design(
    design_schema: RobotDesignSchema,
    output_path: str | None = None,
    width: int = 800,
    height: int = 600,
) -> np.ndarray:
    """
    Render the robot design using Vapory.

    Args:
        design_schema: Robot design specification
        output_path: Path to save the rendered image
        (if None, image is saved in the current working directory)
        width: Image width in pixels
        height: Image height in pixels

    Returns:
        np.ndarray: Rendered image as a numpy array
    """
    rods = extract_rods(design_schema)

    background_path = str(
        importlib.resources.files("elastica_agents") / "tool" / "povray_background.inc"
    )
    light = vapory.LightSource([2, 4, -3], "color", [1, 1, 1])

    # Camera settings
    camera_position = [0.6, 0.7, -0.9]
    look_at = [0.0, 0.0, 0.0]
    # angle = 30
    camera = vapory.Camera(
        "location", camera_position, "look_at", look_at
    )  # , "angle", 30)

    objects = [light]
    for rod in rods:
        objects.append(rod())

        # text_label = Text(
        #     "ttf",
        #     '"timrom.ttf"',
        #     f'"{actuator.id}"',
        #     0.1,
        #     0.0,
        #     "scale",
        #     [0.5, 0.5, 0.5],
        #     "translate",
        #     text_position,
        #     Texture(Pigment("color", [0, 0, 0])),
        # )
        # objects.append(text_label)

    # Render connections
    # for connection in design_schema.connections:
    #     # Draw connections as small boxes between the connected points
    #     for point in connection.rigid_link_locations:
    #         position = (point.x, point.y, point.z)
    #         connection_box = Box(
    #             [p - 0.2 for p in position],
    #             [p + 0.2 for p in position],
    #             connection_material,
    #         )
    #         objects.append(connection_box)

    # Create the scene
    scene = vapory.Scene(camera, objects=objects, included=[background_path])

    # Render
    image = scene.render(width=width, height=height, antialiasing=0.01)

    # Save if path is provided
    if not output_path:
        output_path = "./robot_view.png"

    from PIL import Image as PILImage

    img = PILImage.fromarray(image)
    img.save(output_path)

    return image
