# Franka Golf Environment
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

import os

from dataclasses import MISSING

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg, AssetBaseCfg
from isaaclab.envs import ManagerBasedRLEnvCfg
from isaaclab.managers import EventTermCfg as EventTerm
from isaaclab.managers import ObservationGroupCfg as ObsGroup
from isaaclab.managers import ObservationTermCfg as ObsTerm
from isaaclab.managers import RewardTermCfg as RewTerm
from isaaclab.managers import SceneEntityCfg
from isaaclab.managers import TerminationTermCfg as DoneTerm
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sensors import FrameTransformerCfg, CameraCfg
from isaaclab.utils import configclass
from isaaclab.assets import (
    ArticulationCfg,
    RigidObjectCfg,
    AssetBaseCfg,
)
from isaaclab.sim.spawners.from_files.from_files_cfg import GroundPlaneCfg
from isaaclab.sensors.frame_transformer.frame_transformer_cfg import OffsetCfg
from isaaclab_assets.robots.franka import (
    FRANKA_PANDA_CFG,
    FRANKA_PANDA_HIGH_PD_CFG,
)  # isort: skip
from isaaclab.markers.config import FRAME_MARKER_CFG  # isort: skip


from isaaclab.controllers.differential_ik_cfg import DifferentialIKControllerCfg
from isaaclab.envs.mdp.actions.actions_cfg import DifferentialInverseKinematicsActionCfg
from isaaclab.utils import configclass

from . import mdp

##
# Pre-defined configs
##

FRAME_MARKER_SMALL_CFG = FRAME_MARKER_CFG.copy()
FRAME_MARKER_SMALL_CFG.markers["frame"].scale = (0.10, 0.10, 0.10)
ASSETS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/assets"

FRANKA_POS = (1.2, -0.6, 0.0)
FRANKA_ROT = (0.7071, 0, 0, 0.7071)

##
# Scene definition
##


@configclass
class GolfSceneCfg(InteractiveSceneCfg):
    """Configuration for the cabinet scene with a robot and a cabinet.

    This is the abstract base implementation, the exact scene is defined in the derived classes
    which need to set the robot and end-effector frames
    """

    # robots, Will be populated by agent env cfg
    robot: ArticulationCfg = FRANKA_PANDA_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
    robot.spawn.semantic_tags = [("class", "robot")]
    robot.init_state.pos = FRANKA_POS
    robot.init_state.rot = FRANKA_ROT

    ee_frame: FrameTransformerCfg = MISSING

    # Set wrist camera
    wrist_cam = CameraCfg(
        prim_path="{ENV_REGEX_NS}/Robot/panda_hand/wrist_cam",
        update_period=0.0333,
        height=84,
        width=84,
        data_types=["rgb", "distance_to_image_plane"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=24.0,
            focus_distance=400.0,
            horizontal_aperture=20.955,
            clipping_range=(0.1, 1.0e5),
        ),
        offset=CameraCfg.OffsetCfg(
            pos=(0.025, 0.0, 0.0), rot=(0.707, 0.0, 0.0, 0.707), convention="ros"
        ),
    )

    # Set table view camera
    table_cam = CameraCfg(
        prim_path="{ENV_REGEX_NS}/table_cam",
        update_period=0.0333,
        height=84,
        width=84,
        data_types=["rgb", "distance_to_image_plane"],
        spawn=sim_utils.PinholeCameraCfg(
            focal_length=24.0,
            focus_distance=400.0,
            horizontal_aperture=20.955,
            clipping_range=(0.1, 1.0e5),
        ),
        offset=CameraCfg.OffsetCfg(
            pos=(1.0, 0.0, 0.33),
            rot=(-0.3799, 0.5963, 0.5963, -0.3799),
            convention="ros",
        ),
    )

    # golf course
    golf_course = AssetBaseCfg(
        prim_path="/World/envs/env_.*/GolfCourse",
        spawn=sim_utils.UsdFileCfg(
            usd_path=f"{ASSETS_DIR}/flat_golf_course.usd",
        ),
        init_state=AssetBaseCfg.InitialStateCfg(pos=(0.0, 0.0, 0.0)),
    )

    # golf club
    golf_club = ArticulationCfg(
        prim_path="{ENV_REGEX_NS}/GolfClub",
        spawn=sim_utils.UsdFileCfg(
            usd_path=f"{ASSETS_DIR}/golf_club.usd",
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.0),
            rot=(0.7071, 0.7071, 0.0, 0.0),
            joint_pos={},
            joint_vel={},
        ),
        actuators={},
    )

    # golf ball
    golf_ball = RigidObjectCfg(
        prim_path="/World/envs/env_.*/GolfBall",
        spawn=sim_utils.SphereCfg(
            radius=0.021336,
            visual_material=sim_utils.PreviewSurfaceCfg(diffuse_color=(1.0, 1.0, 1.0)),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                max_depenetration_velocity=5.0,
                kinematic_enabled=False,
                enable_gyroscopic_forces=True,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=0,
                sleep_threshold=0.005,
                stabilization_threshold=0.0025,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(),
            physics_material=sim_utils.RigidBodyMaterialCfg(
                static_friction=0.5, dynamic_friction=0.5, restitution=0.7
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=0.04593),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.7, 0.0, 0.0203),
            rot=(1.0, 0.0, 0.0, 0.0),
        ),
    )

    # plane
    plane = AssetBaseCfg(
        prim_path="/World/GroundPlane",
        init_state=AssetBaseCfg.InitialStateCfg(pos=[0, 0, -1.05]),
        spawn=GroundPlaneCfg(),
    )

    # lights
    light = AssetBaseCfg(
        prim_path="/World/light",
        spawn=sim_utils.DistantLightCfg(color=(0.75, 0.75, 0.75), intensity=2000.0),
    )


