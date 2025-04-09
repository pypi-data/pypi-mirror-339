import os

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.utils.assets import ISAACLAB_NUCLEUS_DIR

##
# Configuration
##

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/assets"

COBOT_CFG = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=f"{ASSETS_DIR}/flattened_visual_jetcobot.usd",
        activate_contact_sensors=False,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True, solver_position_iteration_count=8, solver_velocity_iteration_count=0
        ),
        # collision_props=sim_utils.CollisionPropertiesCfg(contact_offset=0.005, rest_offset=0.0),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        joint_pos={
            "one_Joint": 0.0,
            "two_Joint": 0.0,
            "three_Joint": 0.0,
            "four_Joint": 0.0,
            "five_Joint": 0.0,
            "six_Joint": 0.0,
            "gripper_base_to_gripper_left2": 0.0,
            "gripper_base_to_gripper_right2": 0.0,
            "gripper_base_to_gripper_right3": 0.0,
            "gripper_right3_to_gripper_right1": 0.0,
            "gripper_controller": 0.0,
            "gripper_left3_to_gripper_left1": 0.0,
        },
    ),
    actuators={
        "all_actuators": ImplicitActuatorCfg(
            joint_names_expr=[
                "one_Joint",
                "two_Joint",
                "three_Joint",
                "four_Joint",
                "five_Joint",
                "six_Joint",
                "gripper_base_to_gripper_left2",
                "gripper_base_to_gripper_right2",
                "gripper_base_to_gripper_right3",
                "gripper_right3_to_gripper_right1",
                "gripper_controller",
                "gripper_left3_to_gripper_left1",
            ],
            effort_limit=1000.0,
            velocity_limit=10.0,
            stiffness=1.74533,
            damping=0.01745,
        ),
    },
)
