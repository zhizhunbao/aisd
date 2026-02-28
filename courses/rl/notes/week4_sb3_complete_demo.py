"""
Week 4: Stable-Baselines3 完整演示
Week 4: Stable-Baselines3 Complete Demo

演示 SB3 的统一 API、算法对比、向量化环境和超参数调优。
Demonstrates SB3 unified API, algorithm comparison, vectorized environments, and hyperparameter tuning.
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gymnasium as gym
from gymnasium import spaces

# 输出目录 (Output directory)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week4_sb3_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


# ============================================================
# 步骤 1：SB3 统一 API 演示
# Step 1: SB3 Unified API Demo
# ============================================================

from stable_baselines3 import DQN, PPO, A2C
from stable_baselines3.common.evaluation import evaluate_policy

print("=" * 60)
print("Step 1: SB3 Unified API Demo")
print("=" * 60)

# 使用 CartPole-v1 演示统一 API
# Use CartPole-v1 to demonstrate unified API
env = gym.make("CartPole-v1")

print(f"\nEnvironment: CartPole-v1")
print(f"  Observation space: {env.observation_space}")
print(f"  Action space: {env.action_space}")

# 演示所有算法共享相同 API
# Demonstrate all algorithms share the same API
algorithms = {
    "DQN": DQN,
    "PPO": PPO,
    "A2C": A2C,
}

results = {}
for name, AlgClass in algorithms.items():
    print(f"\n--- Training {name} ---")
    model = AlgClass("MlpPolicy", env, verbose=0, seed=42)
    model.learn(total_timesteps=5000)

    # 评估 (Evaluate)
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10, deterministic=True)
    results[name] = (mean_reward, std_reward)
    print(f"  {name}: mean_reward = {mean_reward:.1f} +/- {std_reward:.1f}")

env.close()

# 可视化算法对比 (Visualize algorithm comparison)
fig, ax = plt.subplots(figsize=(8, 5))
names = list(results.keys())
means = [results[n][0] for n in names]
stds = [results[n][1] for n in names]
colors = ['#3498db', '#2ecc71', '#e74c3c']

bars = ax.bar(names, means, yerr=stds, capsize=5, color=colors, alpha=0.8, edgecolor='#2c3e50')
ax.set_title("SB3 Algorithm Comparison on CartPole-v1\n(5000 timesteps training)", fontsize=12)
ax.set_ylabel("Mean Reward (10 episodes)")
ax.set_ylim(0, 550)
ax.axhline(y=500, color='gray', linestyle='--', alpha=0.5, label='Max possible (500)')
ax.legend()

for bar, mean in zip(bars, means):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            f'{mean:.0f}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step1_algorithm_comparison.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n>> Saved: step1_algorithm_comparison.png")


# ============================================================
# 步骤 2：训练曲线对比 — DQN vs PPO vs A2C
# Step 2: Training Curves Comparison — DQN vs PPO vs A2C
# ============================================================

print("\n" + "=" * 60)
print("Step 2: Training Curves Comparison")
print("=" * 60)

from stable_baselines3.common.callbacks import BaseCallback

class RewardLoggerCallback(BaseCallback):
    """记录每个 episode 的奖励 (Log reward per episode)"""
    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self._current_reward = 0

    def _on_step(self):
        # 累积奖励 (Accumulate reward)
        self._current_reward += self.locals.get("rewards", [0])[0]
        dones = self.locals.get("dones", [False])
        if dones[0]:
            self.episode_rewards.append(self._current_reward)
            self._current_reward = 0
        return True

training_curves = {}
timesteps = 20000

for name, AlgClass in algorithms.items():
    print(f"  Training {name} for {timesteps} timesteps...")
    env = gym.make("CartPole-v1")
    callback = RewardLoggerCallback()
    model = AlgClass("MlpPolicy", env, verbose=0, seed=42)
    model.learn(total_timesteps=timesteps, callback=callback)
    training_curves[name] = callback.episode_rewards
    env.close()
    print(f"    Episodes: {len(callback.episode_rewards)}, "
          f"Final avg: {np.mean(callback.episode_rewards[-20:]):.1f}")

# 可视化训练曲线 (Visualize training curves)
fig, ax = plt.subplots(figsize=(10, 5))
colors_map = {"DQN": '#3498db', "PPO": '#2ecc71', "A2C": '#e74c3c'}
window = 10

for name, rewards in training_curves.items():
    if len(rewards) > window:
        smoothed = np.convolve(rewards, np.ones(window)/window, mode='valid')
        ax.plot(smoothed, label=f"{name} (smoothed)", color=colors_map[name], linewidth=1.5)

ax.set_title(f"Training Curves: DQN vs PPO vs A2C on CartPole-v1\n({timesteps} timesteps)", fontsize=12)
ax.set_xlabel("Episode")
ax.set_ylabel("Episode Reward")
ax.axhline(y=500, color='gray', linestyle='--', alpha=0.5, label='Max (500)')
ax.legend()
ax.set_ylim(0, 550)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step2_training_curves.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n>> Saved: step2_training_curves.png")


# ============================================================
# 步骤 3：Policy 选择演示 — MlpPolicy vs MultiInputPolicy
# Step 3: Policy Selection Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 3: Policy Selection Demo")
print("=" * 60)

print("""
Policy 选择规则 (Policy Selection Rules):

