"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""

# 导入操作系统、时间、随机和动态导入模块
# Import os, time, random and importlib modules
import os
import time
import random
import importlib

# 动态导入悬崖行走环境模块
# Dynamically import the cliff walking environment module
env_module = importlib.import_module('041107730_lab2_cliff_env')


def train(env: env_module.Env, episodes: int, gamma: float,
          epsilon: float, decay: float, alpha: float) -> list[list[float]]:
    """训练Q-Learning智能体
    Train Q-Learning agent"""

    # 初始化Q表，使用随机值
    # Initialize Q-table with random values
    # 原因：随机初始化可以打破对称性，帮助探索不同的状态-动作组合
    # Reason: Random initialization breaks symmetry and helps explore different state-action pairs
    qtable = [
        [random.random() for _ in range(env.actions())]
        for _ in range(env.states())
    ]

    # 训练主循环，遍历所有回合
    # Main training loop, iterate through all episodes
    for episode in range(episodes):
        # 重置环境，获取初始状态
        # Reset environment and get initial state
        state, _, done = env.reset()
        steps = 0
        episode_reward = 0

        # 回合内循环，直到到达终止状态
        # Episode loop, until reaching terminal state
        while not done:
            # 清屏并显示当前状态
            # Clear screen and show current state
            os.system('cls' if os.name == 'nt' else 'clear')

            # 打印当前回合信息
            # Print current episode information
            print("episode #", episode + 1, "/", episodes)
            print(f"Steps: {steps} | Total Reward: {episode_reward} | Epsilon: {epsilon:.4f}")

            # 渲染当前环境状态
            # Render current environment state
            env.render()

            # 暂停以便观察动画效果
            # Pause to observe the animation
            time.sleep(0.05)

            # 增加步数计数
            # Increment step count
            steps += 1

            # ε-贪婪策略 (ε-greedy policy)：平衡“探索”与“利用”
            # ε-greedy policy: balancing "Exploration" and "Exploitation"
            # 1. 探索 (Exploration)：以 epsilon 概率随机尝试，防止陷入局部最优。
            # 2. 利用 (Exploitation)：以 1-epsilon 概率选择当前认为最好的动作。
            if random.random() < epsilon:
                # 随机选择动作：发现可能存在但尚未被发现的高奖励路径
                # Exploration: randomly select action to discover potentially better paths
                action = random.choice(range(env.actions()))
            else:
                # 贪婪选择：选择 Q 值最大的动作
                # Why called "Greedy"? 贪婪是指“只看眼前，不顾未来”：
                # 它总是选择当前 Q 表中评价最高、最有利可图的动作，而不去尝试其他可能。
                # Exploitation: select action with maximum Q-value (the "greedy" choice).
                # It's called "greedy" because it shortsightedly picks the best current option.
                action = qtable[state].index(max(qtable[state]))

            # 执行动作，获取下一状态、奖励和终止标志
            # Execute action, get next state, reward, and done flag
            next_state, reward, done = env.step(action)
            episode_reward += reward

            # 使用贝尔曼方程更新Q表：Q(s,a) = r + γ * max Q(s',a')
            # Update Q-table using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
            # 这里的 alpha 表示学习率 (Learning Rate)，控制新旧信息的平衡：
            # alpha=0: 不学习新东西；alpha=1: 完全抛弃旧知识，只看最新估计。
            # Here alpha is the Learning Rate, balancing old and new information:
            # alpha=0: learn nothing; alpha=1: completely replace old knowledge.
            # 标准公式为：Q(s,a) = (1-α)Q(s,a) + α[r + γ * max Q(s',a')]
            # 此处 alpha=1，故公式简化为直接赋值。
            qtable[state][action] = reward + gamma * max(qtable[next_state])

            # 更新当前状态为下一状态
            # Update current state to next state
            state = next_state

            # 防止无限循环的安全机制
            # Safety mechanism to prevent infinite loops
            if steps > 1000:
                break

        # 衰减探索率，随着学习进行减少随机探索
        # Decay exploration rate, reduce random exploration as learning progresses
        epsilon -= decay * epsilon

        # 打印回合总结信息
        # Print episode summary
        print(f"\nEpisode {episode + 1} finished: {steps} steps, Total Reward: {episode_reward}")
        time.sleep(0.5)

    # 返回训练好的Q表
    # Return the trained Q-table
    return qtable


