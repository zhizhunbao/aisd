# null.py
# ============================================================
# Null Agent for CreateRedBall-v0
# CreateRedBall-v0 空代理
#
# 作者: Peng Wang (041107730)
# Author: Peng Wang (041107730)
#
# 随机选择动作来测试环境是否正常工作。
# Selects random actions to test if the environment works.
# ============================================================

import gymnasium as gym
import aisd_examples

# ============================================================
# Configuration constants / 配置常量
# ============================================================
ENV_ID = "aisd_examples/CreateRedBall-v0"
RENDER_MODE = "human"
TEST_STEPS = 1000

# ============================================================
# 创建环境并运行随机动作
# Create environment and run random actions
# ============================================================
env = gym.make(ENV_ID, render_mode=RENDER_MODE)
observation, info = env.reset()

# 执行 TEST_STEPS 步随机动作
# Perform random actions for TEST_STEPS steps
for i in range(TEST_STEPS):
    action = env.action_space.sample()  # 随机选择动作 / Random action
    observation, reward, terminated, truncated, info = env.step(action)
    print(f"Step {i+1}: action={action}, obs={observation}, reward={reward:.3f}")

    if terminated or truncated:
        observation, info = env.reset()

env.close()
