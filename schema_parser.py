from dotenv import load_dotenv
import os
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def instruction_to_schema(prompt: str) -> str:
    SYSTEM_PROMPT = """
        The objective is to design a soft-slender robot that is composed of multiple pneumatic actuators. 
        Each actuator can exhibit a purely bending or purely twisting mode of continuous deformation. 
        The connections between actuators can be arranged serially or in parallel, resulting in more complex overall deformation.
        For each actuator placement, the framework should incorporate the starting-point and the end-point, and the expected maximum deformation. 
        If twisting actuator is used, specify if the deformation needs to be clock-wise or counter-clockwise. 
        If bending actuator is used, specify the direction of bending.
        If rods will be connected in parallel, specify which rod will be glued to which rod, and specify the location.
        If rods will be connected in serial, it is called ”connection link.” Each link can connect to multiple actuators,
        hence specify which actuator will be connected in which angle. For simplicity, ignore the volume of the link.
        Lastly, consider the actuation space. In most naive form, number of actuation is equal to the number of
        actuator, meaning each actuators are activated independently. It is possible to link the action for more than two
        actuators to reduce the action space. In the framework, it should be possible to specify this grouping actuations.
        Come up with a text-based grammar that can represent such design framework. 
        Given the manuscript, the entire robot should be manufacturable without missing information. 
        The language should be easily converted to mermaid syntax for visualization.

        Robot =
            "ROBOT" "{"
            ActuatorSection
            ConnectionSection
            ActuationSpaceSection
            "}";

        ActuatorSection =
            "ACTUATORS" "{"
            { ActuatorDefinition }
            "}";

        ConnectionSection =
            "CONNECTIONS" "{"
            { ConnectionDefinition }
            "}";

        ActuationSpaceSection =
            "ACTUATION_SPACE" "{"
            { ActuationGroupDefinition }
            "}";

        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        ;; Actuator Definitions
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

        ActuatorDefinition =
            "ACTUATOR" ActuatorID "{"
                "mode" ":" ActuatorMode ","
                "start_point" ":" Point3D ","
                "end_point" ":" Point3D ","
                "max_deformation" ":" Number,
                [ "direction" ":" Direction ]
            "}";

        ActuatorID = Identifier ;
            (* e.g. A1, A2, or a descriptive name like ActBend1 *)

        ActuatorMode = "bending" | "twisting" ;

        Point3D = "(" Number "," Number "," Number ")" ;
            (* or however you wish to represent the coordinate system *)

        Number = Digit { Digit | "." } ;
            (* simplified numeric representation; real number or int *)

        Direction =
              "clockwise"
            | "counter-clockwise"
            | "up"
            | "down"
            | "left"
            | "right"
            | Identifier ;
            (* Bending might have directions "up/down/left/right/etc."
            Twisting might be "clockwise" or "counter-clockwise."
            Or potentially other enumerations. *)

        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        ;; Connection Definitions
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

        ConnectionDefinition = ParallelConnection | SerialConnection ;

        (* Parallel connections: multiple rods are glued together. *)

        ParallelConnection =
            "PARALLEL" "{"
                { GlueSpec }
            "}";

        GlueSpec =
            "GLUE" ActuatorRef "TO" ActuatorRef "AT" LocationSpec ";";

        (* Serial connections: actuators meet at a ’link’ that sets
        angles or other constraints. We ignore link volume. *)

        SerialConnection =
            "LINK" LinkID "{"
                { ActuatorLinkSpec }
            "}";

        LinkID = Identifier ;

        ActuatorLinkSpec =
            "CONNECT" ActuatorRef "AT_ANGLE" Number ";";
        (* ’AT_ANGLE’ can be the angle of intersection or orientation *)

        (* Reference to an actuator by ID *)
        ActuatorRef = ActuatorID ;

        (* The location at which the rods are glued.
        Could be a coordinate or textual annotation. *)
        LocationSpec = Point3D | Identifier ;

        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
        ;; Actuation Space Definitions
        ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

        ActuationGroupDefinition =
            "GROUP" GroupID "{"
                { ActuatorRef }
            "}";

        GroupID = Identifier ;
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
