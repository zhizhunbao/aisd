"""
Lab 2: Q-Learning Agent for Cliff Walking
Student ID: 041107730
Implements Q-Learning using Bellman equation: Q(s,a) = r + γ * max Q(s',a')
Modified from Hybrid Activity 1 to solve the Cliff Walking problem.
"""

# 导入操作系统模块，用于清屏操作
# 导入时间模块，用于控制动画速度
# 导入随机模块，用于探索策略中的随机动作选择
# 导入importlib模块，用于动态导入环境模块
#
# Import os module for screen clearing operations
# Import time module for controlling animation speed
# Import random module for random action selection in exploration strategy
# Import importlib module for dynamically importing environment module
import os
import time
import random
import importlib

# 动态导入悬崖行走环境模块
#
# Dynamically import the cliff walking environment module
env_module = importlib.import_module('041107730_lab2_cliff_env')


def train(env: env_module.Env, episodes: int = 50, gamma: float = 0.9,
          epsilon: float = 0.1, decay: float = 0.5, alpha: float = 1.0,
          render_training: bool = False) -> list[list[float]]:
    """
    训练Q-Learning智能体

    参数:
        env: 环境实例
        episodes: 训练回合数
        gamma: 折扣因子，决定未来奖励的重要性
        epsilon: 初始探索率，控制随机探索的概率
        decay: epsilon衰减率，随训练进行减少探索
        alpha: 步长超参数（用于讨论）
        render_training: 是否显示实时可视化

    返回:
        qtable: 训练好的Q表

    ----

    Train Q-Learning agent

    Args:
        env: Environment instance
        episodes: Number of training episodes
        gamma: Discount factor, determines importance of future rewards
        epsilon: Initial exploration rate, controls probability of random exploration
        decay: Epsilon decay rate, reduces exploration as training progresses
        alpha: Step-size hyperparameter (for discussion)
        render_training: Whether to show live visualization

    Returns:
        qtable: Trained Q-table
    """

    # 初始化Q表，使用随机值
    # 原因：随机初始化可以打破对称性，帮助探索不同的状态-动作组合
    # 每个状态有4个动作（左、右、上、下），总共有 rows * cols 个状态
    #
    # Initialize Q-table with random values
    # Reason: Random initialization breaks symmetry and helps explore different state-action pairs
    # Each state has 4 actions (left, right, up, down), total of rows * cols states
    qtable = [
        [random.random() for _ in range(env.actions())]
        for _ in range(env.states())
    ]

    # 训练主循环，遍历所有回合
    #
    # Main training loop, iterate through all episodes
    for episode in range(episodes):
        # 重置环境，获取初始状态
        # 初始化步数计数器和本回合累计奖励
        #
        # Reset environment and get initial state
        # Initialize step counter and cumulative reward for this episode
        state, _, done = env.reset()
        steps = 0
        episode_reward = 0

        # 回合内循环，直到到达终止状态
        #
        # Episode loop, until reaching terminal state
        while not done:
            # 清屏并显示当前状态（与原始文章格式一致）
            # Windows用cls，其他系统用clear
            #
            # Clear screen and show current state (matching original article format)
            # Use 'cls' for Windows, 'clear' for others
            os.system('cls' if os.name == 'nt' else 'clear')

            # 打印当前回合信息
            #
            # Print current episode information
            print("episode #", episode + 1, "/", episodes)
            print(f"Steps: {steps} | Total Reward: {episode_reward} | Epsilon: {epsilon:.4f}")

            # 渲染当前环境状态
            #
            # Render current environment state
            env.render()

            # 暂停以便观察动画效果
            #
            # Pause to observe the animation
            time.sleep(0.05)

            # 增加步数计数
            #
            # Increment step count
            steps += 1

            # ε-贪婪策略：以epsilon概率随机探索，否则利用已学知识
            # 这是探索-利用权衡的核心实现
            #
            # ε-greedy policy: explore randomly with epsilon probability, otherwise exploit learned knowledge
            # This is the core implementation of exploration-exploitation trade-off
            if random.random() < epsilon:
                # 探索：随机选择动作，允许发现新的状态-动作价值
                #
                # Exploration: randomly select action, allowing discovery of new state-action values
                action = random.choice(range(env.actions()))
            else:
                # 利用：选择Q值最大的动作（贪婪策略）
                # 使用index(max(...))找到最大值对应的动作索引
                #
                # Exploitation: select action with maximum Q-value (greedy policy)
                # Use index(max(...)) to find the action index corresponding to maximum value
                action = qtable[state].index(max(qtable[state]))

            # 执行动作，获取下一状态、奖励和终止标志
            # 累加本步奖励到回合总奖励
            #
            # Execute action, get next state, reward, and done flag
            # Add step reward to episode total reward
            next_state, reward, done = env.step(action)
            episode_reward += reward

            # 使用贝尔曼方程更新Q表
            # Q(s,a) = r + γ * max_a' Q(s',a')
            # 这里alpha=1，即完全替换旧值（不使用加权平均）
            # 完整公式应为：Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
            # 当α=1时，简化为：Q(s,a) = r + γ * max Q(s',a')
            #
            # Update Q-table using Bellman equation
            # Q(s,a) = r + γ * max_a' Q(s',a')
            # Here alpha=1, meaning completely replace old value (no weighted average)
            # Full formula should be: Q(s,a) = Q(s,a) + α * [r + γ * max Q(s',a') - Q(s,a)]
            # When α=1, simplifies to: Q(s,a) = r + γ * max Q(s',a')
            qtable[state][action] = reward + gamma * max(qtable[next_state])

            # 更新当前状态为下一状态
            #
            # Update current state to next state
            state = next_state

            # 防止无限循环的安全机制
            #
            # Safety mechanism to prevent infinite loops
            if steps > 1000:
                break

        # 衰减探索率：随着学习进行，减少随机探索
        # 公式：ε_new = ε_old - decay * ε_old = ε_old * (1 - decay)
        # 原因：早期需要更多探索，后期应更多利用已学知识
        #
        # Decay exploration rate: reduce random exploration as learning progresses
        # Formula: ε_new = ε_old - decay * ε_old = ε_old * (1 - decay)
        # Reason: more exploration needed early, more exploitation of learned knowledge later
        epsilon -= decay * epsilon

        # 打印回合总结信息
        # 暂停以便查看总结
        #
        # Print episode summary
        # Pause to view the summary
        print(f"\nEpisode {episode + 1} finished: {steps} steps, Total Reward: {episode_reward}")
        time.sleep(0.5)

    # 返回训练好的Q表
    #
    # Return the trained Q-table
    return qtable


