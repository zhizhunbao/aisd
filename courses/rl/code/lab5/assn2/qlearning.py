# qlearning.py
# ============================================================
# Q-Learning Agent for CreateRedBall-v0
# CreateRedBall-v0 Q-Learning 代理
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 在 CreateRedBall-v0 环境上实现表格型 Q-Learning。
# Implements tabular Q-Learning on the CreateRedBall-v0 environment.
#
# 状态空间: 641 个离散状态 (x 像素 0-640)
# State space: 641 discrete states (x-pixel 0-640)
# 动作空间: 641 个离散动作 (映射到 Twist 角速度)
# Action space: 641 discrete actions (maps to Twist angular velocity)
#
# 注意: 641×641 的 Q 表相当大 (约 411,000 个条目)，
# 但对于现代机器来说仍在可接受范围内。
# Note: A 641×641 Q-table is quite large (~411,000 entries),
# but still manageable for modern machines.
# ============================================================

import os
import random
import numpy as np
import matplotlib.pyplot as plt

import gymnasium as gym
import aisd_examples

# ============================================================
# Configuration / 配置
# ============================================================
IMAGE_DIR = "screenshots"
os.makedirs(IMAGE_DIR, exist_ok=True)

# ============================================================
# 多组超参数用于对比（原始 + 3 组新参数）
# Multiple hyperparameter sets for comparison (original + 3 new sets)
#
# 格式: (title, EPISODES, ALPHA, GAMMA, EPSILON_INIT, EPSILON_DECAY, EPSILON_MIN)
# Format: (title, EPISODES, ALPHA, GAMMA, EPSILON_INIT, EPSILON_DECAY, EPSILON_MIN)
# ============================================================
HYPERPARAMETER_SETS = [
    # 原始超参数（作业要求标题为 "Original Hyperparameters"）
    # Original Hyperparameters (assignment requires this title)
    ("Original Hyperparameters",
     50, 0.1, 0.99, 1.0, 0.95, 0.01),
]


def run_qlearning(title, episodes, alpha, gamma, epsilon_init, epsilon_decay, epsilon_min):
    """
    运行一组超参数的 Q-Learning 训练。
    Run Q-Learning training with one set of hyperparameters.

    Q-Learning 更新公式 / Q-Learning update formula:
        Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]

    参数 / Parameters:
        title: 实验标题 / Experiment title
        episodes: 训练回合数 / Number of training episodes
        alpha: 学习率 / Learning rate
        gamma: 折扣因子 / Discount factor
        epsilon_init: 初始探索率 / Initial exploration rate
        epsilon_decay: 探索率衰减 / Exploration decay rate
        epsilon_min: 最小探索率 / Minimum exploration rate

    返回 / Returns:
        (episode_rewards, episode_steps): 每回合的奖励和步数列表
                                          Lists of per-episode rewards and steps
    """
    env = gym.make("aisd_examples/CreateRedBall-v0", render_mode=None)

    n_states = env.observation_space.n    # 641
    n_actions = env.action_space.n        # 641

    # --------------------------------------------------------
    # Q 表初始化（全零）
    # Q-table initialization (all zeros)
    # 大小: 641 × 641 ≈ 411,000 个条目
    # Size: 641 × 641 ≈ 411,000 entries
    # --------------------------------------------------------
    Q = np.zeros((n_states, n_actions))

    episode_rewards = []
    episode_steps = []
    epsilon = epsilon_init

    for episode in range(episodes):
        state, _ = env.reset()
        total_reward = 0
        steps = 0
        done = False

        while not done:
            steps += 1

            # --------------------------------------------------------
            # ε-贪心策略选择动作
            # Epsilon-greedy action selection
            # --------------------------------------------------------
            if random.random() < epsilon:
                # 探索：随机选择动作 / Explore: random action
                action = env.action_space.sample()
            else:
                # 利用：选择 Q 值最大的动作 / Exploit: max Q-value action
                action = int(np.argmax(Q[state]))

            # --------------------------------------------------------
            # 执行动作并获取反馈
            # Execute action and get feedback
            # --------------------------------------------------------
            next_state, reward, terminated, truncated, info = env.step(action)
            total_reward += reward

            # --------------------------------------------------------
            # Q-Learning 更新
            # Q-Learning update
            # Q(s,a) ← Q(s,a) + α[r + γ·max_a'Q(s',a') - Q(s,a)]
            # --------------------------------------------------------
            best_next = np.max(Q[next_state])
            Q[state, action] += alpha * (
                reward + gamma * best_next - Q[state, action]
            )

            state = next_state
            done = terminated or truncated

        # 衰减探索率 / Decay exploration rate
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        episode_rewards.append(total_reward)
        episode_steps.append(steps)
        print(f"  Episode {episode + 1}/{episodes}: "
              f"{steps} steps, reward: {total_reward:.1f}, "
              f"epsilon: {epsilon:.4f}")

    env.close()
    return episode_rewards, episode_steps


# ============================================================
# 训练所有超参数组合
# Train all hyperparameter sets
# ============================================================
all_results = []

for i, (title, episodes, alpha, gamma, eps, decay, eps_min) in enumerate(HYPERPARAMETER_SETS):
    print(f"\n{'=' * 60}")
    print(f"Training Set {i + 1}: {title}")
    print(f"{'=' * 60}")
    rewards, steps = run_qlearning(title, episodes, alpha, gamma, eps, decay, eps_min)
    all_results.append((title, rewards, steps))

# ============================================================
# 为每组超参数生成图表
# Generate plots for each hyperparameter set
# ============================================================
for i, (title, rewards, steps) in enumerate(all_results):
    # Episode Returns
    plt.figure(figsize=(10, 5))
    plt.plot(rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title(f'Q-Learning Episode Returns\n{title}')
    plt.tight_layout()
    fname = f"qlearning_set{i + 1}_returns.png"
    plt.savefig(os.path.join(IMAGE_DIR, fname), dpi=150)
    plt.close()

    # Steps per Episode
    plt.figure(figsize=(10, 5))
    plt.plot(steps)
    plt.xlabel('Episode')
    plt.ylabel('Steps')
    plt.title(f'Q-Learning Steps per Episode\n{title}')
    plt.tight_layout()
    fname = f"qlearning_set{i + 1}_steps.png"
    plt.savefig(os.path.join(IMAGE_DIR, fname), dpi=150)
    plt.close()

    print(f"Saved: qlearning_set{i + 1}_returns.png, qlearning_set{i + 1}_steps.png")

print("\nQ-Learning training complete.")