##
# MDP settings
##


@configclass
class EventCfg:
    """Configuration for events."""

    init_franka_arm_pose = EventTerm(
        func=mdp.set_default_joint_pose,
        mode="startup",
        params={
            "default_pose": [
                0.0444,
                -0.1894,
                -0.1107,
                -2.5148,
                0.0044,
                2.3775,
                0.6952,
                0.0400,
                0.0400,
            ],
        },
    )

    randomize_franka_joint_state = EventTerm(
        func=mdp.randomize_joint_by_gaussian_offset,
        mode="reset",
        params={
            "mean": 0.0,
            "std": 0.02,
            "asset_cfg": SceneEntityCfg("robot"),
        },
    )

    randomize_club_position = EventTerm(
        func=mdp.randomize_object_pose,
        mode="reset",
        params={
            "pose_range": {
                "x": (1.0, 1.3),
                "y": (0.0, 0.25),
                "z": (0.0213, 0.0213),
                "roll": (1.57, 1.57),
                "pitch": (0.0, 0.0),
                "yaw": (3.14, 3.14),
            },
            "asset_cfgs": [SceneEntityCfg("golf_club")],
        },
    )


@configclass
class ActionsCfg:
    """Action specifications for the MDP."""

    arm_action: mdp.JointPositionActionCfg = mdp.JointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_joint.*"],
        scale=0.5,
        use_default_offset=True,
    )
    gripper_action: mdp.BinaryJointPositionActionCfg = mdp.BinaryJointPositionActionCfg(
        asset_name="robot",
        joint_names=["panda_finger.*"],
        open_command_expr={"panda_finger_.*": 0.04},
        close_command_expr={"panda_finger_.*": 0.0},
    )


