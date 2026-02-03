"""
CliffWalking Environment Package
CST8509 Lab 2 - Gymnasium Environments for Reinforcement Learning
Student ID: 041107730
"""

# 导入gymnasium的注册函数
# Import gymnasium's register function
from gymnasium.envs.registration import register

# 注册GridWorld原始环境（Lab 2 Step 2: Trial Run 使用）
# Register original GridWorld environment (used by Lab 2 Step 2: Trial Run)
register(
    id="cliffwalking_env/GridWorld-v0",
    entry_point="cliffwalking_env.envs:GridWorldEnv",
    max_episode_steps=300,
)

# 注册CliffWalking环境
# Register CliffWalking environment
register(
    id="cliffwalking_env/CliffWalking-v0",
    entry_point="cliffwalking_env.envs:CliffWalkingEnv",
    max_episode_steps=200,
)
