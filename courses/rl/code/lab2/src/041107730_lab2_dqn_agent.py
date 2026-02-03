"""
Lab 2: DQN Agent (Stable-Baselines3) for Gymnasium CliffWalking
Author: Peng Wang
Student Number: 041107730

Trains a DQN agent from Stable-Baselines3 on the custom CliffWalking
Gymnasium environment using a class-based structure.
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

# 导入核心系统与日期模块
# Import core system and date modules
import os
import sys
import warnings
from datetime import datetime

# 抑制 pkg_resources 弃用警告
# Suppress pkg_resources deprecation warning
warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")

# 导入环境变量加载库
# Import environment variable loader
from dotenv import load_dotenv

# 导入数据科学与数值计算模块
# Import data science and numerical computing modules
import numpy as np
import matplotlib.pyplot as plt

# 导入强化学习相关库
# Import reinforcement learning libraries
import gymnasium
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback

# 导入自定义环境包（触发注册）
# Import custom environment package (triggers registration)
import cliffwalking_env


# ============================================================
# 配置常量
# Configuration Constants
# (注意：禁止在代码中使用魔术数字 / NOTE: No magic numbers allowed)
# ============================================================

# 训练总步数
# Total training timesteps
TOTAL_TIMESTEPS = 100000

# DQN学习率：0.001（即 1/1000），控制网络权重更新的步长
# DQN learning rate: 0.001, controls the step size of network weight updates
DQN_LEARNING_RATE = 0.001

# 经验回放缓冲区大小
# Experience replay buffer size
DQN_BUFFER_SIZE = 50000

# 探索阶段占总训练步数的比例
# Fraction of total steps for exploration phase
DQN_EXPLORATION_FRACTION = 0.8

# 探索率的最终下限
# Final epsilon floor
DQN_EXPLORATION_FINAL_EPS = 0.05

# 训练日志打印间隔
# Training log print interval
LOG_INTERVAL = 10

# 随机状态种子
# Random state seed
RANDOM_STATE = 42


# ============================================================
# 工具函数
# Utility Functions
# ============================================================

# ============================================================
# initialize_lab: 步骤 0 - 初始化实验环境与基础配置
#                 Step 0 - Initialize lab environment and configs
#
# Returns:
#   tuple: (output_dir, line_width)
# ============================================================
def initialize_lab():
    # 加载 .env.local 环境变量文件
    # Load .env.local environment variable file
    load_dotenv('.env.local')

    # 从环境变量中读取学生详细信息
    # Read student details from environment variables
    student_name = os.getenv('NAME', 'Peng Wang')
    student_id = os.getenv('NUMBER', '041107730')

    # 获取当前脚本文件所在的绝对路径目录
    # Get the absolute directory path where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义实验结果输出目录（保存在脚本同级目录下，不含学号前缀）
    # Define output directory (saved in the same folder as the script, no student ID prefix)
    output_dir = os.path.join(script_dir, "lab2_images")

    # 定义控制台输出的分隔线宽度
    # Define the divider line length for console output
    line_width = 60

    # 创建输出目录
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # 获取当前运行时间并格式化
    # Get and format current execution time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 打印实验报告头部
    # Print lab report header
    print("=" * line_width)
    print(f"Lab Session: {student_name} ({student_id})")
    print(f"Execution Time: {current_time}")
    print("=" * line_width + "\n")

    # 返回必要的配置参数
    # Return necessary configuration parameters
    return output_dir, line_width


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
# save_plot: 统一样式保存图表到输出目录
#            Save plot to output directory with consistent style
#
# Parameters:
#   filename: 文件名（不含路径）
#   output_dir: 图像保存的目录路径
#   title: 图表标题（可选）
# ============================================================
def save_plot(filename, output_dir, title=None):
    # 如果提供标题，则添加到图表中
    if title:
        plt.title(title)
    # 生成完整的保存路径
    save_path = os.path.join(output_dir, filename)
    # 保存高清图表并去除冗余边距
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    # 关闭当前图表资源
    plt.close()
    # 在控制台输出保存反馈
    print(f"Figure saved: {save_path}")


# ============================================================
# 类与模型定义
# Class and Model Definitions
# ============================================================

# ============================================================
# TrainingCallback: 训练回调类，用于实时记录每回合统计指标
#                   Callback class for real-time recording of per-episode metrics
# ============================================================
class TrainingCallback(BaseCallback):
    """训练回调类，用于实时记录每回合统计指标
    Callback class for real-time recording of per-episode metrics"""

    # ============================================================
    # __init__: 初始化回调实例
    #           Initialize callback instance
    #
    # Parameters:
    #   verbose: 日志冗余级别
    # ============================================================
    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_returns = []
        self.episode_steps = []

    # ============================================================
    # _on_step: 在每个训练步被引擎自动调用
    #           Automatically called by the engine at each step
    #
    # Returns:
    #   bool: 是否继续训练标志
    # ============================================================
    def _on_step(self) -> bool:
        # 检测回合终结信息并存入统计列表
        # Detect episode completion info and store in stats
        infos = self.locals.get("infos", [])
        for info in infos:
            if "episode" in info:
                self.episode_returns.append(info["episode"]["r"])
                self.episode_steps.append(info["episode"]["l"])
        return True


# ============================================================
# DQNAgent: 封装 Stable-Baselines3 DQN 算法的智能体类
#           Agent class encapsulating Stable-Baselines3 DQN algorithm
# ============================================================
class DQNAgent:
    """封装 Stable-Baselines3 DQN 算法的智能体类
    Agent class encapsulating Stable-Baselines3 DQN algorithm"""

    # ============================================================
    # __init__: 初始化智能体实例并构建模型架构
    #           Initialize agent instance and build model architecture
    #
    # Parameters:
    #   env: 待交互的 Gymnasium 环境
    #   lr: 深度神经网络的学习率
    #   buffer_size: 经验回放池的存储容量
    #   fraction: 探索概率衰减所需的步数占比
    #   final_eps: 衰减后的最小探索概率
    # ============================================================
    def __init__(self, env, lr, buffer_size, fraction, final_eps):
        # 实例化内部 DQN 模型并配置超参数
        # Instantiate internal DQN model and configure hyperparameters
        # 参数："MultiInputPolicy" 用于处理字典型观察空间（包含代理和目标位置），
        #       env 为 Gymnasium 强化学习环境，
        #       verbose=1 表示打印详细训练日志，
        #       learning_rate 为优化器学习率，
        #       buffer_size 为经验回放缓冲区的大小（存储历史转移样本），
        #       exploration_fraction 确定探索率从 1.0 衰减到最终值所需的总步数比例，
        #       exploration_final_eps 是探索率的最终下限值（保留最低随机性）
        # Parameters: "MultiInputPolicy" handles dict observation spaces (agent & target positions),
        #       env is the Gymnasium RL environment,
        #       verbose=1 enables detailed training logs,
        #       learning_rate is the optimizer learning rate,
        #       buffer_size is the size of the experience replay buffer (stores past transitions),
        #       exploration_fraction is the fraction of total steps for epsilon decay (from 1.0 to final),
        #       exploration_final_eps is the final exploration probability floor (retains minimum randomness)
        self.model = DQN(
            "MultiInputPolicy",
            env,
            verbose=1,
            learning_rate=lr,
            buffer_size=buffer_size,
            exploration_fraction=fraction,
            exploration_final_eps=final_eps,
            seed=RANDOM_STATE
        )

    # ============================================================
    # train: 执行智能体的学习迭代过程 (类成员方法)
    #        Perform agent's learning iteration (Class method)
    #
    # Parameters:
    #   total_timesteps: 学习总步数
    #   log_interval: 日志输出间隔
    #
    # Returns:
    #   tuple: (model, episode_returns, episode_steps)
    # ============================================================
    def train(self, total_timesteps, log_interval):
        # 创建自定义统计监测器
        callback = TrainingCallback()
        # 开启强化学习训练引擎
        self.model.learn(
            total_timesteps=total_timesteps, 
            log_interval=log_interval, 
            callback=callback
        )
        return self.model, callback.episode_returns, callback.episode_steps

    # ============================================================
    # save: 将训练好的模型权重持久化到本地文件
    #       Persist trained model weights to a local file
    #
    # Parameters:
    #   model_name: 目标文件名称
    # ============================================================
    def save(self, model_name):
        self.model.save(model_name)


# ============================================================
# 主程序入口
# Main Programme Entry
# ============================================================

def main():
    # ============================================================
    # 步骤 0：实验初始化
    # Step 0: Lab Initialization
    # ============================================================
    output_dir, line_width = initialize_lab()

    # ============================================================
    # 步骤 1：构建强化学习环境
    # Step 1: Initialize Environment
    # ============================================================

    # 创建悬崖行走环境并禁用归绘图动画（设为 None 以极速运行）
    # Create CliffWalking environment and disable animation (set to None for max speed)
    env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode=None)

    # 打印环境就绪状态
    # Print environment readiness status
    print_step(
        "Step 1: Initialize Environment", 
        "cliffwalking_env/CliffWalking-v0", 
        f"Env Ready: {env.action_space} Actions", 
        line_width
    )

    # ============================================================
    # 步骤 2：执行类方法驱动的 Agent 训练
    # Step 2: Agent Training via Class Method
    # ============================================================

    # 实例化 Agent 并应用超参数
    # Instantiate Agent and apply hyperparameters
    agent = DQNAgent(
        env, 
        DQN_LEARNING_RATE, 
        DQN_BUFFER_SIZE, 
        DQN_EXPLORATION_FRACTION, 
        DQN_EXPLORATION_FINAL_EPS
    )

    # 触发训练逻辑
    # Trigger training logic
    model, returns, steps = agent.train(TOTAL_TIMESTEPS, LOG_INTERVAL)

    # 汇总训练成果
    # Summarize training results
    print_step(
        "Step 2: Train DQN Agent", 
        f"Method: DQNAgent.train()", 
        f"Episodes Captured: {len(returns)}", 
        line_width
    )

    # ============================================================
    # 步骤 3：多维数据持久化与展示
    # Step 3: Persistence and Visualization
    # ============================================================

    # 定义本地存档标识
    # Define local archive identifier
    model_name = "dqn_cliffwalking"
    agent.save(model_name)

    # 1. 绘制收益收敛曲线
    # 1. Plot reward convergence curve
    plt.figure(figsize=(10, 5))
    plt.plot(returns, 'b-', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True, alpha=0.3)
    save_plot("dqn_returns.png", output_dir, "DQN Episode Returns")

    # 2. 绘制步数效率曲线
    # 2. Plot step efficiency curve
    plt.figure(figsize=(10, 5))
    plt.plot(steps, 'g-', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Steps')
    plt.grid(True, alpha=0.3)
    save_plot("dqn_steps.png", output_dir, "DQN Steps per Episode")

    # 打印步骤 3 汇总
    # Print Step 3 summary
    print_step(
        "Step 3: Save Model & Plots", 
        f"Results in {output_dir}", 
        f"Model: {model_name}.zip", 
        line_width
    )

    # 停用图形渲染并关闭环境
    # Deactivate graphics rendering and close environment
    env.close()


if __name__ == "__main__":
    main()