@configclass
class ObservationsCfg:
    """Observation specifications for the MDP."""

    @configclass
    class PolicyCfg(ObsGroup):
        """Observations for policy group with state values."""

        actions = ObsTerm(func=mdp.last_action)
        joint_pos = ObsTerm(func=mdp.joint_pos_rel)
        joint_vel = ObsTerm(func=mdp.joint_vel_rel)
        eef_pos = ObsTerm(func=mdp.ee_frame_pos)
        eef_quat = ObsTerm(func=mdp.ee_frame_quat)
        gripper_pos = ObsTerm(func=mdp.gripper_pos)

        ball_positions = ObsTerm(
            func=mdp.object_position_in_world_frame,
            params={"object_cfg": SceneEntityCfg("golf_ball")},
        )

        ball_velocities = ObsTerm(
            func=mdp.object_velocity,
            params={"object_cfg": SceneEntityCfg("golf_ball")},
        )

        club_pos = ObsTerm(
            func=mdp.object_position_in_world_frame,
            params={"object_cfg": SceneEntityCfg("golf_club")},
        )

        club_quat = ObsTerm(
            func=mdp.object_orientation_in_world_frame,
            params={"object_cfg": SceneEntityCfg("golf_club")},
        )

        rel_eef_club_handle_pos = ObsTerm(
            func=mdp.rel_eef_club_handle_pos,
        )

        rel_club_hitting_point_ball_pos = ObsTerm(
            func=mdp.rel_club_hitting_point_ball_pos,
        )

        rel_ball_hole_pos = ObsTerm(
            func=mdp.rel_ball_hole_pos,
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = False

    @configclass
    class RGBCameraPolicyCfg(ObsGroup):
        """Observations for policy group with RGB images."""

        table_cam = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg("table_cam"),
                "data_type": "rgb",
                "normalize": False,
            },
        )
        wrist_cam = ObsTerm(
            func=mdp.image,
            params={
                "sensor_cfg": SceneEntityCfg("wrist_cam"),
                "data_type": "rgb",
                "normalize": False,
            },
        )

        def __post_init__(self):
            self.enable_corruption = False
            self.concatenate_terms = False

    # observation groups
    policy: PolicyCfg = PolicyCfg()
    rgb_camera: RGBCameraPolicyCfg = RGBCameraPolicyCfg()


@configclass
class RewardsCfg:
    """Reward terms for the MDP."""

    # # 1. Approach the club grip
    approach_ee_club_grip = RewTerm(
        func=mdp.approach_ee_club_grip, weight=0.8, params={"threshold": 0.1}
    )
    align_ee_club_grip = RewTerm(func=mdp.align_ee_club_grip, weight=0.7)

    # # 2. Grasp the club grip
    approach_gripper_club_grip = RewTerm(
        func=mdp.approach_gripper_club_grip, weight=0.7, params={"offset": 0.04}
    )
    align_grasp_around_club_grip = RewTerm(
        func=mdp.align_grasp_around_club_grip, weight=0.9
    )
    grasp_club_grip = RewTerm(
        func=mdp.grasp_club_grip,
        weight=1.0,
        params={
            "threshold": 0.03,
            "open_joint_pos": 0.04,
            "asset_cfg": SceneEntityCfg("robot", joint_names=["panda_finger_.*"]),
        },
    )

    # 3. Lift the club grip
    lifting_club_grip = RewTerm(
        func=mdp.lifting_club_grip,
        weight=1.5,
        params={
            "z_threshold": 0.05,
        },
    )

    # 4. Approach golf hitting point to the ball
    approach_hitting_point_ball = RewTerm(
        func=mdp.approach_hitting_point_ball, weight=2.0
    )

    # 5. Approach ball to the hole
    approach_ball_hole = RewTerm(func=mdp.approach_ball_hole, weight=3.0)

    # 6. Penalize actions for cosmetic reasons
    action_rate_l2 = RewTerm(func=mdp.action_rate_l2, weight=-1e-2)
    joint_vel = RewTerm(func=mdp.joint_vel_l2, weight=-0.0001)


@configclass
class TerminationsCfg:
    """Termination terms for the MDP."""

    time_out = DoneTerm(func=mdp.time_out, time_out=True)

    success = is_ball_in_hole = DoneTerm(func=mdp.is_ball_in_hole)


##
# Environment configuration
##


