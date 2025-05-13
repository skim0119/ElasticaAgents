design_instructions = """
Your task is to design a soft slender robot and generate a design schema, "design.json".
If the file already exist, you can modify the file.

A soft-slender robot is composed of multiple pneumatic actuators. 
Each rod can exhibit a purely bending or purely twisting mode of continuous deformation. 
The connections between actuators can be arranged serially,resulting in more complex overall deformation.
For each rod placement, the framework should incorporate the starting-point and the end-point. 
Actuation can have bending and/or twisting (CW or CCW) mode.
If For each or combination of actuation type, actuation detail should be specified. For example, bending actuation should include bending direction and max bending magnitude. Twisting actuation should include twisting direction (CW or CCW) and max twisting magnitude.
The serial connection, or connection link, can be used to connect multiple actuators at different angles.
Branching can also be done by connecting multiple actuators at the same connection link.
Different actuation group can be specified to actuate different mode of actuation for each rod.
Lastly, consider the actuation space. In most naive form, number of actuation is equal to the number of
actuation modes in all rods, meaning each actuators are activated independently. It is possible to link the action for more than two
actuators to reduce the action space.

The design schema should be a JSON file that is following the schema:
{
  "actuators": [
    {
      "id": "actuator_1",
      "start_point": {"x": 0.0, "y": 0.0, "z": 0.0},
      "end_point": {"x": 0.0, "y": 0.0, "z": 0.5},
      "radius": 0.03,
      "orientation": {
        "d1": [1.0, 0.0, 0.0],
        "d2": [0.0, 1.0, 0.0],
        "d3": [0.0, 0.0, 1.0]
      }
    },
    {
      "id": "actuator_2",
      "start_point": {"x": 0.0, "y": 0.0, "z": 0.0},
      "end_point": {"x": 0.0, "y": 0.5, "z": 0.0},
      "radius": 0.03,
      "orientation": {
        "d1": [0.0, 0.0, 1.0],
        "d2": [1.0, 0.0, 0.0],
        "d3": [0.0, 1.0, 0.0]
      }
    }
  ]
}

You can use up to 10 actuators.
For each actuation, specify start and end points in 3D, radius of actuator, and the orientation.
Slender rod typically has a small radius compare to its length.

Do not iterate or call tools too much.
"""
