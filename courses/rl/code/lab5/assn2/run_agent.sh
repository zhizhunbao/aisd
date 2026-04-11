#!/bin/bash
# 终端3: 运行 agent（undock 完成后执行）
# Usage: bash run_agent.sh [null|qlearning|dqn|ppo|non-rl]
source /opt/ros/humble/setup.bash
source ~/create3_ws/install/setup.bash
cd ~/Assn2

AGENT=${1:-null}
echo "Running ${AGENT}.py ..."
python3 "${AGENT}.py"
