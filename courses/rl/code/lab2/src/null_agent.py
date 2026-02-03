"""
Lab 2: Null Agent for Environment Testing
Author: Peng Wang
Student Number: 041107730

Tests the CliffWalking Gymnasium environment with random actions.
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

# 导入核心系统与时间模块
# Import core system and time modules
import os
import sys
import time
import warnings
from datetime import datetime

# 抑制 pkg_resources 弃用警告
# Suppress pkg_resources deprecation warning
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

# 导入环境变量加载库
# Import environment variable loader
from dotenv import load_dotenv

# 导入强化学习相关库
# Import reinforcement learning libraries
import gymnasium

# 导入自定义环境包（触发注册）
# Import custom environment package (triggers registration)
import cliffwalking_env


# ============================================================
# 配置常量
# Configuration Constants
# (注意：禁止在代码中使用魔术数字 / NOTE: No magic numbers allowed)
# ============================================================

# 随机测试总步数
# Total random test steps
TEST_STEPS = 100

# 每步之间的延迟（秒）
# Delay between steps (seconds)
STEP_DELAY = 0.1


# ============================================================
# 工具函数
# Utility Functions
# ============================================================

# ============================================================
# initialize_lab: 步骤 0 - 初始化实验环境与基础配置
#                 Step 0 - Initialize lab environment and configs
#
# Returns:
#   dict: 包含初始化后的配置项
# ============================================================
def initialize_lab():
    # 加载 .env.local 环境变量文件
    load_dotenv('.env.local')

    # 从环境变量中读取学生详细信息
    student_name = os.getenv('NAME', 'Peng Wang')
    student_id = os.getenv('NUMBER', '041107730')

    # 定义控制台输出的分隔线长度
    line_width = 60

    # 获取当前运行时间并格式化
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 打印实验报告头部
    print("=" * line_width)
    print(f"Lab Session: {student_name} ({student_id})")
    print(f"Execution Time: {current_time}")
    print("=" * line_width + "\n")

    return {
        "student_name": student_name,
        "student_id": student_id,
        "line_width": line_width
    }


# ============================================================
# print_step: 格式化打印实验步骤的输入与输出
#            Format and print lab step inputs and outputs
#
# Parameters:
#   step_name: 步骤标题名称
#   step_input: 该步骤的输入描述
#   step_output: 该步骤的输出结果描述
#   line_width: 分隔线宽度
# ============================================================
def print_step(step_name, step_input, step_output, line_width):
    # 打印步骤顶部分隔线
    print("=" * line_width)
    # 打印步骤标题
    print(step_name)
    # 打印步骤中部分隔线
    print("=" * line_width)
    # 打印输入与输出信息
    print(f"Input: {step_input}")
    print(f"Output: {step_output}\n")


# ============================================================
# 主程序入口
# Main Programme Entry
# ============================================================

def main():
    # ============================================================
    # 步骤 0：实验初始化
    # Step 0: Lab Initialization
    # ============================================================
    config = initialize_lab()

    # ============================================================
    # 步骤 1：创建环境
    # Step 1: Create Environment
    # ============================================================

    # 创建环境（人类渲染模式）
    env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode="human")

    # 重置环境
    observation, info = env.reset()

    # 打印步骤 1 汇总
    print_step(
        "Step 1: Initialize Environment", 
        "cliffwalking_env/CliffWalking-v0", 
        f"Initial Obs: {observation}", 
        config["line_width"]
    )

    # ============================================================
    # 步骤 2：执行随机动作测试
    # Step 2: Perform Random Action Tests
    # ============================================================

    total_reward = 0
    steps = 0
    episodes = 0

    print(f"Executing {TEST_STEPS} random steps test...")

    for _ in range(TEST_STEPS):
        # 随机采样动作
        action = env.action_space.sample()

        # 执行动作步进
        observation, reward, terminated, truncated, _ = env.step(action)
        total_reward += reward
        steps += 1

        # 视觉观察延迟
        time.sleep(STEP_DELAY)

        # 检查回合结束
        if terminated or truncated:
            episodes += 1
            print(f"  Episode {episodes}: {steps} steps, Reward: {total_reward:.1f}")
            observation, _ = env.reset()
            total_reward = 0
            steps = 0

    # 打印步骤 2 汇总
    print_step(
        "Step 2: Random Agent Testing", 
        f"{TEST_STEPS} Random Steps", 
        f"Test Completed: {episodes} Episodes finished", 
        config["line_width"]
    )

    # 关闭环境资源
    env.close()


if __name__ == "__main__":
    main()
