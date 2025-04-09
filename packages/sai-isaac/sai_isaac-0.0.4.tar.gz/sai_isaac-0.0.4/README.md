# ArenaX Lab's IsaacSim Environments

This package contains the IsaacSim environments used for the SAI Platform.

## Installation

```bash
pip install sai-isaac
```

## Usage

```python
import gymnasium as gym
import sai_isaac

env = gym.make("Isaac-Franka-Golf-v0")
```

# Environment List

- `Isaac-Cobot-Stack-v0`: A robotic arm environment with a block to stack.
- `Isaac-Franka-Golf-Direct-v0`: A robotic arm playing golf.
- `Isaac-Franka-Golf-v0`: A robotic arm playing golf.
- `Isaac-Franka-Golf-IK-Rel-v0`: A robotic arm playing golf with inverse kinematics.
- `Isaac-Franka-Golf-IK-Abs-v0`: A robotic arm playing golf with inverse kinematics.

# More Information

- [SAI Platform](https://competesai.com)
- [SAI Documentation](https://docs.competesai.com)
