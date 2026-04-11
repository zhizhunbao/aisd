"""
AISD Examples Gymnasium Environment Package
作者: Peng Wang (041107730)
Author: Peng Wang (041107730)

注册 CreateRedBall-v0 环境。
Registers CreateRedBall-v0 environment.
"""

from gymnasium.envs.registration import register

# CreateRedBall-v0: 基于 Create 3 机器人的红球追踪环境
# CreateRedBall-v0: Create 3 robot red ball tracking environment
register(
    id="aisd_examples/CreateRedBall-v0",
    entry_point="aisd_examples.envs:Create3RedBallEnv",
)
