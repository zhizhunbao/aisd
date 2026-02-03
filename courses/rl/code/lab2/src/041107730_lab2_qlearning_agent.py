"""
Lab 2: Q-Learning Agent for Gymnasium CliffWalking
Author: Peng Wang
Student Number: 041107730

Implements Q-Learning using a class-based structure and Bellman equation.
"""

# ============================================================
# 导入库
# Import Libraries
# ============================================================

# 导入核心系统与日期模块
# Import core system and date modules
import os
import sys
import random
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

# 导入自定义环境包
# Import custom environment package
import cliffwalking_env


# ============================================================
# 配置常量
# Configuration Constants
# (注意：禁止在代码中使用魔术数字 / NOTE: No magic numbers allowed)
# ============================================================

# 训练方案配置
# Training scheme configuration
EPISODES = 500
MAX_STEPS_PER_EPISODE = 1000

# 算法超参数
# Algorithm hyperparameters
GAMMA = 0.9
EPSILON = 0.1
DECAY = 0.5
ALPHA = 1.0

# 实验重现配置
# Reproducibility settings
RANDOM_SEED = 42


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
    # 加载环境变量持久化设置
    load_dotenv('.env.local')

    # 从系统环境解析个人实名标识
    student_name = os.getenv('NAME', 'Peng Wang')
    student_id = os.getenv('NUMBER', '041107730')

    # 获取当前脚本所在的绝对路径
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 配置 UI 分隔线规范与结果输出目录（相对于脚本路径）
    # Configure UI dividers and output directory (relative to script path)
    output_dir = os.path.join(script_dir, "lab2_images")
    line_width = 60
    os.makedirs(output_dir, exist_ok=True)

    # 固定伪随机数发生器核心
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    # 导出任务执行头
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * line_width)
    print(f"Lab Session: {student_name} ({student_id})")
    print(f"Execution Time: {current_time}")
    print("=" * line_width + "\n")

    return output_dir, line_width


# ============================================================
# print_step: 格式化打印实验步骤的 I/O 反馈
# ============================================================
def print_step(step_name, step_input, step_output, line_width):
    print("=" * line_width)
    print(step_name)
    print("=" * line_width)
    print(f"Input: {step_input}")
    print(f"Output: {step_output}\n")


# ============================================================
# save_plot: 渲染并保存可视化成果
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
# QLearningAgent: 封装有 Q-Table 及其更新法则的强化学习类
#                 Reinforcement learning class encapsulating Q-Table and its update rules
# ============================================================
class QLearningAgent:
    """封装有 Q-Table 及其更新法则的强化学习类
    Reinforcement learning class encapsulating Q-Table and its update rules"""

    # ============================================================
    # __init__: 构造并初始化 Q 表结构
    #
    # Parameters:
    #   num_states: 状态空间总数
    #   num_actions: 动作空间总数
    #   gamma: 未来奖励折损率
    #   alpha: 系统学习速率
    # ============================================================
    def __init__(self, num_states, num_actions, gamma, alpha):
        # 存储内部学习策略超参数
        self.gamma = gamma
        self.alpha = alpha
        self.num_actions = num_actions
        
        # 实例化 Q 值矩阵
        # Instantiate Q-Value Matrix
        # 参数：num_states 定义行数（环境中的格点总数），
        #       num_actions 定义列数（智能体可执行的动作数），
        #       random.random() 生成 0~1 间的随机数作为初始估值
        # Parameters: num_states defines rows (total grid points in environment),
        #       num_actions defines columns (number of executable actions),
        #       random.random() generates random 0~1 values as initial estimates
        self.q_table = [[random.random() for _ in range(num_actions)] for _ in range(num_states)]

    # ============================================================
    # train: 执行 Q-Learning 启发式学习循环 (类方法)
    #        Execute Q-Learning heuristic learning loop (Class method)
    #
    # Parameters:
    #   env: 待测试的环境对象
    #   episodes: 总训练回合数
    #   epsilon: 初始探索率
    #   decay: 探索率随回合的衰减率
    #
    # Returns:
    #   tuple: (returns_history, steps_history)
    # ============================================================
    def train(self, env, episodes, epsilon, decay):
        # 计算状态观察值的空间宽度
        xsize = env.observation_space['agent'].high[0] + 1
        
        returns_history = []
        steps_history = []

        # 启动回合级大循环
        for episode in range(episodes):
            # 外部感知重置与映射
            observation, _ = env.reset()
            state = self._state_from_obs(observation, xsize)
            
            total_reward = 0
            steps = 0
            done = False

            # 启动原子级时间步步进
            # Start atomic level time-step stepping
            while not done:
                steps += 1
                
                # ε-贪婪动作决策点
                # ε-greedy action decision point
                action = self._select_action(state, epsilon)

                # 驱动物理引擎步进
                # Drive physics engine step
                # 返回值：observation 下一状态观察，
                #         reward 环境即时奖酬，
                #         terminated 目标终结信号，
                #         truncated 步数截断信号
                # Return values: observation next state obs,
                #         reward immediate penalty/gain,
                #         terminated goal reach signal,
                #         truncated max-step cutoff signal
                next_obs, reward, terminated, truncated, _ = env.step(action)
                next_state = self._state_from_obs(next_obs, xsize)
                total_reward += reward

                # 贝尔曼价值传递公式 (Q-Update)
                # Bellman Value Transfer Formula (Q-Update)
                # 逻辑：Q(s,a) = r + γ * max Q(s',a')
                # Logic: Q(s,a) = r + γ * max Q(s',a')
                best_next_action = max(self.q_table[next_state])
                self.q_table[state][action] = reward + self.gamma * best_next_action
                
                # 状态更替与出口判定
                # State transition and exit condition check
                state = next_state
                done = terminated or truncated

                # 防护：无限循坏强行解挂
                # Guard: Forced breakout of infinite loops
                if steps > MAX_STEPS_PER_EPISODE:
                    break

            # 处理后退属性
            # Process decay attribute
            epsilon -= decay * epsilon
            returns_history.append(total_reward)
            steps_history.append(steps)

            # 控制台即刻反馈汇报
            # Immediate feedback report to console
            print(f"Episode {episode + 1}/{episodes}: {steps} steps, reward: {total_reward:.1f}")

        return returns_history, steps_history

    def _state_from_obs(self, observation, xsize):
        """将多维坐标投影为单一线性索引"""
        agent_pos = observation['agent']
        return agent_pos[1] * xsize + agent_pos[0]

    def _select_action(self, state, epsilon):
        """决策引擎：平衡探索与收敛利用"""
        if random.random() < epsilon:
            return random.choice(range(self.num_actions))
        else:
            state_values = self.q_table[state]
            return state_values.index(max(state_values))