def main():
    """主训练和测试程序
    Main training and testing routine"""

    # 打印程序标题
    # Print program header
    print("="*50)
    print("Lab 2: Q-Learning - Cliff Walking")
    print("Student ID: 041107730")
    print("="*50)

    # 创建悬崖行走环境
    # Create Cliff Walking environment
    env = env_module.GridEnv(size=12)

    # 设置训练回合数为50
    # Set number of training episodes to 50
    # 原因：50回合足够让智能体学习到最优策略，同时训练时间适中
    # Reason: 50 episodes are sufficient for agent to learn optimal policy while keeping training time reasonable
    # 取值依据：悬崖行走问题相对简单，状态空间小（48个状态），不需要太多回合
    # Value rationale: Cliff Walking is relatively simple with small state space (48 states), doesn't need many episodes
    EPISODES = 50

    # 设置折扣因子γ=0.9
    # Set discount factor γ=0.9
    # 原因：折扣因子控制智能体对未来奖励的重视程度，γ越大越重视长期收益
    # Reason: Discount factor controls how much agent values future rewards, larger γ means more emphasis on long-term gains
    # 取值依据：0.9是常用值，既考虑未来奖励（避免短视），又不让未来奖励权重过大
    # Value rationale: 0.9 is a common value, balances future rewards (avoiding myopia) without overweighting distant rewards
    GAMMA = 0.9

    # 设置初始探索率ε=0.1
    # Set initial exploration rate ε=0.1
    # 原因：探索率决定随机探索vs利用已学知识的平衡，避免过早陷入局部最优
    # Reason: Exploration rate balances random exploration vs exploitation of learned knowledge, avoids premature local optima
    # 取值依据：0.1表示10%探索90%利用，配合衰减策略，初期探索不会过度干扰学习
    # Value rationale: 0.1 means 10% exploration 90% exploitation, with decay strategy, initial exploration won't overly disrupt learning
    EPSILON = 0.1

    # 设置探索率衰减系数=0.5
    # Set exploration rate decay factor=0.5
    # 原因：随着训练进行，智能体应该减少随机探索，更多利用已学知识
    # Reason: As training progresses, agent should reduce random exploration and exploit learned knowledge more
    # 取值依据：0.5使ε快速衰减（每回合减半一半），早期充分探索，后期快速收敛
    # Value rationale: 0.5 causes ε to decay rapidly (halving the difference each episode), thorough early exploration, fast late convergence
    DECAY = 0.5

    # 设置步长参数α=1.0（完全更新）
    # Set step-size parameter α=1.0 (full update)
    # 原因：α控制新旧Q值的混合比例，α=1表示完全用新值替换旧值
    # Reason: α controls mix ratio of new and old Q-values, α=1 means completely replace old with new
    # 取值依据：本问题是确定性环境，每次转移结果相同，α=1可以快速学习无需平均
    # Value rationale: This problem has deterministic environment, same transition results each time, α=1 enables fast learning without averaging
    ALPHA = 1.0

    # 打印超参数配置
    # Print hyperparameter configuration
    print(f"\nHyperparameters:")
    print(f"  Episodes: {EPISODES}")
    print(f"  Gamma (γ): {GAMMA}")
    print(f"  Epsilon (ε): {EPSILON}")
    print(f"  Decay: {DECAY}")
    print(f"  Alpha (α): {ALPHA} (step-size, for discussion)")

    # 开始训练智能体
    # Start training agent
    print("\nTraining agent...")
    qtable = train(
        env=env,
        episodes=EPISODES,
        gamma=GAMMA,
        epsilon=EPSILON,
        decay=DECAY,
        alpha=ALPHA
    )

    # 训练完成
    # Training complete
    print("\nTraining complete!")


# 程序入口点，运行主函数
# Program entry point, run main function
if __name__ == "__main__":
    main()
