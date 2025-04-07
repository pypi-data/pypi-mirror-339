# Franka Golf Direct Environment
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

from __future__ import annotations
import os

import torch

from isaacsim.core.utils.stage import get_current_stage
from isaacsim.core.utils.torch.transformations import tf_combine, tf_inverse
from pxr import UsdGeom

import isaaclab.sim as sim_utils
from isaaclab.actuators.actuator_cfg import ImplicitActuatorCfg
from isaaclab.assets import (
    ArticulationCfg,
    RigidObjectCfg,
    AssetBaseCfg,
)
from isaaclab.envs import DirectRLEnv, DirectRLEnvCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.utils import configclass
from isaaclab.utils.assets import ISAAC_NUCLEUS_DIR

ASSETS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/assets"


@configclass
class GolfSceneCfg(InteractiveSceneCfg):
    # robot
    robot = ArticulationCfg(
        prim_path="/World/envs/env_.*/Robot",
        spawn=sim_utils.UsdFileCfg(
            usd_path=f"{ISAAC_NUCLEUS_DIR}/Robots/Franka/franka_instanceable.usd",
            activate_contact_sensors=False,
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                max_depenetration_velocity=5.0,
            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=12,
                solver_velocity_iteration_count=1,
            ),
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            joint_pos={
                "panda_joint1": 0.0,
                "panda_joint2": -0.3,
                "panda_joint3": 0.0,
                "panda_joint4": -1.8,
                "panda_joint5": 0.0,
                "panda_joint6": 1.5,
                "panda_joint7": 0.8,
                "panda_finger_joint.*": 0.02,
            },
            pos=(0.0, 0.0, 0.0),
            rot=(0.7071, 0, 0, 0.7071),
        ),
        actuators={
            "panda_shoulder": ImplicitActuatorCfg(
                joint_names_expr=["panda_joint[1-4]"],
                effort_limit=87.0,
                velocity_limit=2.175,
                stiffness=80.0,
                damping=4.0,
            ),
            "panda_forearm": ImplicitActuatorCfg(
                joint_names_expr=["panda_joint[5-7]"],
                effort_limit=12.0,
                velocity_limit=2.61,
                stiffness=80.0,
                damping=4.0,
            ),
            "panda_hand": ImplicitActuatorCfg(
                joint_names_expr=["panda_finger_joint.*"],
                effort_limit=200.0,
                velocity_limit=0.2,
                stiffness=2e3,
                damping=1e2,
            ),
        },
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
    golf_club = RigidObjectCfg(
        prim_path="/World/envs/env_.*/GolfClub",
        spawn=sim_utils.UsdFileCfg(
            usd_path=f"{ASSETS_DIR}/golf_club.usd",
            activate_contact_sensors=False,
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
        ),
        init_state=RigidObjectCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.0),
            rot=(0.7071, 0, 0, 0.7071),
        ),
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
            pos=(0.0, 0.0, 0.0213),
            rot=(0.0, 0.0, 0.0, 1.0),
        ),
    )

    # terrain
    terrain = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        collision_group=-1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="multiply",
            restitution_combine_mode="multiply",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
    )

    # light
    distant_light = AssetBaseCfg(
        prim_path="/World/distant_light",
        spawn=sim_utils.DistantLightCfg(color=(1.0, 1.0, 1.0), intensity=2000.0),
    )


@configclass
class FrankaGolfDirectEnvCfg(DirectRLEnvCfg):
    # env
    episode_length_s = 8.3333  # 500 timesteps
    decimation = 2
    action_space = 9
    observation_space = 34
    state_space = 0

    action_scale = 7.5
    dof_velocity_scale = 0.1

    # simulation
    sim: SimulationCfg = SimulationCfg(
        dt=1 / 120,
        render_interval=decimation,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="multiply",
            restitution_combine_mode="multiply",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
    )

    # scene
    scene: GolfSceneCfg = GolfSceneCfg(
        num_envs=4096, env_spacing=5.0, replicate_physics=True
    )

    # Reward scales
    ball_hole_distance_reward_scale = 5.0
    action_penalty_scale = 0.05
    hole_reward = 50.0
    club_in_gripper_reward_scale = 20.0

    # Environment settings
    random_ball_placement = False
    terrain_type = "flat"

    ball_in_hole_threshold = 0.01

    robot_init_global_pos = (0.75, -0.6, 0.021)
    ball_init_global_pos = (0.75, 0.0, 0.021)
    club_init_global_pos = (0.75, -0.2, 0.021)


