"""
CST8509 Lab 2: Q-Learning Agent for Cliff Walking (Gymnasium)
Author: Peng Wang
Student Number: 041107730

Description:
This script adapts the Q-Learning algorithm to work with the custom Gymnasium CliffWalking environment.
It implements the ε-greedy policy for exploration-exploitation balance and the Bellman equation 
for Q-value updates. The agent's performance is visualized through episode returns and step counts.
"""

# 导入必要的系统和环境管理库
# Import necessary system and environment management libraries
import os
import random
from datetime import datetime
from dotenv import load_dotenv

# 导入科学计算和绘图库
# Import scientific computing and plotting libraries
import numpy as np
import matplotlib.pyplot as plt

# 导入 Gymnasium 框架和自定义环境
# Import Gymnasium framework and custom environment
import gymnasium as gym
import cliffwalking_env

# 加载个人信息
# Load personal information
load_dotenv('.env.local')


def get_state_index(observation, xsize):
    """将坐标观测转换为一维状态索引
    Convert coordinate observation to 1D state index"""

    # 提取代理的 [x, y] 坐标
    # Extract agent's [x, y] coordinates
    agent_pos = observation['agent']
    
    # 计算一维索引：index = y * width + x
    # Calculate 1D index: index = y * width + x
    return int(agent_pos[1] * xsize + agent_pos[0])


def train(env, episodes, gamma, epsilon, decay, alpha):
    """训练 Q-Learning 智能体
    Train Q-Learning agent"""

    # 获取环境状态总数和动作总数
    # Get total number of states and actions in the environment
    xsize = env.observation_space['agent'].high[0] + 1
    ysize = env.observation_space['agent'].high[1] + 1
    num_states = xsize * ysize
    num_actions = env.action_space.n

    # 初始化随机 Q 表
    # Initialize random Q-table
    q_table = np.random.rand(num_states, num_actions)

    # 存储统计信息用于后续绘图
    # Store statistics for later plotting
    all_returns = []
    all_steps = []

    # 训练循环
    # Training loop
    for episode in range(episodes):
        # 重置环境
        # Reset environment
        observation, info = env.reset()
        state = get_state_index(observation, xsize)
        
        episode_return = 0
        steps = 0
        terminated = False
        truncated = False

        while not (terminated or truncated):
            # ε-贪婪策略：平衡平衡探索与利用
            # ε-greedy policy: balancing exploration and exploitation
            if random.random() < epsilon:
                # 探索：随机选择动作
                # Exploration: choose random action
                action = env.action_space.sample()
            else:
                # 利用：选择最优动作
                # Exploitation: choose best action
                action = np.argmax(q_table[state])

            # 执行动作
            # Execute action
            next_obs, reward, terminated, truncated, info = env.step(action)
            next_state = get_state_index(next_obs, xsize)
            
            # 使用贝尔曼方程更新 Q 表
            # Update Q-table using Bellman equation
            # 公式：Q(s,a) = (1-α)Q(s,a) + α[r + γ * max Q(s',a')]
            best_next_action = np.argmax(q_table[next_state])
            td_target = reward + gamma * q_table[next_state][best_next_action]
            q_table[state][action] = (1 - alpha) * q_table[state][action] + alpha * td_target

            # 更新状态、回报和步数
            # Update state, return, and steps
            state = next_state
            episode_return += reward
            steps += 1

            # 防止陷入无限循环
            # Prevent getting stuck in infinite loop
            if steps > 1000:
                break

        # 衰减探索率
        # Decay exploration rate
        epsilon *= (1 - decay)
        
        # 记录统计数据
        # Record statistics
        all_returns.append(episode_return)
        all_steps.append(steps)

        # 每 10 回合打印一次进度
        # Print progress every 10 episodes
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1}/{episodes} | Return: {episode_return} | Steps: {steps}")

    return q_table, all_returns, all_steps


def main():
    """主程序：设置参数、运行训练并绘图
    Main program: set parameters, run training, and plot results"""

    # 打印页眉
    # Print header
    print("=" * 80)
    print("Step 1: Q-Learning Agent Training on CliffWalking-v0")
    print("=" * 80)
    print(f"Author: {os.getenv('NAME', 'Peng Wang')}")
    print(f"Student Number: {os.getenv('NUMBER', '041107730')}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("-" * 80)

    # 创建实验图像保存目录 (路径相对于当前脚本)
    # Create directory to save experiment images (path relative to current script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'lab2_images')
    os.makedirs(output_dir, exist_ok=True)

    # 设置超参数
    # Set hyperparameters
    HYPERPARAMS = {
        "EPISODES": 500,     # 增加回合数以确保收敛 / More episodes to ensure convergence
        "GAMMA": 0.9,        # 折扣因子 / Discount factor
        "EPSILON": 0.1,      # 初始探索率 / Initial exploration rate
        "DECAY": 0.01,       # 衰减率 / Decay rate
        "ALPHA": 0.1         # 学习率 / Learning rate
    }

    # 打印超参数配置
    # Print hyperparameter configuration
    print("Hyperparameters:")
    for key, val in HYPERPARAMS.items():
        print(f"  {key}: {val}")
    print("-" * 80)

    # 创建不带渲染的环境进行快速训练
    # Create environment without rendering for fast training
    env = gym.make("cliffwalking_env/CliffWalking-v0", render_mode=None)

    # 开始训练
    # Start training
    print("Training agent...")
    q_table, returns, steps = train(
        env=env,
        episodes=HYPERPARAMS["EPISODES"],
        gamma=HYPERPARAMS["GAMMA"],
        epsilon=HYPERPARAMS["EPSILON"],
        decay=HYPERPARAMS["DECAY"],
        alpha=HYPERPARAMS["ALPHA"]
    )
    print("Training complete!")
    print("-" * 80)

    # 步骤 2：可视化训练结果
    # Step 2: Visualize training results
    print("=" * 80)
    print("Step 2: Plotting and Saving Results")
    print("=" * 80)

    # 绘制回合回报曲线
    # Plot episode returns
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(returns)
    plt.title('Episode Returns')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')

    # 绘制每回合步数曲线
    # Plot steps per episode
    plt.subplot(1, 2, 2)
    plt.plot(steps)
    plt.title('Steps per Episode')
    plt.xlabel('Episode')
    plt.ylabel('Step Count')

    # 保存图表
    # Save chart
    plot_path = os.path.join(output_dir, 'qlearning_performance.png')
    plt.tight_layout()
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Performance plots saved to: {plot_path}")

    # 运行一次带渲染的可视化演示
    # Run a visualized demonstration with rendering
    print("\nRunning visual demonstration...")
    render_env = gym.make("cliffwalking_env/CliffWalking-v0", render_mode="human")
    obs, info = render_env.reset()
    xsize = render_env.observation_space['agent'].high[0] + 1
    
    for _ in range(50):
        state = get_state_index(obs, xsize)
        action = np.argmax(q_table[state])
        obs, reward, terminated, truncated, info = render_env.step(action)
        if terminated or truncated:
            break
    
    render_env.close()
    print("Demonstration finished.")

    # 提交提示 (仅限调试)
    # Submission Reminder (Debugging only)
    print("\n" + "=" * 60)
    print("Reminder:")
    print("1. Ensure screenshots are of Terminal Output and relevant plots.")
    print("2. Submit .py results and .ipynb converted notebook.")
    print("=" * 60)


# 程序入口点
# Program entry point
if __name__ == "__main__":
    main()
