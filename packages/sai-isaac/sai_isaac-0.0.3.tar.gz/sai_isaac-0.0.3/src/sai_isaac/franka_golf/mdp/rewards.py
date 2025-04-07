# MDP for Franka Golf
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

from __future__ import annotations

from .observations import hole_poses
import torch
from typing import TYPE_CHECKING

from isaaclab.managers import SceneEntityCfg
from isaaclab.utils.math import matrix_from_quat

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def align_grasp_around_club_grip(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for correct hand orientation around the club grip.

    Encourages the fingers to be positioned on opposite sides of the club grip,
    with a continuous reward gradient.
    """
    # Target object position
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_pos = club.data.body_pos_w[:, club_grip_idx, :]
    club_grip_quat = club.data.body_quat_w[:, club_grip_idx, :]

    # Get club orientation vectors
    club_rot_mat = matrix_from_quat(club_grip_quat)
    club_long_axis = club_rot_mat[..., 2]  # Assuming z is along the grip length

    # Fingertips position
    ee_fingertips_w = env.scene["ee_frame"].data.target_pos_w[..., 1:, :]
    lfinger_pos = ee_fingertips_w[..., 0, :]
    rfinger_pos = ee_fingertips_w[..., 1, :]

    # Vector from grip to each finger
    lvec = lfinger_pos - club_grip_pos
    rvec = rfinger_pos - club_grip_pos

    # Project vectors onto plane perpendicular to club's long axis
    l_dot_long = (
        torch.bmm(lvec.unsqueeze(1), club_long_axis.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )
    r_dot_long = (
        torch.bmm(rvec.unsqueeze(1), club_long_axis.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )

    l_proj = lvec - l_dot_long.unsqueeze(-1) * club_long_axis
    r_proj = rvec - r_dot_long.unsqueeze(-1) * club_long_axis

    # Find a reference vector perpendicular to club_long_axis
    # Using cross product with world up vector for stability
    world_up = torch.tensor([0.0, 0.0, 1.0], device=club_long_axis.device).repeat(
        club_long_axis.shape[0], 1
    )
    side_dir = torch.cross(club_long_axis, world_up, dim=-1)
    side_dir_norm = torch.norm(side_dir, dim=-1, keepdim=True)
    # Handle case where club is parallel to world up
    side_dir = torch.where(
        side_dir_norm > 1e-6,
        side_dir / side_dir_norm,
        torch.tensor([1.0, 0.0, 0.0], device=side_dir.device),
    )

    # Check if fingers are on opposite sides
    l_side = (
        torch.bmm(l_proj.unsqueeze(1), side_dir.unsqueeze(-1)).squeeze(-1).squeeze(-1)
    )
    r_side = (
        torch.bmm(r_proj.unsqueeze(1), side_dir.unsqueeze(-1)).squeeze(-1).squeeze(-1)
    )

    # Reward components:
    # 1. Fingers should be on opposite sides (l_side and r_side should have opposite signs)
    opposite_sides = -l_side * r_side
    opposite_sides_reward = torch.sigmoid(
        opposite_sides * 5
    )  # Smooth 0 to 1 transition

    # 2. Fingers should be at similar distances from the grip axis
    l_dist_from_axis = torch.norm(l_proj, dim=-1)
    r_dist_from_axis = torch.norm(r_proj, dim=-1)
    balanced_dist = 1.0 - torch.abs(l_dist_from_axis - r_dist_from_axis) / (
        l_dist_from_axis + r_dist_from_axis + 1e-6
    )

    # 3. Fingers should be close to the grip (but not too close)
    ideal_distance = 0.04  # This should be the radius of the grip plus a small margin
    l_dist_reward = torch.exp(-10.0 * torch.abs(l_dist_from_axis - ideal_distance))
    r_dist_reward = torch.exp(-10.0 * torch.abs(r_dist_from_axis - ideal_distance))

    # 4. Fingers should be at similar heights along the club grip
    similar_height = 1.0 - torch.abs(l_dot_long - r_dot_long) / (
        torch.abs(l_dot_long) + torch.abs(r_dot_long) + 1e-6
    )

    # Combine rewards with weighting
    return (
        0.4 * opposite_sides_reward
        + 0.2 * balanced_dist
        + 0.2 * (l_dist_reward + r_dist_reward) / 2.0
        + 0.2 * similar_height
    )


def approach_ee_club_grip(env: ManagerBasedRLEnv, threshold: float) -> torch.Tensor:
    """Reward the robot for reaching the club grip using inverse-square law with smooth transition."""
    ee_tcp_pos = env.scene["ee_frame"].data.target_pos_w[..., 0, :]
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_pos = club.data.body_pos_w[:, club_grip_idx, :]

    # Compute the distance of the end-effector to the handle
    distance = torch.norm(club_grip_pos - ee_tcp_pos, dim=-1, p=2)

    # Base reward using inverse-square law
    reward = 1.0 / (1.0 + distance**2)
    reward = torch.pow(reward, 2)

    # Smooth transition at threshold using sigmoid instead of binary threshold
    transition = torch.sigmoid(
        -10 * (distance - threshold)
    )  # Smooth 1 to 0 around threshold
    bonus_factor = 1.0 + transition

    return bonus_factor * reward


def align_ee_club_grip(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for aligning the end-effector with the club grip."""
    ee_tcp_quat = env.scene["ee_frame"].data.target_quat_w[..., 0, :]
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_quat = club.data.body_quat_w[:, club_grip_idx, :]

    ee_tcp_rot_mat = matrix_from_quat(ee_tcp_quat)
    club_grip_rot_mat = matrix_from_quat(club_grip_quat)

    # Get current axes
    club_grip_x, club_grip_y = club_grip_rot_mat[..., 0], club_grip_rot_mat[..., 1]
    ee_tcp_x, ee_tcp_z = ee_tcp_rot_mat[..., 0], ee_tcp_rot_mat[..., 2]

    # Calculate alignments (dot products)
    align_z = (
        torch.bmm(ee_tcp_z.unsqueeze(1), -club_grip_x.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )
    align_x = (
        torch.bmm(ee_tcp_x.unsqueeze(1), -club_grip_y.unsqueeze(-1))
        .squeeze(-1)
        .squeeze(-1)
    )

    # Use smooth function instead of sign * squared
    # Convert dot product (-1 to 1) to a 0 to 1 reward
    align_z_reward = (align_z + 1) / 2
    align_x_reward = (align_x + 1) / 2

    # Apply non-linearity to increase reward as alignment improves
    align_z_reward = align_z_reward**2
    align_x_reward = align_x_reward**2

    return 0.5 * (align_z_reward + align_x_reward)


def approach_gripper_club_grip(
    env: ManagerBasedRLEnv, offset: float = 0.04
) -> torch.Tensor:
    """Reward the robot's gripper reaching the club grip with the right pose.

    Uses a continuous reward function that encourages fingers to approach their ideal positions
    on opposite sides of the club grip.
    """
    # Target object position
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_pos = club.data.body_pos_w[:, club_grip_idx, :]
    club_grip_quat = club.data.body_quat_w[:, club_grip_idx, :]

    # Get club orientation vectors
    club_rot_mat = matrix_from_quat(club_grip_quat)
    club_long_axis = club_rot_mat[..., 2]  # Assuming z is along the grip length

    # Fingertips position
    ee_fingertips_w = env.scene["ee_frame"].data.target_pos_w[..., 1:, :]
    lfinger_pos = ee_fingertips_w[..., 0, :]
    rfinger_pos = ee_fingertips_w[..., 1, :]

    # Find a reference vector perpendicular to club_long_axis (for side-to-side orientation)
    world_up = torch.tensor([0.0, 0.0, 1.0], device=club_long_axis.device).repeat(
        club_long_axis.shape[0], 1
    )
    side_dir = torch.cross(club_long_axis, world_up, dim=-1)
    side_dir_norm = torch.norm(side_dir, dim=-1, keepdim=True)
    # Handle case where club is parallel to world up
    side_dir = torch.where(
        side_dir_norm > 1e-6,
        side_dir / side_dir_norm,
        torch.tensor([1.0, 0.0, 0.0], device=side_dir.device),
    )

    # Calculate ideal positions for left and right fingers
    ideal_left = club_grip_pos - side_dir * offset
    ideal_right = club_grip_pos + side_dir * offset

    # Compute distances to ideal positions
    left_dist = torch.norm(lfinger_pos - ideal_left, dim=-1)
    right_dist = torch.norm(rfinger_pos - ideal_right, dim=-1)

    # Convert distances to rewards (closer is better)
    left_reward = torch.exp(-5.0 * left_dist)
    right_reward = torch.exp(-5.0 * right_dist)

    return 0.5 * (left_reward + right_reward)


def lifting_club_grip(env: ManagerBasedRLEnv, z_threshold: float) -> torch.Tensor:
    """Reward for lifting the club grip above a threshold height.

    Only rewards lifting when the club is being grasped, with the reward scaling based on grasp quality.
    """
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_pos = club.data.body_pos_w[:, club_grip_idx, :]

    # Get a continuous grasp quality measure
    grasp_quality = approach_gripper_club_grip(env, offset=0.04)

    # Height above threshold (clipped at 0 to avoid negative rewards)
    height_above = torch.clamp(club_grip_pos[:, 2] - z_threshold, min=0.0)

    # Apply a threshold to grasp_quality to ensure club is actually held
    # Use a smooth step function centered at 0.3 quality threshold
    is_held = torch.sigmoid(
        (grasp_quality - 0.3) * 20
    )  # Sharper transition than regular sigmoid

    # Scale reward by grasp quality (between 1x and 2x multiplier for held grasps)
    # but only when the club is actually held
    scaling_factor = 1.0 + grasp_quality

    return is_held * scaling_factor * height_above


def approach_hitting_point_ball(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for approaching the club grip hitting point to the ball.

    Only rewards approaching the ball when the club is being grasped properly.
    """
    club = env.scene["golf_club"]
    club_hitting_point_idx = club.find_bodies("head_link")[0][0]
    club_hitting_point_pos = club.data.body_pos_w[:, club_hitting_point_idx, :]
    ball_pos = env.scene["golf_ball"].data.root_pos_w
    distance = torch.norm(club_hitting_point_pos - ball_pos, dim=-1, p=2)

    # Distance-based reward (closer is better)
    distance_reward = 1 - torch.tanh(distance)

    # Get a continuous grasp quality measure
    grasp_quality = approach_gripper_club_grip(env, offset=0.04)

    # Apply a threshold to grasp_quality to ensure club is actually held
    # Use a smooth step function centered at 0.3 quality threshold
    is_held = torch.sigmoid(
        (grasp_quality - 0.3) * 20
    )  # Sharp transition but still continuous

    # Scale reward smoothly based on quality of grasp, but only when actually held
    return distance_reward * is_held


def grasp_club_grip(
    env: ManagerBasedRLEnv,
    threshold: float,
    open_joint_pos: float,
    asset_cfg: SceneEntityCfg,
) -> torch.Tensor:
    """Reward for closing the fingers when being close to the club grip."""
    ee_tcp_pos = env.scene["ee_frame"].data.target_pos_w[..., 0, :]
    club = env.scene["golf_club"]
    club_grip_idx = club.find_bodies("grip_link")[0][0]
    club_grip_pos = club.data.body_pos_w[:, club_grip_idx, :]
    gripper_joint_pos = env.scene[asset_cfg.name].data.joint_pos[:, asset_cfg.joint_ids]

    distance = torch.norm(club_grip_pos - ee_tcp_pos, dim=-1, p=2)

    # Smooth distance reward instead of binary is_close
    closeness = torch.exp(-10.0 * (distance - threshold))

    # Encourage closing fingers (proportional to how close they are to closed)
    closing_reward = torch.sum(open_joint_pos - gripper_joint_pos, dim=-1)

    return closeness * closing_reward


def approach_ball_hole(env: ManagerBasedRLEnv) -> torch.Tensor:
    """Reward for approaching the ball to the hole."""
    ball_pos = env.scene["golf_ball"].data.root_pos_w
    hole_pos = hole_poses(env)
    distance = torch.norm(ball_pos - hole_pos, dim=-1, p=2)

    # The original was fine, just keeping for completeness
    return 1 - torch.tanh(distance)
