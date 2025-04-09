import importlib
from typing import Any, Union

import gymnasium as gym
import torch

def create_isaacsim_env(
    env_entry_point: Union[str, Any],
    env_cfg_entry_point: Union[str, Any],
    headless: bool = True,
    num_envs: int = 1,
) -> gym.Env:
    """Create an IsaacSim environment with the specified configuration.

    This function creates and initializes an IsaacSim environment using the provided
    entry points for both the environment and its configuration. It handles CUDA availability
    checks and IsaacLab package imports.

    Args:
        env_entry_point: Either a string in the format "module:class" or a class object
            representing the environment to create.
        env_cfg_entry_point: Either a string in the format "module:class" or a class object
            representing the environment configuration.
        headless: Whether to run the simulation in headless mode (no GUI).
        num_envs: Number of parallel environments to create.

    Returns:
        A Gymnasium environment instance.

    Raises:
        ImportError: If the IsaacLab package is not installed.
        ValueError: If the entry points are invalid or not properly formatted.
        AssertionError: If CUDA is not available on the device.
    """
    # Check if CUDA is available
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is not available on this device")

    # Import IsaacLab packages
    try:
        from isaaclab.app import AppLauncher  # noqa: F401
    except ImportError:
        raise ImportError(
            "Please install the `isaaclab` package to use the IsaacSimGym"
        )

    # Launch Isaac Sim
    app_cfg = {"headless": headless, "enable_cameras": True}
    AppLauncher(app_cfg)

    # Parse and import environment class
    if isinstance(env_entry_point, str):
        try:
            mod_name, cls_name = env_entry_point.rsplit(":", 1)
            mod = importlib.import_module(mod_name)
            entry_cls = getattr(mod, cls_name)
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(
                f"Invalid environment entry point '{env_entry_point}': {str(e)}"
            )
    else:
        entry_cls = env_entry_point

    # Parse and import environment configuration
    if isinstance(env_cfg_entry_point, str):
        try:
            mod_name, cls_name = env_cfg_entry_point.rsplit(":", 1)
            mod = importlib.import_module(mod_name)
            env_cfg_cls = getattr(mod, cls_name)()
        except (ValueError, ImportError, AttributeError) as e:
            raise ValueError(
                f"Invalid environment config entry point '{env_cfg_entry_point}': {str(e)}"
            )
    else:
        env_cfg_cls = env_cfg_entry_point

    # Set number of environments
    env_cfg_cls.scene.num_envs = num_envs

    return entry_cls(cfg=env_cfg_cls)