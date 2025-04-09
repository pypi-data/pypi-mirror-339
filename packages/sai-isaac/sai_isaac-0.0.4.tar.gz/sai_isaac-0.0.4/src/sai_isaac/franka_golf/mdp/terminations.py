# MDP for Franka Golf
# Author: Matin Moezzi (matin@aiarena.io)
# Date: 2025-03-17

from __future__ import annotations

from typing import TYPE_CHECKING
from .observations import hole_poses

import torch

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def is_ball_in_hole(env: ManagerBasedRLEnv):
    hole_pos = hole_poses(env)
    ball_pos = env.scene["golf_ball"].data.root_pos_w
    return torch.norm(ball_pos - hole_pos, dim=-1) < 0.05
