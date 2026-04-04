# dqn.py
# ============================================================
# DQN Agent for CreateRedBall-v0
# CreateRedBall-v0 DQN 代理
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 使用 Stable-Baselines3 的 DQN 算法训练 Create 3 追踪红球。
# Uses Stable-Baselines3 DQN algorithm to train Create 3
# to track the red ball.
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

import gymnasium as gym
import aisd_examples
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback

# ============================================================
# Configuration constants / 配置常量
# ============================================================
ENV_ID = "aisd_examples/CreateRedBall-v0"
RENDER_MODE = None                   # 训练时不渲染 / No rendering during training
POLICY = "MlpPolicy"                # 多层感知机策略 / MLP policy
TOTAL_TIMESTEPS = 5000              # 总训练步数 / Total training steps
LOG_INTERVAL = 4                    # 日志打印间隔 / Log print interval
DQN_LEARNING_RATE = 0.001          # DQN 学习率 / DQN learning rate
DQN_BUFFER_SIZE = 50000            # 经验回放缓冲区大小 / Replay buffer size
DQN_EXPLORATION_INITIAL_EPS = 1.0  # 初始探索率 / Initial exploration rate
DQN_EXPLORATION_FINAL_EPS = 0.05   # 最终探索率 / Final exploration rate
DQN_EXPLORATION_FRACTION = 0.1     # 探索率衰减比例 / Exploration decay fraction
MODEL_NAME = "dqn_createredball"   # 模型保存名 / Model save name
IMAGE_DIR = "screenshots"
os.makedirs(IMAGE_DIR, exist_ok=True)


# ============================================================
# 自定义回调：记录每回合的奖励和步数
# Custom callback: record per-episode rewards and steps
#
# SB3 将环境包装在 Monitor + DummyVecEnv 中，
# 回合结束时统计信息出现在 infos 中。
# SB3 wraps envs with Monitor + DummyVecEnv,
# episode stats appear in infos when an episode ends.
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

model = DQN(
    POLICY,
    env,
    learning_rate=DQN_LEARNING_RATE,
    buffer_size=DQN_BUFFER_SIZE,
    exploration_initial_eps=DQN_EXPLORATION_INITIAL_EPS,
    exploration_final_eps=DQN_EXPLORATION_FINAL_EPS,
    exploration_fraction=DQN_EXPLORATION_FRACTION,
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
    plt.title("DQN Episode Returns (CreateRedBall-v0)")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "dqn_returns.png"), dpi=150)
    plt.close()

    # Steps per Episode
    plt.figure(figsize=(10, 5))
    plt.plot(callback.episode_lengths)
    plt.xlabel("Episode")
    plt.ylabel("Steps")
    plt.title("DQN Steps per Episode (CreateRedBall-v0)")
    plt.tight_layout()
    plt.savefig(os.path.join(IMAGE_DIR, "dqn_steps.png"), dpi=150)
    plt.close()

    print(f"Saved: {IMAGE_DIR}/dqn_returns.png, {IMAGE_DIR}/dqn_steps.png")
else:
    print("Warning: No episode data recorded.")

env.close()
