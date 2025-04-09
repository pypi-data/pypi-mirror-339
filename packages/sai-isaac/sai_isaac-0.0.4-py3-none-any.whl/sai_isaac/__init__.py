from gymnasium import register

# Cobot Stack
register(
    id="Isaac-Cobot-Stack-v0",
    entry_point="sai_isaac.utils.common:create_isaacsim_env",
    kwargs={
        "env_cfg_entry_point": "sai_isaac.cobotstack:CobotStackCfg",
        "env_entry_point": "isaaclab.envs:ManagerBasedRLEnv",
    },
)

# Frank Golf
register(
    id="Isaac-Franka-Golf-Direct-v0",
    entry_point="sai_isaac.utils.common:create_isaacsim_env",
    kwargs={
        "env_cfg_entry_point": "sai_isaac.franka_golf:FrankaGolfDirectEnvCfg",
        "env_entry_point": "sai_isaac.franka_golf:FrankaGolfDirectEnv",
    },
)

register(
    id="Isaac-Franka-Golf-Joint-v0",
    entry_point="sai_isaac.utils.common:create_isaacsim_env",
    kwargs={
        "env_cfg_entry_point": "sai_isaac.franka_golf:FrankaGolfEnvCfg",
        "env_entry_point": "isaaclab.envs:ManagerBasedRLEnv",
    },
)

register(
    id="Isaac-Franka-Golf-IK-Rel-v0",
    entry_point="sai_isaac.utils.common:create_isaacsim_env",
    kwargs={
        "env_cfg_entry_point": "sai_isaac.franka_golf:FrankaGolfEnvCfg_IKRel",
        "env_entry_point": "isaaclab.envs:ManagerBasedRLEnv",
    },
)

register(
    id="Isaac-Franka-Golf-IK-Abs-v0",
    entry_point="sai_isaac.utils.common:create_isaacsim_env",
    kwargs={
        "env_cfg_entry_point": "sai_isaac.franka_golf:FrankaGolfEnvCfg_IKAbs",
        "env_entry_point": "isaaclab.envs:ManagerBasedRLEnv",
    },
)
