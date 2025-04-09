"""
Random agent for Isaac Lab environments.
"""
import time
import torch
import argparse
import gymnasium as gym
import sai_isaac

# add argparse arguments
parser = argparse.ArgumentParser(description="Random agent for Isaac Lab environments.")
parser.add_argument(
    "--disable_fabric",
    action="store_true",
    default=False,
    help="Disable fabric and use USD I/O operations.",
)
parser.add_argument(
    "--num_envs", type=int, default=2, help="Number of environments to simulate."
)
parser.add_argument(
    "--task", type=str, default="Isaac-Cobot-Stack-v0", help="Name of the task."
)
parser.add_argument(
    "--headless", type=bool, default=False, help="Run in headless mode."
)

args_cli = parser.parse_args()


def main():
    # Create the environment using the wrapper
    env = gym.make(
        args_cli.task, num_envs=args_cli.num_envs, headless=args_cli.headless
    )

    # Get environment information
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")

    # Run a few episodes
    num_episodes = 50
    max_steps_per_episode = 50

    for episode in range(num_episodes):
        print(f"\nEpisode {episode + 1}/{num_episodes}")

        # Reset the environment
        obs, info = env.reset()
        episode_rewards = torch.zeros(
            env.unwrapped.num_envs, device=env.unwrapped.device
        )
        episode_steps = torch.zeros(
            env.unwrapped.num_envs, dtype=torch.int, device=env.unwrapped.device
        )

        for step in range(max_steps_per_episode):
            # Sample random actions for all environments
            actions = torch.tensor(
                env.action_space.sample(), device=env.unwrapped.device
            )
            # actions = torch.zeros_like(actions)

            # Take a step in the environment
            obs, reward, terminated, truncated, info = env.step(actions)
            episode_rewards += reward
            episode_steps += 1

            # Check which environments are done
            done_envs = terminated | truncated

            # Reset environments that are done
            if torch.any(done_envs):
                # Get indices of done environments
                done_indices = torch.where(done_envs)[0]

                # Print information for done environments
                for env_idx in done_indices:
                    print(
                        f"Environment {env_idx} finished after {episode_steps[env_idx].item()} steps with reward {episode_rewards[env_idx]:.2f}"
                    )

                # Reset only the done environments
                obs, info = env.reset()

                # Reset rewards and steps for done environments
                episode_rewards[done_indices] = 0
                episode_steps[done_indices] = 0

            # Sleep to slow down visualization
            if not args_cli.headless:
                time.sleep(0.01)

            # Check if all environments are done
            if torch.all(done_envs):
                print(f"All environments finished after {step + 1} steps")
                break

        # Print episode summary
        print(
            f"Episode {episode + 1} average reward: {episode_rewards.mean().item():.2f}"
        )
        print(f"Episode {episode + 1} max reward: {episode_rewards.max().item():.2f}")
        print(f"Episode {episode + 1} min reward: {episode_rewards.min().item():.2f}")

    # Close the environment
    env.close()
    print("Test completed successfully!")


if __name__ == "__main__":
    main()