┌─────────────────────────┬──────────────────┐
│ Observation Space       │ Policy           │
├─────────────────────────┼──────────────────┤
│ Discrete(n)             │ MlpPolicy        │
│ Box(shape=(d,))         │ MlpPolicy        │
│ Dict({...})             │ MultiInputPolicy │
│ Box(shape=(H,W,C))      │ CnnPolicy        │
└─────────────────────────┴──────────────────┘

示例:
  # Discrete 观测
  env = gym.make("CartPole-v1")  # Box(4,) obs
  model = DQN("MlpPolicy", env)

  # Dict 观测
  # model = DQN("MultiInputPolicy", env_with_dict_obs)

  # 图像观测
  # model = PPO("CnnPolicy", env_with_image_obs)
""")

# 演示 CartPole 的观测空间
# Demo CartPole observation space
env = gym.make("CartPole-v1")
obs, info = env.reset(seed=42)
print(f"CartPole-v1 observation space: {env.observation_space}")
print(f"  Type: Box")
print(f"  Shape: {env.observation_space.shape}")
print(f"  Sample obs: {obs}")
print(f"  → Use MlpPolicy")
env.close()

# 可视化 Policy 选择决策树
# Visualize Policy selection decision tree
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')
ax.set_title("SB3 Policy Selection Decision Tree", fontsize=14)

# Root
ax.text(5, 7, "Observation Space Type?", ha='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', edgecolor='#2c3e50'))

# Branches
branches = [
    (2, 5, "Discrete(n)\nor Box(d,)", "MlpPolicy", '#3498db'),
    (5, 5, "Dict({...})", "MultiInputPolicy", '#e74c3c'),
    (8, 5, "Box(H,W,C)\n(images)", "CnnPolicy", '#2ecc71'),
]

for x, y, obs_type, policy, color in branches:
    ax.annotate("", xy=(x, y+0.5), xytext=(5, 6.5),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
    ax.text(x, y, obs_type, ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#f8f9fa', edgecolor='gray'))
    ax.text(x, y-1.5, policy, ha='center', fontsize=12, fontweight='bold', color=color,
            bbox=dict(boxstyle='round,pad=0.4', facecolor=color, edgecolor=color, alpha=0.15))

# Algorithm selection
ax.text(5, 1.5, "Algorithm Selection", ha='center', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', edgecolor='#2c3e50'))

alg_info = [
    (1.5, 0.3, "DQN\nDiscrete only", '#3498db'),
    (4, 0.3, "PPO\nBoth (default)", '#2ecc71'),
    (6.5, 0.3, "A2C\nBoth", '#e67e22'),
    (9, 0.3, "SAC\nContinuous only", '#9b59b6'),
]
for x, y, text, color in alg_info:
    ax.text(x, y, text, ha='center', fontsize=9, color=color, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.1, edgecolor=color))

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step3_policy_selection.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n>> Saved: step3_policy_selection.png")


# ============================================================
# 步骤 4：向量化环境演示
# Step 4: Vectorized Environment Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 4: Vectorized Environment Demo")
print("=" * 60)

from stable_baselines3.common.env_util import make_vec_env
import time

# 对比不同 n_envs 的训练速度
# Compare training speed with different n_envs
env_counts = [1, 4, 8]
vec_results = {}

for n_envs in env_counts:
    vec_env = make_vec_env("CartPole-v1", n_envs=n_envs, seed=42)
    model = PPO("MlpPolicy", vec_env, verbose=0, seed=42, n_steps=256)

    start_time = time.time()
    model.learn(total_timesteps=10000)
    elapsed = time.time() - start_time

    mean_reward, std_reward = evaluate_policy(model, gym.make("CartPole-v1"), n_eval_episodes=10)
    vec_results[n_envs] = {"time": elapsed, "reward": mean_reward, "std": std_reward}

    print(f"  n_envs={n_envs}: time={elapsed:.2f}s, reward={mean_reward:.1f}+/-{std_reward:.1f}")
    vec_env.close()

# 可视化 (Visualize)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# 训练时间
envs = list(vec_results.keys())
times = [vec_results[n]["time"] for n in envs]
ax1.bar([str(n) for n in envs], times, color=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.8)
ax1.set_title("Training Time vs n_envs\n(PPO, 10k timesteps)", fontsize=12)
ax1.set_xlabel("n_envs")
ax1.set_ylabel("Time (seconds)")
for i, (n, t) in enumerate(zip(envs, times)):
    ax1.text(i, t + 0.1, f"{t:.2f}s", ha='center', fontsize=10)

# 奖励
rewards = [vec_results[n]["reward"] for n in envs]
stds = [vec_results[n]["std"] for n in envs]
ax2.bar([str(n) for n in envs], rewards, yerr=stds, capsize=5,
        color=['#3498db', '#2ecc71', '#e74c3c'], alpha=0.8)
ax2.set_title("Mean Reward vs n_envs\n(PPO, 10k timesteps)", fontsize=12)
ax2.set_xlabel("n_envs")
ax2.set_ylabel("Mean Reward")
ax2.set_ylim(0, 550)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step4_vectorized_env.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n>> Saved: step4_vectorized_env.png")


# ============================================================
# 步骤 5：超参数影响演示
# Step 5: Hyperparameter Impact Demo
# ============================================================

print("\n" + "=" * 60)
print("Step 5: Hyperparameter Impact Demo")
print("=" * 60)

# 对比不同 learning_rate 的影响
# Compare impact of different learning rates
learning_rates = [1e-2, 3e-4, 1e-5]
lr_results = {}

for lr in learning_rates:
    env = gym.make("CartPole-v1")
    callback = RewardLoggerCallback()
    model = PPO("MlpPolicy", env, learning_rate=lr, verbose=0, seed=42)
    model.learn(total_timesteps=15000, callback=callback)
    lr_results[lr] = callback.episode_rewards
    env.close()
    avg = np.mean(callback.episode_rewards[-20:]) if len(callback.episode_rewards) >= 20 else np.mean(callback.episode_rewards)
    print(f"  lr={lr:.0e}: episodes={len(callback.episode_rewards)}, final_avg={avg:.1f}")

# 可视化 (Visualize)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Learning rate 对比
colors_lr = ['#e74c3c', '#2ecc71', '#3498db']
for (lr, rewards), color in zip(lr_results.items(), colors_lr):
    if len(rewards) > 10:
        smoothed = np.convolve(rewards, np.ones(10)/10, mode='valid')
        ax1.plot(smoothed, label=f"lr={lr:.0e}", color=color, linewidth=1.5)

ax1.set_title("Impact of Learning Rate on PPO\n(CartPole-v1, 15k timesteps)", fontsize=12)
ax1.set_xlabel("Episode")
ax1.set_ylabel("Episode Reward")
ax1.axhline(y=500, color='gray', linestyle='--', alpha=0.5)
ax1.legend()
ax1.set_ylim(0, 550)

# 超参数总结表
ax2.axis('off')
ax2.set_title("Key SB3 Hyperparameters", fontsize=12)

table_data = [
    ["Parameter", "Default", "Effect"],
    ["learning_rate", "3e-4", "Step size"],
    ["gamma", "0.99", "Discount factor"],
    ["n_steps", "2048", "Steps per update"],
    ["gae_lambda", "0.95", "Bias-variance"],
    ["clip_range", "0.2", "PPO clipping"],
    ["ent_coef", "0.0", "Exploration"],
    ["max_grad_norm", "0.5", "Gradient clip"],
]

table = ax2.table(cellText=table_data[1:], colLabels=table_data[0],
                  loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

# 设置表头样式
for j in range(3):
    table[0, j].set_facecolor('#2c3e50')
    table[0, j].set_text_props(color='white', fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "step5_hyperparameters.png"), dpi=150, bbox_inches='tight')
plt.close()
print(f"\n>> Saved: step5_hyperparameters.png")


# ============================================================
# 步骤 6：模型保存/加载与评估
# Step 6: Model Save/Load and Evaluation
# ============================================================

print("\n" + "=" * 60)
print("Step 6: Model Save/Load and Evaluation")
print("=" * 60)

import tempfile

# 训练并保存模型 (Train and save model)
env = gym.make("CartPole-v1")
model = PPO("MlpPolicy", env, verbose=0, seed=42)
model.learn(total_timesteps=10000)

# 保存 (Save)
save_path = os.path.join(OUTPUT_DIR, "ppo_cartpole")
model.save(save_path)
print(f"  Model saved to: {save_path}.zip")

# 加载 (Load)
loaded_model = PPO.load(save_path)
print(f"  Model loaded from: {save_path}.zip")

# 评估原始模型和加载的模型 (Evaluate both)
mean1, std1 = evaluate_policy(model, env, n_eval_episodes=20)
mean2, std2 = evaluate_policy(loaded_model, env, n_eval_episodes=20)
print(f"\n  Original model:  {mean1:.1f} +/- {std1:.1f}")
print(f"  Loaded model:    {mean2:.1f} +/- {std2:.1f}")
print(f"  Models are equivalent: {abs(mean1 - mean2) < 50}")

# 运行一个完整 episode 并记录 (Run one full episode)
obs, info = env.reset(seed=0)
episode_reward = 0
steps = 0
actions_taken = []

while True:
    action, _ = loaded_model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    episode_reward += reward
    steps += 1
    actions_taken.append(int(action))
    if terminated or truncated:
        break

print(f"\n  Demo episode: {steps} steps, reward = {episode_reward:.1f}")
print(f"  Actions (first 20): {actions_taken[:20]}...")
env.close()

print("\n" + "=" * 60)
print("Demo Complete!")
print("=" * 60)
print(f"\nAll charts saved to: {OUTPUT_DIR}")
print(f"  1. step1_algorithm_comparison.png")
print(f"  2. step2_training_curves.png")
print(f"  3. step3_policy_selection.png")
print(f"  4. step4_vectorized_env.png")
print(f"  5. step5_hyperparameters.png")
