# ppo.py
# ============================================================
# PPO Agent for CreateRedBall-v0
# CreateRedBall-v0 PPO 代理
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 使用 Stable-Baselines3 的 PPO 算法训练 Create 3 追踪红球。
# Uses Stable-Baselines3 PPO algorithm to train Create 3
# to track the red ball.
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

import gymnasium as gym
import aisd_examples
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback

# ============================================================
# Configuration constants / 配置常量
# ============================================================
ENV_ID = "aisd_examples/CreateRedBall-v0"
RENDER_MODE = None                    # 训练时不渲染 / No rendering during training
POLICY = "MlpPolicy"                 # 多层感知机策略 / MLP policy
TOTAL_TIMESTEPS = 5000               # 总训练步数 / Total training steps
LOG_INTERVAL = 1                     # 日志打印间隔 / Log print interval
PPO_LEARNING_RATE = 0.0003          # PPO 学习率 / PPO learning rate
PPO_N_STEPS = 2048                  # 每次更新的步数 / Steps per update
PPO_BATCH_SIZE = 64                 # 批大小 / Batch size
PPO_GAMMA = 0.99                    # 折扣因子 / Discount factor
MODEL_NAME = "ppo_createredball"    # 模型保存名 / Model save name
IMAGE_DIR = "screenshots"
os.makedirs(IMAGE_DIR, exist_ok=True)


# ============================================================
# 自定义回调：记录每回合的奖励和步数
# Custom callback: record per-episode rewards and steps
# ============================================================
class EpisodeLogCallback(BaseCallback):
    """Records episode return and length during training.
    记录训练过程中的回合回报和长度。"""

    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self.episode_lengths = []

    def _on_step(self) -> bool:
        infos = self.locals.get("infos", [])
        for info in infos:
            # DummyVecEnv 自动重置并将回合信息移到这里
            # DummyVecEnv auto-resets and moves episode info here
            maybe_ep = info.get("episode")
            if maybe_ep is not None:
                self.episode_rewards.append(float(maybe_ep["r"]))
                self.episode_lengths.append(int(maybe_ep["l"]))
                print(
                    f"Episode {len(self.episode_rewards)}: "
                    f"{int(maybe_ep['l'])} steps, "
                    f"reward: {float(maybe_ep['r']):.1f}"
                )
        return True


# ============================================================
# 训练 / Train
# ============================================================
env = gym.make(ENV_ID, render_mode=RENDER_MODE)
callback = EpisodeLogCallback()

model = PPO(
    POLICY,
    env,
    learning_rate=PPO_LEARNING_RATE,
    n_steps=PPO_N_STEPS,
    batch_size=PPO_BATCH_SIZE,
    gamma=PPO_GAMMA,
    verbose=1,
)
model.learn(
    total_timesteps=TOTAL_TIMESTEPS,
    log_interval=LOG_INTERVAL,
    callback=callback,
)
model.save(MODEL_NAME)

# ============================================================
# 绘制图表 / Plot graphs
# ============================================================
if callback.episode_rewards:
    # Episode Returns
    plt.figure(figsize=(10, 5))
    plt.plot(callback.episode_rewards)
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.title("PPO Episode Returns (CreateRedBall-v0)")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "ppo_returns.png"), dpi=150)
    plt.close()

    # Steps per Episode
    plt.figure(figsize=(10, 5))
    plt.plot(callback.episode_lengths)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.title("PPO Steps per Episode (CreateRedBall-v0)")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "ppo_steps.png"), dpi=150)
    plt.close()

    print(f"Saved: {IMAGE_DIR}/ppo_returns.png, {IMAGE_DIR}/ppo_steps.png")
else:
    print("Warning: No episode data recorded.")

env.close()