# ============================================================
# 主程序入口
# Main Programme Entry
# ============================================================

def main():
    # ============================================================
    # 步骤 0：初始化实验配置
    # Step 0: Initialize lab configuration
    # ============================================================
    output_dir, line_width = initialize_lab()

    # ============================================================
    # 步骤 1：同步挂载环境并禁用动画渲染（确保纯计算加速）
    # Step 1: Synchronously mount environment and disable animation (ensure pure computation speedup)
    # ============================================================
    env = gymnasium.make("cliffwalking_env/CliffWalking-v0", render_mode=None)
    
    # 解析状态空间几何限制
    # Parse state space geometric constraints
    xsize = env.observation_space['agent'].high[0] + 1
    ysize = env.observation_space['agent'].high[1] + 1
    num_states = xsize * ysize
    num_actions = env.action_space.n

    # 反馈环境就绪报文
    # Feedback environment ready message
    print_step(
        "Step 1: Init Env", 
        "Gymnasium: CliffWalking", 
        f"Resolution: {xsize}x{ysize} ({num_states} States)", 
        line_width
    )

    # ============================================================
    # 步骤 2：部署 Agent 并开启类方法驱动的训练历程
    # Step 2: Deploy Agent and start class-driven training journey
    # ============================================================
    agent = QLearningAgent(num_states, num_actions, GAMMA, ALPHA)
    returns, steps = agent.train(env, EPISODES, EPSILON, DECAY)

    # 打印收敛平均收益指标
    # Print convergence average reward metrics
    performance = f"Episode Reward: {returns[-1]:.1f}"
    print_step("Step 2: Training Agent", "Method: QLearningAgent.train()", performance, line_width)

    # ============================================================
    # 步骤 3: 绘制演进图谱
    # Step 3: Plot evolution maps
    # ============================================================
    # 1. 收益演化记录
    # 1. Reward evolution record
    plt.figure(figsize=(10, 5))
    plt.plot(returns, 'b-', linewidth=1.5)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True, alpha=0.3)
    save_plot("qlearning_returns.png", output_dir, "Q-Learning Episode Returns")

    # 2. 效率轨迹记录
    # 2. Efficiency trajectory record
    plt.figure(figsize=(10, 5))
    plt.plot(steps, 'g-', linewidth=1.5)
    plt.xlabel('Episode')
    plt.ylabel('Steps')
    plt.grid(True, alpha=0.3)
    save_plot("qlearning_steps.png", output_dir, "Q-Learning Steps per Episode")

    # 确认存档完成状态
    # Confirm archive completion status
    print_step(
        "Step 3: Post-Analysis", 
        "Captured Stats", 
        f"Assets Location: {output_dir}/", 
        line_width
    )

    # 彻底释放环境句柄
    # Thoroughly release environment handles
    env.close()


if __name__ == "__main__":
    main()
