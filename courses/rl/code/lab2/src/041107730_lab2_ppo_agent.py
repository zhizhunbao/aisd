"""
Lab 2: PPO Agent (Stable-Baselines3) for Gymnasium CliffWalking
Author: Peng Wang
Student Number: 041107730

Trains a PPO agent from Stable-Baselines3 on the custom CliffWalking
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
from stable_baselines3 import PPO
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

# PPO学习率：恢复标准 0.0003 以加快学习速度
# PPO learning rate: 0.0003 for faster acquisition
PPO_LEARNING_RATE = 0.0003

# 每次策略更新前收集的步数：1024 步
# Steps collected before each policy update: 1024 steps
PPO_N_STEPS = 1024

# 每次梯度更新使用的样本数
# Samples per gradient update
PPO_BATCH_SIZE = 64

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
    load_dotenv('.env.local')

    # 从环境变量中读取学生详细信息
    student_name = os.getenv('NAME', 'Peng Wang')
    student_id = os.getenv('NUMBER', '041107730')

    # 获取当前脚本文件所在的绝对路径目录
    # Get the absolute directory path where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义实验结果输出目录（相对于脚本路径，不含学号）
    # Define output directory (relative to script path, no student ID)
    output_dir = os.path.join(script_dir, "lab2_images")
    line_width = 60

    # 实体创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 打印标准化实验头
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * line_width)
    print(f"Lab Session: {student_name} ({student_id})")
    print(f"Execution Time: {current_time}")
    print("=" * line_width + "\n")

    return output_dir, line_width


# ============================================================
# print_step: 格式化打印实验步骤的输入与输出
#            Format and print lab step inputs and outputs
# ============================================================
def print_step(step_name, step_input, step_output, line_width):
    print("=" * line_width)
    print(step_name)
    print("=" * line_width)
    print(f"Input: {step_input}")
    print(f"Output: {step_output}\n")


# ============================================================
# save_plot: 统一样式保存图表到输出目录
#            Save plot to output directory with consistent style
# ============================================================
def save_plot(filename, output_dir, title=None):
    if title:
        plt.title(title)
    save_path = os.path.join(output_dir, filename)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Figure saved: {save_path}")


# ============================================================
# 类与模型定义
# Class and Model Definitions
# ============================================================

# ============================================================
# TrainingCallback: 训练回调类，用于实时记录 PPO 的每个回合数据
#                   Callback class for real-time recording of PPO episode data
# ============================================================
class TrainingCallback(BaseCallback):
    """训练回调类，用于实时记录 PPO 的每个回合数据
    Callback class for real-time recording of PPO episode data"""

    # ============================================================
    # __init__: 初始化策略回调
    #
    # Parameters:
    #   verbose: 冗余程度
    # ============================================================
    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_returns = []
        self.episode_steps = []

    # ============================================================
    # _on_step: 在时间步推进时捕获环境反馈
    #
    # Returns:
    #   bool: 是否继续迭代
    # ============================================================
    def _on_step(self) -> bool:
        infos = self.locals.get("infos", [])
        for info in infos:
            if "episode" in info:
                self.episode_returns.append(info["episode"]["r"])
                self.episode_steps.append(info["episode"]["l"])
        return True


# ============================================================
# PPOAgent: 封装 Stable-Baselines3 PPO 算法的智能体类
#           Agent class encapsulating Stable-Baselines3 PPO algorithm
# ============================================================
class PPOAgent:
    """封装 Stable-Baselines3 PPO 算法的智能体类
    Agent class encapsulating Stable-Baselines3 PPO algorithm"""

    # ============================================================
    # __init__: 构造智能体并初始化 PPO 核心模型
    #           Construct agent and initialize PPO core model
    #
    # Parameters:
    #   env: 待注册的 Gymnasium 环境空间
    #   lr: 深度神经网络的更新步长
    #   n_steps: 在执行更新前需收集的时间步数量
    #   batch_size: 梯度更新时的小批量容量
    # ============================================================
    def __init__(self, env, lr, n_steps, batch_size):
        # 实例化内部 PPO 模型并配置超参数
        # Instantiate internal PPO model and configure hyperparameters
        # 参数："MultiInputPolicy" 用于处理网格世界的坐标字典输入，
        #       env 为 Gymnasium 交互环境，
        #       verbose=1 开启控制台详细训练反馈，
        #       learning_rate 决定策略梯度更新的速度，
        #       n_steps 定义每次学习前缓存的步数，
        #       batch_size 定义每次梯度计算使用的样本量
        # Parameters: "MultiInputPolicy" handles the coordinate dict input of the grid world,
        #       env is the Gymnasium interaction environment,
        #       verbose=1 enables detailed training feedback in console,
        #       learning_rate determines the speed of policy gradient updates,
        #       n_steps defines the number of steps to buffer before each learning phase,
        #       batch_size defines the sample size used for each gradient calculation
        self.model = PPO(
            "MultiInputPolicy",
            env,
            verbose=1,
            learning_rate=lr,
            n_steps=n_steps,
            batch_size=batch_size,
            ent_coef=0.2,
            seed=RANDOM_STATE
        )

    # ============================================================
    # train: 执行 PPO 学习引擎的成员方法 (类方法)
    #        Member method to execute PPO learning engine (Class method)
    #
    # Parameters:
    #   total_timesteps: 训练周期内的总步数
    #   log_interval: 控制台日志的回传频率
    #
    # Returns:
    #   tuple: (model, episode_returns, episode_steps)
    # ============================================================
    def train(self, total_timesteps, log_interval):
        callback = TrainingCallback()
        self.model.learn(
            total_timesteps=total_timesteps, 
            log_interval=log_interval, 
            callback=callback
        )
        return self.model, callback.episode_returns, callback.episode_steps

    # ============================================================
    # save: 将当前主模型的状态字典存入磁盘
    #       Save current main model's state dict to disk
    #
    # Parameters:
    #   model_name: 存档名称
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
    # 步骤 1：同步环境加载
    # Step 1: Environment Sync Loading
    # ============================================================

    # 调起悬崖世界仿真器并禁用图形渲染（提升训练效率）
    # Launch CliffWalking world simulator and disable rendering (to improve training efficiency)
    env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode=None)

    # 导出步骤确认消息
    # Export step confirmation message
    print_step(
        "Step 1: Initialize Environment", 
        "cliffwalking_env/CliffWalking-v0", 
        f"Initialized: {env.action_space}", 
        line_width
    )

    # ============================================================
    # 步骤 2：启动基于类的 Agent 训练任务
    # Step 2: Launch Class-based Agent Training
    # ============================================================

    # 构建 PPO 智能体对象
    # Construct PPO agent object
    agent = PPOAgent(
        env, 
        PPO_LEARNING_RATE, 
        PPO_N_STEPS, 
        PPO_BATCH_SIZE
    )

    # 通过成员方法触发学习机制
    # Trigger learning mechanism via member method
    model, returns, steps = agent.train(TOTAL_TIMESTEPS, LOG_INTERVAL)

    # 显示训练阶段完成状态
    # Show training phase completion status
    print_step(
        "Step 2: Train PPO Agent", 
        f"Method: PPOAgent.train()", 
        f"Captured {len(returns)} Episodes", 
        line_width
    )

    # ============================================================
    # 步骤 3：数据图景生成与本地归档
    # Step 3: Visualization and Archiving
    # ============================================================

    # 归档模型二进制文件
    # Archive model binary file
    model_name = "ppo_cliffwalking"
    agent.save(model_name)

    # 1. 绘制收敛性能曲线
    # 1. Plot convergence performance curve
    plt.figure(figsize=(10, 5))
    plt.plot(returns, 'r-', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True, alpha=0.3)
    save_plot("ppo_returns.png", output_dir, "PPO Episode Returns")

    # 2. 绘制步数效率曲线
    # 2. Plot step efficiency curve
    plt.figure(figsize=(10, 5))
    plt.plot(steps, 'm-', alpha=0.7)
    plt.xlabel('Episode')
    plt.ylabel('Steps')
    plt.grid(True, alpha=0.3)
    save_plot("ppo_steps.png", output_dir, "PPO Steps per Episode")

    # 打印最终步骤摘要
    # Print final step summary
    print_step(
        "Step 3: Save Model & Plots", 
        f"Trained PPO Assets", 
        f"Path: {output_dir}", 
        line_width
    )

    # 关闭仿真器资源
    # Close simulator resource
    env.close()


if __name__ == "__main__":
    main()
