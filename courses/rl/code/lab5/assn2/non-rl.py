# non-rl.py
# ============================================================
# Non-RL Agent for CreateRedBall-v0
# CreateRedBall-v0 非 RL 代理
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 直接计算动作，不使用 RL 算法。
# Directly computes actions without using RL algorithms.
#
# 策略 / Strategy:
#   动作 = 观测值（红球 x 像素位置）
#   action = observation (red ball x-pixel position)
#   这样机器人会旋转到红球当前位置对应的方向，
#   使红球保持在视野中心。
#   This makes the robot rotate to the direction corresponding
#   to the red ball's current position, keeping it centered.
#
#   直觉 / Intuition:
#   - 如果红球在 x=100（左侧），action=100 → 向左转
#     If red ball is at x=100 (left), action=100 → turn left
#   - 如果红球在 x=320（中心），action=320 → 不转
#     If red ball is at x=320 (center), action=320 → no turn
#   - 如果红球在 x=500（右侧），action=500 → 向右转
#     If red ball is at x=500 (right), action=500 → turn right
# ============================================================

import os
import numpy as np
import matplotlib.pyplot as plt

import gymnasium as gym
import aisd_examples

# ============================================================
# Configuration constants / 配置常量
# ============================================================
ENV_ID = "aisd_examples/CreateRedBall-v0"
RENDER_MODE = None                    # 训练时不渲染 / No rendering during training
EPISODES = 50                         # 回合数（和 Q-Learning 一致便于对比）
IMAGE_DIR = "screenshots"
os.makedirs(IMAGE_DIR, exist_ok=True)


# ============================================================
# 直接计算策略：action = observation
# Direct computation policy: action = observation
#
# 更智能的版本：使用比例控制，避免过度旋转
# Smarter version: use proportional control to avoid overshooting
# ============================================================
def compute_action(observation):
    """
    非 RL 策略：将动作设置为当前红球位置。
    Non-RL policy: set action to current red ball position.

    这等效于告诉机器人"转到红球所在的方向"。
    This is equivalent to telling the robot "turn towards the red ball".
    """
    # 如果观测值为 320（默认中心 = 没检测到球），旋转搜索
    # If observation is 320 (default center = no ball detected), rotate to search
    if int(observation) == 320:
        return 0  # 动作 0 → 最大左转角速度，搜索红球 / action 0 → max left turn to search
    return int(observation)


# ============================================================
# 运行多个回合并记录指标
# Run multiple episodes and record metrics
# ============================================================
env = gym.make(ENV_ID, render_mode=RENDER_MODE)

episode_rewards = []
episode_steps = []

for episode in range(EPISODES):
    observation, info = env.reset()
    total_reward = 0
    steps = 0
    done = False

    while not done:
        steps += 1
        # 非 RL 策略：直接使用观测值作为动作
        # Non-RL policy: directly use observation as action
        action = compute_action(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated

    episode_rewards.append(total_reward)
    episode_steps.append(steps)
    print(f"Episode {episode + 1}/{EPISODES}: "
          f"{steps} steps, reward: {total_reward:.1f}")

env.close()

# ============================================================
# 绘制图表 / Plot graphs
# ============================================================
# Episode Returns
plt.figure(figsize=(10, 5))
plt.plot(episode_rewards)
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.title('Non-RL Agent: Episode Returns\n(action = observation, direct computation)')
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "nonrl_returns.png"), dpi=150)
plt.close()
print(f"Saved: {IMAGE_DIR}/nonrl_returns.png")

# Steps per Episode
plt.figure(figsize=(10, 5))
plt.plot(episode_steps)
plt.xlabel('Episode')
plt.ylabel('Steps')
plt.title('Non-RL Agent: Steps per Episode\n(action = observation, direct computation)')
plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, "nonrl_steps.png"), dpi=150)
plt.close()
print(f"Saved: {IMAGE_DIR}/nonrl_steps.png")

print("\nNon-RL agent complete.")