@configclass
class FrankaGolfEnvCfg(ManagerBasedRLEnvCfg):
    """Configuration for the cabinet environment."""

    # Scene settings
    scene: GolfSceneCfg = GolfSceneCfg(
        num_envs=4096, env_spacing=5.0, replicate_physics=False
    )
    # Basic settings
    observations: ObservationsCfg = ObservationsCfg()
    actions: ActionsCfg = ActionsCfg()
    # MDP settings
    rewards: RewardsCfg = RewardsCfg()
    terminations: TerminationsCfg = TerminationsCfg()
    events: EventCfg = EventCfg()

    def __post_init__(self):
        """Post initialization."""
        # general settings
        self.decimation = 5
        self.episode_length_s = 30.0
        # simulation settings
        self.sim.dt = 0.01  # 120Hz
        self.sim.render_interval = self.decimation
        self.sim.physx.bounce_threshold_velocity = 0.2
        self.sim.physx.bounce_threshold_velocity = 0.01
        self.sim.physx.friction_correlation_distance = 0.00625
        self.sim.physx.gpu_found_lost_aggregate_pairs_capacity = 1024 * 1024 * 4
        self.sim.physx.gpu_total_aggregate_pairs_capacity = 16 * 1024

        self.scene.ee_frame = FrameTransformerCfg(
            prim_path="{ENV_REGEX_NS}/Robot/panda_link0",
            debug_vis=False,
            visualizer_cfg=FRAME_MARKER_CFG.replace(
                prim_path="/Visuals/FrameTransformer"
            ).replace(markers={"frame": {"scale": (0.1, 0.1, 0.1)}}),
            target_frames=[
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_hand",
                    name="end_effector",
                    offset=OffsetCfg(
                        pos=[0.0, 0.0, 0.1034],
                    ),
                ),
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_rightfinger",
                    name="tool_rightfinger",
                    offset=OffsetCfg(
                        pos=(0.0, 0.0, 0.046),
                    ),
                ),
                FrameTransformerCfg.FrameCfg(
                    prim_path="{ENV_REGEX_NS}/Robot/panda_leftfinger",
                    name="tool_leftfinger",
                    offset=OffsetCfg(
                        pos=(0.0, 0.0, 0.046),
                    ),
                ),
            ],
        )


@configclass
class FrankaGolfEnvCfg_IKRel(FrankaGolfEnvCfg):
    """Configuration for the Franka Golf environment with relative IK."""

    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        self.scene.robot = FRANKA_PANDA_HIGH_PD_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )

        self.scene.robot.init_state.pos = FRANKA_POS
        self.scene.robot.init_state.rot = FRANKA_ROT

        # Set actions for the specific robot type (franka)
        self.actions.arm_action = DifferentialInverseKinematicsActionCfg(
            asset_name="robot",
            joint_names=["panda_joint.*"],
            body_name="panda_hand",
            controller=DifferentialIKControllerCfg(
                command_type="pose", use_relative_mode=True, ik_method="dls"
            ),
            scale=0.5,
            body_offset=DifferentialInverseKinematicsActionCfg.OffsetCfg(
                pos=[0.0, 0.0, 0.107]
            ),
        )


@configclass
class FrankaGolfEnvCfg_IKAbs(FrankaGolfEnvCfg):
    """Configuration for the Franka Golf environment with absolute IK."""

    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        self.scene.robot = FRANKA_PANDA_HIGH_PD_CFG.replace(
            prim_path="{ENV_REGEX_NS}/Robot"
        )

        self.scene.robot.init_state.pos = FRANKA_POS
        self.scene.robot.init_state.rot = FRANKA_ROT

        self.actions.arm_action = DifferentialInverseKinematicsActionCfg(
            asset_name="robot",
            joint_names=["panda_joint.*"],
            body_name="panda_hand",
            controller=DifferentialIKControllerCfg(
                command_type="pose", use_relative_mode=False, ik_method="dls"
            ),
            body_offset=DifferentialInverseKinematicsActionCfg.OffsetCfg(
                pos=[0.0, 0.0, 0.107]
            ),
        )
