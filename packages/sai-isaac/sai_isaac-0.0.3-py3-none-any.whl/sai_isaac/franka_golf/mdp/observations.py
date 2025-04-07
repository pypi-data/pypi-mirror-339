# MDP for Franka Golf
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

from __future__ import annotations

import torch
from typing import TYPE_CHECKING

from isaaclab.assets import Articulation, RigidObject
from isaaclab.managers import SceneEntityCfg
from isaaclab.sensors import FrameTransformer
from isaaclab.assets import RigidObject
from isaaclab.managers import SceneEntityCfg
from isaacsim.core.prims import XFormPrim

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv

def hole_poses(env: ManagerBasedRLEnv) -> torch.Tensor:
    hole_poses = []
    for i in range(env.scene.num_envs):
        prim_path = f"World/envs/env_{i}/GolfCourse/worldBody/sites/hole_detector"
        hole = XFormPrim(prim_path, reset_xform_properties=False)
        hole_poses.append(hole.get_world_poses()[0][0])
    return torch.stack(hole_poses)


def object_position_in_world_frame(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """The position of the object in the robot's root frame."""
    object: RigidObject = env.scene[object_cfg.name]
    object_pos_w = object.data.root_pos_w[:, :3]
    return object_pos_w


def object_orientation_in_world_frame(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """The orientation of the object in the robot's root frame."""
    object: RigidObject = env.scene[object_cfg.name]
    object_quat_w = object.data.root_quat_w
    return object_quat_w


def object_velocity(
    env: ManagerBasedRLEnv,
    object_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """The velocity of the object in the robot's root frame."""
    object: RigidObject = env.scene[object_cfg.name]
    object_vel_w = object.data.root_lin_vel_w
    return object_vel_w


def rel_eef_object_pos(
    env: ManagerBasedRLEnv,
    obj_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """The relative position of the object in the robot's root frame."""
    obj: RigidObject = env.scene[obj_cfg.name]
    obj_pos_w = obj.data.root_pos_w
    eef_pos_w = env.scene["ee_frame"].data.target_pos_w[:, 0, :]
    return obj_pos_w - eef_pos_w


def rel_objects_pos(
    env: ManagerBasedRLEnv,
    obj1_cfg: SceneEntityCfg = SceneEntityCfg("object"),
    obj2_cfg: SceneEntityCfg = SceneEntityCfg("object"),
) -> torch.Tensor:
    """The relative position of obj2 in obj1's frame."""
    obj1: RigidObject = env.scene[obj1_cfg.name]
    obj2: RigidObject = env.scene[obj2_cfg.name]
    obj2_pos_w = obj2.data.root_pos_w
    obj1_pos_w = obj1.data.root_pos_w
    return obj2_pos_w - obj1_pos_w


def ee_frame_pos(
    env: ManagerBasedRLEnv, ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame")
) -> torch.Tensor:
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    ee_frame_pos = ee_frame.data.target_pos_w[:, 0, :] - env.scene.env_origins[:, 0:3]

    return ee_frame_pos


def ee_frame_quat(
    env: ManagerBasedRLEnv, ee_frame_cfg: SceneEntityCfg = SceneEntityCfg("ee_frame")
) -> torch.Tensor:
    ee_frame: FrameTransformer = env.scene[ee_frame_cfg.name]
    ee_frame_quat = ee_frame.data.target_quat_w[:, 0, :]

    return ee_frame_quat


def rel_eef_club_handle_pos(
    env: ManagerBasedRLEnv,
    club_handle_cfg: SceneEntityCfg = SceneEntityCfg("golf_club"),
) -> torch.Tensor:
    club = env.scene[club_handle_cfg.name]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_handle_pos = club.data.body_pos_w[:, club_grip_idx, :]
    eef_pos_w = env.scene["ee_frame"].data.target_pos_w[:, 0, :]
    return club_handle_pos - eef_pos_w


def rel_club_hitting_point_ball_pos(
    env: ManagerBasedRLEnv,
    club_hitting_point_cfg: SceneEntityCfg = SceneEntityCfg("golf_club"),
    ball_cfg: SceneEntityCfg = SceneEntityCfg("golf_ball"),
) -> torch.Tensor:
    club = env.scene[club_hitting_point_cfg.name]
    club_hitting_point_idx = club.find_bodies("head_link")[0][0]
    club_hitting_point_pos = club.data.body_pos_w[:, club_hitting_point_idx, :]
    ball: RigidObject = env.scene[ball_cfg.name]
    ball_pos = ball.data.root_pos_w
    return club_hitting_point_pos - ball_pos


def rel_ball_hole_pos(
    env: ManagerBasedRLEnv,
    ball_cfg: SceneEntityCfg = SceneEntityCfg("golf_ball"),
) -> torch.Tensor:
    ball: RigidObject = env.scene[ball_cfg.name]
    ball_pos = ball.data.root_pos_w
    hole_detector_pos = hole_poses(env)
    return ball_pos - hole_detector_pos


def gripper_pos(
    env: ManagerBasedRLEnv, robot_cfg: SceneEntityCfg = SceneEntityCfg("robot")
) -> torch.Tensor:
    robot: Articulation = env.scene[robot_cfg.name]
    finger_joint_1 = robot.data.joint_pos[:, -1].clone().unsqueeze(1)
    finger_joint_2 = -1 * robot.data.joint_pos[:, -2].clone().unsqueeze(1)

    return torch.cat((finger_joint_1, finger_joint_2), dim=1)
