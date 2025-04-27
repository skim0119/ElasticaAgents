design_instructions = """
    The objective is to design a soft-slender robot that is composed of multiple pneumatic actuators. 
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
"""
