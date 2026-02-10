import os
import gymnasium
import numpy as np
import matplotlib.pyplot as plt
import cliffwalking_env
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

# ============================================================
# Configuration constants
# ============================================================
ENV_ID = "cliffwalking_env/CliffWalking-v0"
RENDER_MODE = None
POLICY = "MultiInputPolicy"
TOTAL_TIMESTEPS = 10000
LOG_INTERVAL = 4
MODEL_NAME = "ppo_cliff"
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "lab2_images")
os.makedirs(IMAGE_DIR, exist_ok=True)


# ============================================================
# Custom callback to record episode returns & steps
# ============================================================
class EpisodeLogCallback(BaseCallback):
    """Records episode return and length during training.

    SB3 wraps envs with Monitor + DummyVecEnv, so episode stats
    are available in `self.locals["infos"]` when an episode ends.
    """
    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self.episode_lengths = []

    def _on_step(self) -> bool:
        infos = self.locals.get("infos", [])
        for info in infos:
            # DummyVecEnv auto-resets and moves episode info here
            maybe_ep = info.get("episode")
            if maybe_ep is not None:
                self.episode_rewards.append(float(maybe_ep["r"]))
                self.episode_lengths.append(int(maybe_ep["l"]))
                print(f"Episode {len(self.episode_rewards)}: "
                      f"{int(maybe_ep['l'])} steps, "
                      f"reward: {float(maybe_ep['r']):.1f}")
        return True




# ============================================================
# Train
# ============================================================
env = gymnasium.make(ENV_ID, render_mode=RENDER_MODE)
callback = EpisodeLogCallback()
model = PPO(POLICY, env, verbose=1)
model.learn(total_timesteps=TOTAL_TIMESTEPS, log_interval=LOG_INTERVAL, callback=callback)
model.save(MODEL_NAME)

# ============================================================
# Plot episode returns
# ============================================================
if callback.episode_rewards:
    plt.figure()
    plt.plot(callback.episode_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("PPO Episode Returns")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "ppo_returns.png"))
    plt.close()

    # Plot steps per episode
    plt.figure()
    plt.plot(callback.episode_lengths)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.title("PPO Steps per Episode")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "ppo_steps.png"))
    plt.close()
else:
    print("Warning: No episode data was recorded. Try increasing TOTAL_TIMESTEPS.")

env.close()
