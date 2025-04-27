import numpy as np
from vapory import (
    Scene,
    Camera,
    LightSource,
    Cylinder,
    Sphere,
    Texture,
    Pigment,
    Finish,
    Box,
    Text,
    Background,
)
from typing import Dict, Any, Optional, List, Tuple, cast
import os
from pathlib import Path

from elastica_agents.design_schema import (
    RobotDesignSchema,
    Point3D,
    Actuator,
    Connection,
    RotationMatrix,
    ActuatorMode,
    BendingParameter,
)


def render_design(
    design_schema: RobotDesignSchema,
    output_path: Optional[str] = None,
    width: int = 800,
    height: int = 600,
    background_color: tuple = (1, 1, 1),
    camera_position: tuple = (15, 15, 15),
    look_at: tuple = (0, 0, 0),
    light_position: tuple = (30, 30, 30),
) -> np.ndarray:
    """
    Render the robot design using Vapory.

    Args:
        design_schema: Robot design specification
        output_path: Path to save the rendered image (if None, only returns the image)
        width: Image width in pixels
        height: Image height in pixels
        background_color: Background color as RGB tuple (values 0-1)
        camera_position: Position of the camera
        look_at: Point the camera is looking at
        light_position: Position of the light source

    Returns:
        np.ndarray: Rendered image as a numpy array
    """
    # Define camera
    camera = Camera("location", camera_position, "look_at", look_at, "angle", 30)

    # Define light
    light = LightSource(light_position, "color", [1, 1, 1])

    # Create objects list
    objects = [Background("color", background_color), light]

    # Material definitions
    actuator_material = Texture(
        Pigment("color", [0.7, 0.2, 0.2]), Finish("phong", 0.8, "reflection", 0.1)
    )

    connection_material = Texture(
        Pigment("color", [0.2, 0.2, 0.7]), Finish("phong", 0.6)
    )

    # Render actuators
    for actuator in design_schema.actuators:
        # Convert Point3D to tuples
        start = (actuator.start_point.x, actuator.start_point.y, actuator.start_point.z)
        end = (actuator.end_point.x, actuator.end_point.y, actuator.end_point.z)

        # Create cylinder for actuator
        cylinder = Cylinder(start, end, actuator.radius, actuator_material)
        objects.append(cylinder)

        # Add spheres at the ends for better visualization
        objects.append(Sphere(start, actuator.radius * 1.05, actuator_material))
        objects.append(Sphere(end, actuator.radius * 1.05, actuator_material))

        # Add small text label with actuator ID
        mid_point = [(start[i] + end[i]) / 2 for i in range(3)]
        text_position = [
            mid_point[0],
            mid_point[1],
            mid_point[2] + actuator.radius * 1.5,
        ]

        text_label = Text(
            "ttf",
            '"timrom.ttf"',
            f'"{actuator.id}"',
            0.1,
            0.0,
            "scale",
            [0.5, 0.5, 0.5],
            "translate",
            text_position,
            Texture(Pigment("color", [0, 0, 0])),
        )
        objects.append(text_label)

    # Render connections
    for connection in design_schema.connections:
        # Draw connections as small boxes between the connected points
        for point in connection.rigid_link_locations:
            position = (point.x, point.y, point.z)
            connection_box = Box(
                [p - 0.2 for p in position],
                [p + 0.2 for p in position],
                connection_material,
            )
            objects.append(connection_box)

    # Create the scene
    scene = Scene(camera, objects=objects)

    # Render
    image = scene.render(width=width, height=height, antialiasing=0.01)

    # Save if path is provided
    if output_path:
        from PIL import Image as PILImage

        img = PILImage.fromarray(image)
        img.save(output_path)

    return image


def render_multiple_views(
    design_schema: RobotDesignSchema,
    output_dir: str,
    base_filename: str = "robot_view",
    width: int = 800,
    height: int = 600,
    background_color: tuple = (1, 1, 1),
    padding_factor: float = 1.5,
) -> Dict[str, np.ndarray]:
    """
    Render multiple views of the robot design (top, side, front, orthogonal) with zoom calculated
    based on the robot's dimensions.

    Args:
        design_schema: Robot design specification
        output_dir: Directory to save the rendered images
        base_filename: Base name for the output files
        width: Image width in pixels
        height: Image height in pixels
        background_color: Background color as RGB tuple (values 0-1)
        padding_factor: Factor to add padding around the robot in the view (1.5 = 50% padding)

    Returns:
        Dict[str, np.ndarray]: Dictionary of view names and corresponding rendered images
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Calculate robot's dimensions from its components
    min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
    max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")

    # Process actuators
    for actuator in design_schema.actuators:
        # Start point
        min_x = min(min_x, actuator.start_point.x - actuator.radius)
        min_y = min(min_y, actuator.start_point.y - actuator.radius)
        min_z = min(min_z, actuator.start_point.z - actuator.radius)
        max_x = max(max_x, actuator.start_point.x + actuator.radius)
        max_y = max(max_y, actuator.start_point.y + actuator.radius)
        max_z = max(max_z, actuator.start_point.z + actuator.radius)

        # End point
        min_x = min(min_x, actuator.end_point.x - actuator.radius)
        min_y = min(min_y, actuator.end_point.y - actuator.radius)
        min_z = min(min_z, actuator.end_point.z - actuator.radius)
        max_x = max(max_x, actuator.end_point.x + actuator.radius)
        max_y = max(max_y, actuator.end_point.y + actuator.radius)
        max_z = max(max_z, actuator.end_point.z + actuator.radius)

    # Process connections
    for connection in design_schema.connections:
        for point in connection.rigid_link_locations:
            min_x = min(min_x, point.x - 0.2)
            min_y = min(min_y, point.y - 0.2)
            min_z = min(min_z, point.z - 0.2)
            max_x = max(max_x, point.x + 0.2)
            max_y = max(max_y, point.y + 0.2)
            max_z = max(max_z, point.z + 0.2)

    # Calculate center and dimensions
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    center_z = (min_z + max_z) / 2

    center = (center_x, center_y, center_z)

    # Calculate the maximum dimension for zoom
    width_x = max_x - min_x
    width_y = max_y - min_y
    width_z = max_z - min_z
    max_dim = max(width_x, width_y, width_z) * padding_factor

    # Define views with camera positions and names
    views = {
        "top": {
            "camera_position": (center_x, center_y + max_dim, center_z),
            "filename": f"{base_filename}_top.png",
        },
        "front": {
            "camera_position": (center_x, center_y, center_z - max_dim),
            "filename": f"{base_filename}_front.png",
        },
        "side": {
            "camera_position": (center_x + max_dim, center_y, center_z),
            "filename": f"{base_filename}_side.png",
        },
        "orthogonal": {
            "camera_position": (
                center_x + max_dim / 1.5,
                center_y + max_dim / 1.5,
                center_z + max_dim / 1.5,
            ),
            "filename": f"{base_filename}_orthogonal.png",
        },
    }

    # Calculate the position of the light source (always in the same relative position to the camera)
    light_position = (
        center_x + max_dim * 2,
        center_y + max_dim * 2,
        center_z + max_dim * 2,
    )

    # Render all views
    results = {}
    for view_name, view_info in views.items():
        output_path = os.path.join(output_dir, str(view_info["filename"]))
        camera_pos = cast(tuple, view_info["camera_position"])
        image = render_design(
            design_schema=design_schema,
            output_path=output_path,
            width=width,
            height=height,
            background_color=background_color,
            camera_position=camera_pos,
            look_at=center,
            light_position=light_position,
        )
        results[view_name] = image

    return results
