"""
CliffWalking Environment Module Initialization
Author: Peng Wang
Student Number: 041107730

Exports the environment classes for external registration.
"""

# ============================================================
# 导出环境类
# Export Environment Classes
# ============================================================

# 导出原始网格世界环境
# Export original GridWorld environment
from cliffwalking_env.envs.grid_world import GridWorldEnv

# 导出定制化悬崖行走环境
# Export customized CliffWalking environment
from cliffwalking_env.envs.cliff_walking import CliffWalkingEnv