class FrankaGolfDirectEnv(DirectRLEnv):
    # pre-physics step calls
    #   |-- _pre_physics_step(action)
    #   |-- _apply_action()
    # post-physics step calls
    #   |-- _get_dones()
    #   |-- _get_rewards()
    #   |-- _reset_idx(env_ids)
    #   |-- _get_observations()

    def __init__(
        self, cfg: FrankaGolfDirectEnvCfg, render_mode: str | None = None, **kwargs
    ):
        super().__init__(cfg, render_mode, **kwargs)

        self._robot = self.scene.articulations["robot"]
        self._golf_club = self.scene.rigid_objects["golf_club"]
        self._golf_course = self.scene.extras["golf_course"]
        self._golf_ball = self.scene.rigid_objects["golf_ball"]

        def get_env_local_pose(
            env_pos: torch.Tensor, xformable: UsdGeom.Xformable, device: torch.device
        ):
            world_transform = xformable.ComputeLocalToWorldTransform(0)
            world_pos = world_transform.ExtractTranslation()
            world_quat = world_transform.ExtractRotationQuat()
            px = world_pos[0] - env_pos[0]
            py = world_pos[1] - env_pos[1]
            pz = world_pos[2] - env_pos[2]
            qx = world_quat.imaginary[0]
            qy = world_quat.imaginary[1]
            qz = world_quat.imaginary[2]
            qw = world_quat.real
            return torch.tensor([px, py, pz, qw, qx, qy, qz], device=device)

        self.dt = self.cfg.sim.dt * self.cfg.decimation

        self.robot_dof_lower_limits = self._robot.data.soft_joint_pos_limits[
            0, :, 0
        ].to(device=self.device)
        self.robot_dof_upper_limits = self._robot.data.soft_joint_pos_limits[
            0, :, 1
        ].to(device=self.device)

        self.robot_dof_speed_scales = torch.ones_like(self.robot_dof_lower_limits)
        self.robot_dof_speed_scales[
            self._robot.find_joints("panda_finger_joint1")[0]
        ] = 0.1
        self.robot_dof_speed_scales[
            self._robot.find_joints("panda_finger_joint2")[0]
        ] = 0.1

        self.robot_dof_targets = torch.zeros(
            (self.num_envs, self._robot.num_joints), device=self.device
        )

        stage = get_current_stage()
        hand_pose = get_env_local_pose(
            self.scene.env_origins[0],
            UsdGeom.Xformable(
                stage.GetPrimAtPath("/World/envs/env_0/Robot/panda_link7")
            ),
            self.device,
        )
        lfinger_pose = get_env_local_pose(
            self.scene.env_origins[0],
            UsdGeom.Xformable(
                stage.GetPrimAtPath("/World/envs/env_0/Robot/panda_leftfinger")
            ),
            self.device,
        )
        rfinger_pose = get_env_local_pose(
            self.scene.env_origins[0],
            UsdGeom.Xformable(
                stage.GetPrimAtPath("/World/envs/env_0/Robot/panda_rightfinger")
            ),
            self.device,
        )

        finger_pose = torch.zeros(7, device=self.device)
        finger_pose[0:3] = (lfinger_pose[0:3] + rfinger_pose[0:3]) / 2.0
        finger_pose[3:7] = lfinger_pose[3:7]
        hand_pose_inv_rot, hand_pose_inv_pos = tf_inverse(
            hand_pose[3:7], hand_pose[0:3]
        )

        robot_local_grasp_pose_rot, robot_local_pose_pos = tf_combine(
            hand_pose_inv_rot, hand_pose_inv_pos, finger_pose[3:7], finger_pose[0:3]
        )
        robot_local_pose_pos += torch.tensor([0.0, 0.0, 0.2], device=self.device)
        self.robot_local_grasp_pos = robot_local_pose_pos.repeat((self.num_envs, 1))
        self.robot_local_grasp_rot = robot_local_grasp_pose_rot.repeat(
            (self.num_envs, 1)
        )

        self.gripper_forward_axis = torch.tensor(
            [0, 0, 1], device=self.device, dtype=torch.float32
        ).repeat((self.num_envs, 1))
        self.gripper_up_axis = torch.tensor(
            [0, 1, 0], device=self.device, dtype=torch.float32
        ).repeat((self.num_envs, 1))

        self.hand_link_idx = self._robot.find_bodies("panda_link7")[0][0]
        self.left_finger_link_idx = self._robot.find_bodies("panda_leftfinger")[0][0]
        self.right_finger_link_idx = self._robot.find_bodies("panda_rightfinger")[0][0]

        self.robot_grasp_rot = torch.zeros((self.num_envs, 4), device=self.device)
        self.robot_grasp_pos = torch.zeros((self.num_envs, 3), device=self.device)

        hole_detector = stage.GetPrimAtPath(
            "/World/envs/env_0/GolfCourse/worldBody/sites/hole_detector/hole_detector"
        )
        if hole_detector:
            self.hole_position = get_env_local_pose(
                self.scene.env_origins[0],
                UsdGeom.Xformable(hole_detector),
                self.device,
            )[:3].repeat((self.num_envs, 1))
        else:
            # Fallback to default position
            self.hole_position = self.scene.env_origins + torch.tensor(
                [1.0, 0.0, 0.0], device=self.device
            )
            self.hole_position = self.hole_position.repeat((self.num_envs, 1))

        # Initialize ball_to_hole_dist for reward calculations
        self.ball_to_hole_dist = torch.zeros(self.num_envs, device=self.device)

        self.robot_init_state = self._robot.data.default_root_state.clone()
        self.robot_init_state[:, :3] = (
            torch.tensor(self.cfg.robot_init_global_pos, device=self.device)
            + self.scene.env_origins
        )

        self.golf_ball_init_state = self._golf_ball.data.default_root_state.clone()
        self.golf_ball_init_state[:, :3] = (
            torch.tensor(self.cfg.ball_init_global_pos, device=self.device)
            + self.scene.env_origins
        )

        self.golf_club_init_state = self._golf_club.data.default_root_state.clone()
        self.golf_club_init_state[:, :3] = (
            torch.tensor(self.cfg.club_init_global_pos, device=self.device)
            + self.scene.env_origins
        )

    def _pre_physics_step(self, actions: torch.Tensor):
        self.actions = actions.clone().clamp(-1.0, 1.0)
        targets = (
            self.robot_dof_targets
            + self.robot_dof_speed_scales
            * self.dt
            * self.actions
            * self.cfg.action_scale
        )
        self.robot_dof_targets[:] = torch.clamp(
            targets, self.robot_dof_lower_limits, self.robot_dof_upper_limits
        )

    def _apply_action(self):
        self._robot.set_joint_position_target(self.robot_dof_targets)

    def _get_dones(self) -> tuple[torch.Tensor, torch.Tensor]:
        ball_in_hole = self.ball_to_hole_dist < self.cfg.ball_in_hole_threshold
        truncated = self.episode_length_buf >= self.max_episode_length - 1
        return ball_in_hole, truncated

    def _get_rewards(self) -> torch.Tensor:
        self._compute_intermediate_values()

        # Get ball position and update distance to hole
        ball_pos = self._golf_ball.data.root_pos_w[:, :3] - self.scene.env_origins
        self.ball_to_hole_dist = torch.norm(self.hole_position - ball_pos, dim=1)

        # Distance-based reward (negative, as closer is better)
        distance_reward = (
            -self.ball_to_hole_dist * self.cfg.ball_hole_distance_reward_scale
        )

        # Penalty for large actions (to encourage smooth control)
        action_penalty = (
            torch.sum(self.actions**2, dim=1) * self.cfg.action_penalty_scale
        )

        # Bonus reward for getting ball in hole
        ball_in_hole = (
            self.ball_to_hole_dist < self.cfg.ball_in_hole_threshold
        ).float()
        hole_reward = ball_in_hole * self.cfg.hole_reward

        # Reward for club in gripper
        club_in_gripper = (
            self._robot.data.body_pos_w[:, self.hand_link_idx]
            - self._golf_club.data.root_pos_w
        )
        club_in_gripper_reward = (
            torch.sum(club_in_gripper**2, dim=1) * self.cfg.club_in_gripper_reward_scale
        )

        # Total reward
        return distance_reward - action_penalty + hole_reward + club_in_gripper_reward

    def _reset_idx(self, env_ids: torch.Tensor | None):
        super()._reset_idx(env_ids)

        # robot state
        joint_pos = self._robot.data.default_joint_pos[env_ids]
        joint_pos = torch.clamp(
            joint_pos, self.robot_dof_lower_limits, self.robot_dof_upper_limits
        )
        joint_vel = torch.zeros_like(joint_pos)
        self._robot.set_joint_position_target(joint_pos, env_ids=env_ids)
        self._robot.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)

        self._robot.write_root_state_to_sim(self.robot_init_state, env_ids=env_ids)

        # Set ball position based on random_ball_placement flag
        if self.cfg.random_ball_placement:
            # Random position within defined boundaries
            ball_pos_xy = (
                torch.rand((len(env_ids), 2), device=self.device) * 0.4
                - 0.2
                + self.golf_ball_init_state[:, :2]
            )
            ball_pos = torch.cat(
                [ball_pos_xy, self.golf_ball_init_state[:, 2].unsqueeze(-1)], dim=1
            )
        else:
            # Fixed position from config
            ball_pos = torch.tensor(
                self.cfg.ball_init_global_pos, device=self.device
            ).repeat(len(env_ids), 1)

        # Apply env_origins offset to get world position
        world_ball_pos = self.scene.env_origins[env_ids] + ball_pos
        world_ball_rot = torch.tensor([0.0, 0.0, 0.0, 1.0], device=self.device).repeat(
            len(env_ids), 1
        )
        world_ball_pose = torch.cat([world_ball_pos, world_ball_rot], dim=1)

        self._golf_ball.write_root_pose_to_sim(world_ball_pose, env_ids=env_ids)

        self._golf_club.write_root_state_to_sim(
            self.golf_club_init_state, env_ids=env_ids
        )

        # Need to refresh the intermediate values so that _get_observations() can use the latest values
        self._compute_intermediate_values(env_ids)

    def _get_observations(self) -> dict:
        # Get scaled joint positions
        dof_pos_scaled = (
            2.0
            * (self._robot.data.joint_pos - self.robot_dof_lower_limits)
            / (self.robot_dof_upper_limits - self.robot_dof_lower_limits)
            - 1.0
        )

        # Get ball position and velocity
        ball_pos = self._golf_ball.data.root_pos_w
        ball_vel = self._golf_ball.data.root_lin_vel_w

        ball_pos_local = ball_pos - self.scene.env_origins

        club_pos = self._golf_club.data.root_pos_w
        club_rot = self._golf_club.data.root_quat_w
        club_pos_local = club_pos - self.scene.env_origins

        # Calculate vector from ball to hole
        to_target = self.hole_position - ball_pos_local

        # Calculate distance from ball to hole for reward computation
        self.ball_to_hole_dist = torch.norm(to_target, dim=1)

        # Combine all observations as per observation space definition
        obs = torch.cat(
            (
                dof_pos_scaled,  # 9 joint positions
                self._robot.data.joint_vel
                * self.cfg.dof_velocity_scale,  # 9 joint velocities
                to_target,  # 3 vector to target
                ball_pos_local,  # 3 ball position
                ball_vel,  # 3 ball velocity
                club_pos_local,  # 3 club position
                club_rot,  # 4 club rotation
            ),
            dim=-1,
        )

        # Clamp to reasonable values
        return {"policy": torch.clamp(obs, -5.0, 5.0)}

    def _compute_intermediate_values(self, env_ids: torch.Tensor | None = None):
        if env_ids is None:
            env_ids = self._robot._ALL_INDICES
        hand_pos = self._robot.data.body_pos_w[env_ids, self.hand_link_idx]
        hand_rot = self._robot.data.body_quat_w[env_ids, self.hand_link_idx]
        (
            self.robot_grasp_rot[env_ids],
            self.robot_grasp_pos[env_ids],
        ) = self._compute_grasp_transforms(
            hand_rot,
            hand_pos,
            self.robot_local_grasp_rot[env_ids],
            self.robot_local_grasp_pos[env_ids],
        )

    def _compute_grasp_transforms(
        self,
        hand_rot,
        hand_pos,
        franka_local_grasp_rot,
        franka_local_grasp_pos,
    ):
        global_franka_rot, global_franka_pos = tf_combine(
            hand_rot, hand_pos, franka_local_grasp_rot, franka_local_grasp_pos
        )
        return (
            global_franka_rot,
            global_franka_pos,
        )