def test(env: env_module.Env, qtable: list[list[float]],
         num_episodes: int = 1, render: bool = True) -> None:
    """
    测试训练好的智能体

    参数:
        env: 环境实例
        qtable: 训练好的Q表
        num_episodes: 测试回合数
        render: 是否渲染显示

    ----

    Test trained agent

    Args:
        env: Environment instance
        qtable: Trained Q-table
        num_episodes: Number of test episodes
        render: Whether to render display
    """
    # 打印测试标题
    #
    # Print test header
    print("\n" + "="*50)
    print("Testing Trained Agent")
    print("="*50)

    # 测试循环，遍历所有测试回合
    #
    # Test loop, iterate through all test episodes
    for episode in range(num_episodes):
        # 重置环境，获取初始状态
        # 初始化步数和累计奖励
        #
        # Reset environment and get initial state
        # Initialize steps and cumulative reward
        state, _, done = env.reset()
        steps = 0
        total_reward = 0

        # 如果需要渲染，打印回合信息
        #
        # If rendering is needed, print episode information
        if render:
            print(f"\nTest Episode {episode + 1}")
            print("-" * 30)
            env.render()
            print()

        # 测试循环，直到结束或超过最大步数
        #
        # Test loop, until done or exceeding max steps
        while not done and steps < 100:
            # 测试时使用纯贪婪策略（不探索）
            # 选择Q值最大的动作
            #
            # Use pure greedy policy during testing (no exploration)
            # Select action with maximum Q-value
            action = qtable[state].index(max(qtable[state]))

            # 执行动作
            # 累加奖励和步数
            #
            # Execute action
            # Accumulate reward and steps
            state, reward, done = env.step(action)
            total_reward += reward
            steps += 1

            # 如果需要渲染，显示每步详情
            # 动作名称映射：0-左，1-右，2-上，3-下
            #
            # If rendering is needed, show step details
            # Action name mapping: 0-left, 1-right, 2-up, 3-down
            if render:
                action_names = ['LEFT', 'RIGHT', 'UP', 'DOWN']
                print(f"Step {steps}: {action_names[action]} | Reward: {reward}")
                env.render()
                print()
                # 暂停以便观察
                #
                # Pause for observation
                time.sleep(0.3)

        # 打印测试回合结果
        # 包括总步数、总回报、是否成功到达目标
        #
        # Print test episode results
        # Including total steps, total return, and whether successfully reached goal
        print(f"\nEpisode {episode + 1} finished:")
        print(f"  Steps: {steps}")
        print(f"  Return (Total Reward): {total_reward}")
        print(f"  Success: {'Yes' if done else 'No'}")


