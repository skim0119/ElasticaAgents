import json
from elastica_agents.design_schema import RobotDesignSchema

path = "design1.json"
with open(path, "r") as f:
    robot_json = json.load(f)

try:
    validated_robot = RobotDesignSchema.model_validate(robot_json)
    print("Robot design validation successful!")
    print(
        f"Robot has {len(validated_robot.actuators)} actuators and {len(validated_robot.actuation_groups)} actuation groups"
    )
except Exception as e:
    print(f"Validation failed: {e}")