def analyze_qtable(qtable: list[list[float]], env: env_module.Env) -> None:
    """
    分析Q表在关键位置的值，用于理解智能体学到的策略

    参数:
        qtable: 训练好的Q表
        env: 环境实例

    ----

    Analyze Q-table values at key positions to understand the learned policy

    Args:
        qtable: Trained Q-table
        env: Environment instance
    """
    # 打印分析标题
    #
    # Print analysis header
    print("\n" + "="*50)
    print("Q-Table Analysis")
    print("="*50)

    # 定义动作名称
    #
    # Define action names
    action_names = ['LEFT', 'RIGHT', 'UP', 'DOWN']

    # 对于悬崖行走环境（4×12网格）
    # 起始位置在(3, 0)，状态编号 = 行号 * 列数 + 列号 = 3 * 12 + 0 = 36
    #
    # For Cliff Walking environment (4×12 grid)
    # Start position at (3, 0), state number = row * cols + col = 3 * 12 + 0 = 36
    start_state = 36
    print(f"\nStart Position (3, 0):")
    # 打印起始位置各动作的Q值
    #
    # Print Q-values for each action at start position
    for i, action in enumerate(action_names):
        print(f"  {action:6s}: {qtable[start_state][i]:8.2f}")

    # 悬崖上方位置(2, 1)，状态编号 = 2 * 12 + 1 = 25
    # 这个位置很关键，因为向下走会掉入悬崖
    #
    # Position above cliff at (2, 1), state number = 2 * 12 + 1 = 25
    # This position is critical because moving down will fall into cliff
    cliff_above = 25
    print(f"\nAbove Cliff (2, 1):")
    # 打印悬崖上方位置各动作的Q值
    #
    # Print Q-values for each action at position above cliff
    for i, action in enumerate(action_names):
        print(f"  {action:6s}: {qtable[cliff_above][i]:8.2f}")


def main():
    """
    主训练和测试程序

    ----

    Main training and testing routine
    """
    # ==================== Step 1: Print Program Header ====================
    # 打印程序标题
    #
    # Print program header
    print("="*50)
    print("Lab 2: Q-Learning - Cliff Walking")
    print("Student ID: 041107730")
    print("="*50)

    # ==================== Step 2: Create Environment ====================
    # 创建悬崖行走环境
    # size参数未使用，但为了兼容性保留
    #
    # Create Cliff Walking environment
    # Size parameter not used, but kept for compatibility
    env = env_module.GridEnv(size=12)

    # ==================== Step 3: Set Hyperparameters ====================
    # 训练回合数（原始设置：50回合）
    #
    # Number of training episodes (original setting: 50 episodes)
    EPISODES = 50

    # 折扣因子γ：决定未来奖励的重要性
    # γ=0.9表示未来奖励会被打9折，越远的奖励折扣越多
    #
    # Discount factor γ: determines the importance of future rewards
    # γ=0.9 means future rewards are discounted by 10%, more discount for more distant rewards
    GAMMA = 0.9

    # 初始探索率ε：以此概率选择随机动作
    # ε=0.1表示10%的概率随机探索，90%的概率利用已学知识
    #
    # Initial exploration rate ε: probability of selecting random action
    # ε=0.1 means 10% probability for random exploration, 90% for exploitation
    EPSILON = 0.1

    # 探索率衰减系数：每回合后ε减少的比例
    # 衰减使智能体从探索逐渐转向利用
    #
    # Exploration rate decay factor: proportion by which ε decreases after each episode
    # Decay shifts agent from exploration to exploitation gradually
    DECAY = 0.5

    # 步长超参数α：学习率（本代码中α=1，即完全更新）
    # α控制新旧Q值的混合比例，α=1表示完全用新值替换旧值
    #
    # Step-size hyperparameter α: learning rate (α=1 in this code, meaning full update)
    # α controls the mix ratio of new and old Q-values, α=1 means completely replace old with new
    ALPHA = 1.0

    # ==================== Step 4: Print Hyperparameters ====================
    # 打印超参数配置
    #
    # Print hyperparameter configuration
    print(f"\nHyperparameters:")
    print(f"  Episodes: {EPISODES}")
    print(f"  Gamma (γ): {GAMMA}")
    print(f"  Epsilon (ε): {EPSILON}")
    print(f"  Decay: {DECAY}")
    print(f"  Alpha (α): {ALPHA} (step-size, for discussion)")

    # ==================== Step 5: Train Agent ====================
    # 开始训练智能体（带实时可视化）
    # 调用训练函数，传入所有超参数
    #
    # Start training agent (with live visualization)
    # Call training function with all hyperparameters
    print("\nTraining agent...")
    qtable = train(
        env=env,
        episodes=EPISODES,
        gamma=GAMMA,
        epsilon=EPSILON,
        decay=DECAY,
        alpha=ALPHA
    )

    # ==================== Step 6: Training Complete ====================
    # 训练完成
    #
    # Training complete
    print("\nTraining complete!")


# 程序入口点
# 运行主函数
#
# Program entry point
# Run main function
if __name__ == "__main__":
    main()
