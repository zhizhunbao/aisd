"""
Week 5: DQN (Deep Q-Network) 完整演示
Week 5: DQN Complete Demo

演示内容 (Demo Contents):
1. Q-Table vs DQN 的对比 — 为什么需要 DQN
2. DQN 核心组件可视化 — Target Network, Replay Buffer, ε-Greedy
3. DQN 训练流程动画 — 6 步训练循环
4. MultiDiscrete → Discrete 展平演示
5. DQN 在 CartPole 上的训练与评估

依赖 (Dependencies): numpy, matplotlib, gymnasium, stable-baselines3
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# === 路径设置 (Path Setup) ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "week5_dqn_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(fig, name):
    """保存图片并关闭 (Save figure and close)"""
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Saved: {name}")


# ============================================================
# Demo 1: Q-Table vs DQN — 状态空间爆炸问题
# Demo 1: Q-Table vs DQN — State Space Explosion
# ============================================================
def demo1_qtable_vs_dqn():
    """展示 Q-Table 在大状态空间下的内存爆炸问题"""
    print("\n📊 Demo 1: Q-Table vs DQN — 状态空间爆炸")

    # 不同环境规模下的状态数量
    # State counts for different environment sizes
    env_sizes = ['2×4', '4×4', '5×5', '6×6', '8×8', '10×10']
    # 近似状态数（排列组合）
    state_counts = [24, 4_096, 120_000, 1_200_000, 100_000_000, 10_000_000_000]
    # Q-Table 内存（假设每个 Q 值 8 bytes, 4 个动作）
    qtable_memory_mb = [s * 4 * 8 / 1e6 for s in state_counts]
    # DQN 网络参数（固定大小，如 2 层 64 节点 MLP）
    dqn_params = 64 * 64 + 64 * 4  # ~4K 参数，固定
    dqn_memory_mb = [dqn_params * 8 / 1e6] * len(env_sizes)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 左图：状态数量增长
    # Left: State count growth
    colors = ['#2ecc71' if s < 10000 else '#f39c12' if s < 1e6 else '#e74c3c'
              for s in state_counts]
    bars = ax1.bar(env_sizes, state_counts, color=colors, edgecolor='black', linewidth=0.5)
    ax1.set_yscale('log')
    ax1.set_ylabel('状态数量 (State Count)', fontsize=11)
    ax1.set_xlabel('环境规模 (Environment Size)', fontsize=11)
    ax1.set_title('状态空间随环境规模指数增长\nState Space Grows Exponentially', fontsize=12)
    ax1.axhline(y=1e6, color='red', linestyle='--', alpha=0.5, label='Q-Table 实际上限 (~1M)')
    ax1.legend(fontsize=9)

    # 添加数值标签
    for bar, count in zip(bars, state_counts):
        if count >= 1e9:
            label = f'{count/1e9:.0f}B'
        elif count >= 1e6:
            label = f'{count/1e6:.0f}M'
        elif count >= 1e3:
            label = f'{count/1e3:.0f}K'
        else:
            label = str(count)
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() * 1.5,
                label, ha='center', va='bottom', fontsize=9, fontweight='bold')

    # 右图：内存对比
    # Right: Memory comparison
    x = np.arange(len(env_sizes))
    width = 0.35
    ax2.bar(x - width/2, qtable_memory_mb, width, label='Q-Table', color='#e74c3c', alpha=0.8)
    ax2.bar(x + width/2, dqn_memory_mb, width, label='DQN (~4K params)', color='#3498db', alpha=0.8)
    ax2.set_yscale('log')
    ax2.set_xticks(x)
    ax2.set_xticklabels(env_sizes)
    ax2.set_ylabel('内存 Memory (MB)', fontsize=11)
    ax2.set_xlabel('环境规模 (Environment Size)', fontsize=11)
    ax2.set_title('内存需求对比\nMemory Requirement Comparison', fontsize=12)
    ax2.legend(fontsize=10)

    fig.suptitle('Demo 1: 为什么需要 DQN？— Q-Table 的维度灾难',
                 fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo1_qtable_vs_dqn.png")


# ============================================================
# Demo 2: DQN 四大组件可视化
# Demo 2: DQN Four Components Visualization
# ============================================================
def demo2_dqn_components():
    """可视化 DQN 的四大核心组件"""
    print("\n📊 Demo 2: DQN 四大组件")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # --- 2a: Q-Network 结构 ---
    ax = axes[0, 0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Q-Network\n输入状态 → 输出 Q 值', fontsize=11, fontweight='bold')

    # 输入层
    for i, label in enumerate(['s₁', 's₂', 's₃', 's₄']):
        circle = plt.Circle((1.5, 6.5 - i * 1.5), 0.4, color='#3498db', alpha=0.8)
        ax.add_patch(circle)
        ax.text(1.5, 6.5 - i * 1.5, label, ha='center', va='center', fontsize=9, color='white')

    # 隐藏层
    for i in range(3):
        circle = plt.Circle((5, 6 - i * 2), 0.4, color='#9b59b6', alpha=0.8)
        ax.add_patch(circle)
        ax.text(5, 6 - i * 2, f'h{i+1}', ha='center', va='center', fontsize=9, color='white')

    # 输出层
    for i, label in enumerate(['Q(a₁)', 'Q(a₂)', 'Q(a₃)']):
        circle = plt.Circle((8.5, 5.5 - i * 2), 0.4, color='#e74c3c', alpha=0.8)
        ax.add_patch(circle)
        ax.text(8.5, 5.5 - i * 2, label, ha='center', va='center', fontsize=7, color='white')

    # 连接线
    for i in range(4):
        for j in range(3):
            ax.plot([1.9, 4.6], [6.5 - i*1.5, 6 - j*2], 'gray', alpha=0.2, linewidth=0.5)
    for i in range(3):
        for j in range(3):
            ax.plot([5.4, 8.1], [6 - i*2, 5.5 - j*2], 'gray', alpha=0.2, linewidth=0.5)

    ax.text(1.5, 0.5, 'Input: State', ha='center', fontsize=9, color='#3498db')
    ax.text(8.5, 0.5, 'Output: Q-values', ha='center', fontsize=9, color='#e74c3c')

    # --- 2b: Target Network 稳定性 ---
    ax = axes[0, 1]
    np.random.seed(42)
    steps = np.arange(100)
    # 无 Target Network：目标不断漂移
    no_target = np.cumsum(np.random.randn(100) * 0.5) + 5
    # 有 Target Network：目标分段稳定
    with_target = np.zeros(100)
    current_target = 5.0
    for i in range(100):
        if i % 20 == 0:  # 每 20 步同步一次
            current_target = no_target[i] + np.random.randn() * 0.3
        with_target[i] = current_target + np.random.randn() * 0.1

    ax.plot(steps, no_target, 'r-', alpha=0.7, label='无 Target Network\n(目标不断漂移)', linewidth=1.5)
    ax.plot(steps, with_target, 'b-', alpha=0.7, label='有 Target Network\n(目标分段稳定)', linewidth=1.5)
    for i in range(0, 100, 20):
        ax.axvline(x=i, color='blue', linestyle=':', alpha=0.3)
    ax.set_xlabel('训练步数 (Training Steps)', fontsize=10)
    ax.set_ylabel('目标 Q 值 (Target Q-value)', fontsize=10)
    ax.set_title('Target Network 稳定训练目标\nTarget Network Stabilizes Training', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')

    # --- 2c: Replay Buffer 打破相关性 ---
    ax = axes[1, 0]
    np.random.seed(123)
    # 顺序数据：高度相关
    sequential = np.array([1,1,1,2,2,2,3,3,3,4,4,4,5,5,5])
    # 随机采样：打破相关性
    shuffled = np.random.permutation(sequential)

    x_pos = np.arange(len(sequential))
    colors_seq = plt.cm.Set1(sequential / 6)
    colors_shuf = plt.cm.Set1(shuffled / 6)

    ax.bar(x_pos - 0.2, sequential, 0.35, color=colors_seq, edgecolor='black',
           linewidth=0.5, label='顺序学习 (Sequential)')
    ax.bar(x_pos + 0.2, shuffled, 0.35, color=colors_shuf, edgecolor='black',
           linewidth=0.5, label='随机采样 (Random Sampling)')
    ax.set_xlabel('样本索引 (Sample Index)', fontsize=10)
    ax.set_ylabel('环境区域 (Environment Region)', fontsize=10)
    ax.set_title('Replay Buffer 打破样本相关性\nReplay Buffer Breaks Correlation', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)

    # --- 2d: ε-Greedy 衰减 ---
    ax = axes[1, 1]
    total_steps = 100000
    exploration_fraction = 0.1
    eps_start = 1.0
    eps_end = 0.05
    decay_steps = int(total_steps * exploration_fraction)

    steps = np.arange(total_steps)
    epsilon = np.where(
        steps < decay_steps,
        eps_start - (eps_start - eps_end) * steps / decay_steps,
        eps_end
    )

    ax.plot(steps, epsilon, 'g-', linewidth=2)
    ax.fill_between(steps, epsilon, alpha=0.1, color='green')
    ax.axhline(y=eps_end, color='red', linestyle='--', alpha=0.5, label=f'ε_final = {eps_end}')
    ax.axvline(x=decay_steps, color='orange', linestyle='--', alpha=0.5,
               label=f'衰减结束 @ {decay_steps:,} steps')
    ax.set_xlabel('训练步数 (Training Steps)', fontsize=10)
    ax.set_ylabel('ε (探索概率)', fontsize=10)
    ax.set_title('ε-Greedy 探索衰减\nε-Greedy Exploration Decay', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.annotate('探索为主\n(Exploration)', xy=(decay_steps*0.3, 0.7),
                fontsize=9, ha='center', color='green')
    ax.annotate('利用为主\n(Exploitation)', xy=(total_steps*0.6, 0.15),
                fontsize=9, ha='center', color='red')

    fig.suptitle('Demo 2: DQN 四大核心组件', fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo2_dqn_components.png")


# ============================================================
# Demo 3: MultiDiscrete → Discrete 展平
# Demo 3: MultiDiscrete to Discrete Flattening
# ============================================================
def demo3_action_flattening():
    """演示 MultiDiscrete 到 Discrete 的动作空间展平"""
    print("\n📊 Demo 3: MultiDiscrete → Discrete 展平")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # 左图：MultiDiscrete([3, 4]) 的网格映射
    dims = (3, 4)
    ax1.set_xlim(-0.5, dims[1] - 0.5)
    ax1.set_ylim(-0.5, dims[0] - 0.5)

    for i in range(dims[0]):
        for j in range(dims[1]):
            flat_idx = i * dims[1] + j
            color = plt.cm.viridis(flat_idx / (dims[0] * dims[1]))
            rect = mpatches.FancyBboxPatch(
                (j - 0.4, i - 0.4), 0.8, 0.8,
                boxstyle="round,pad=0.05", facecolor=color, edgecolor='black', linewidth=1
            )
            ax1.add_patch(rect)
            ax1.text(j, i + 0.15, f'({i},{j})', ha='center', va='center',
                    fontsize=9, color='white', fontweight='bold')
            ax1.text(j, i - 0.15, f'→ {flat_idx}', ha='center', va='center',
                    fontsize=8, color='yellow')

    ax1.set_xlabel('维度 2 (dim[1] = 4)', fontsize=11)
    ax1.set_ylabel('维度 1 (dim[0] = 3)', fontsize=11)
    ax1.set_title('MultiDiscrete([3, 4]) → Discrete(12)\n多维索引 → 整数映射', fontsize=12, fontweight='bold')
    ax1.set_xticks(range(dims[1]))
    ax1.set_yticks(range(dims[0]))
    ax1.invert_yaxis()

    # 右图：np.unravel_index 还原示例
    examples = [(0, (0,0)), (5, (1,1)), (7, (1,3)), (11, (2,3))]
    y_positions = [3, 2, 1, 0]

    for (flat, multi), y in zip(examples, y_positions):
        # 整数动作
        ax2.add_patch(mpatches.FancyBboxPatch(
            (0.5, y - 0.3), 1.5, 0.6,
            boxstyle="round,pad=0.1", facecolor='#3498db', edgecolor='black'
        ))
        ax2.text(1.25, y, f'{flat}', ha='center', va='center',
                fontsize=14, color='white', fontweight='bold')

        # 箭头
        ax2.annotate('', xy=(3.0, y), xytext=(2.2, y),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))
        ax2.text(2.6, y + 0.25, 'unravel', ha='center', fontsize=8, style='italic')

        # 多维索引
        ax2.add_patch(mpatches.FancyBboxPatch(
            (3.0, y - 0.3), 2.0, 0.6,
            boxstyle="round,pad=0.1", facecolor='#e74c3c', edgecolor='black'
        ))
        ax2.text(4.0, y, f'({multi[0]}, {multi[1]})', ha='center', va='center',
                fontsize=14, color='white', fontweight='bold')

    ax2.set_xlim(0, 5.5)
    ax2.set_ylim(-0.8, 3.8)
    ax2.axis('off')
    ax2.set_title('np.unravel_index(flat, (3,4))\n整数 → 多维索引还原', fontsize=12, fontweight='bold')

    fig.suptitle('Demo 3: DiscreteActionWrapper 动作空间展平',
                 fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo3_action_flattening.png")


# ============================================================
# Demo 4: DQN 训练流程图
# Demo 4: DQN Training Process Diagram
# ============================================================
def demo4_training_process():
    """可视化 DQN 的 6 步训练流程"""
    print("\n📊 Demo 4: DQN 训练流程")

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')

    steps = [
        (1, 8.5, '① 交互收集\nInteraction', '#3498db',
         'Agent ↔ Env\n→ (s,a,r,s\') → Buffer'),
        (5, 8.5, '② 预热\nWarm-up', '#f39c12',
         'Random actions\n× learning_starts'),
        (9, 8.5, '③ 采样\nSampling', '#2ecc71',
         'Random mini-batch\nfrom Buffer'),
        (1, 4.5, '④ 计算目标\nTarget Calc', '#e74c3c',
         'y = r + γ max Q_target\n(用 Target Network!)'),
        (5, 4.5, '⑤ 更新主网络\nUpdate Main', '#9b59b6',
         'Loss = MSE(Q, y)\n反向传播'),
        (9, 4.5, '⑥ 同步目标网络\nSync Target', '#1abc9c',
         'Q_target ← Q_main\n(每 N 步)'),
    ]

    for x, y, title, color, desc in steps:
        # 方框
        rect = mpatches.FancyBboxPatch(
            (x - 1.3, y - 1.2), 2.6, 2.4,
            boxstyle="round,pad=0.2", facecolor=color, alpha=0.15,
            edgecolor=color, linewidth=2
        )
        ax.add_patch(rect)
        # 标题
        ax.text(x, y + 0.5, title, ha='center', va='center',
               fontsize=10, fontweight='bold', color=color)
        # 描述
        ax.text(x, y - 0.4, desc, ha='center', va='center',
               fontsize=8, color='#333333')

    # 箭头连接
    arrow_props = dict(arrowstyle='->', color='gray', lw=1.5)
    # 行1: ① → ② → ③
    ax.annotate('', xy=(3.5, 8.5), xytext=(2.5, 8.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 8.5), xytext=(6.5, 8.5), arrowprops=arrow_props)
    # 行1→行2: ③ → ④
    ax.annotate('', xy=(9, 6.0), xytext=(9, 7.0), arrowprops=arrow_props)
    ax.text(9.5, 6.5, '↓', fontsize=14, color='gray')
    # 行2: ④ → ⑤ → ⑥
    ax.annotate('', xy=(3.5, 4.5), xytext=(2.5, 4.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 4.5), xytext=(6.5, 4.5), arrowprops=arrow_props)

    # 循环箭头 ⑥ → ①
    ax.annotate('', xy=(1, 7.0), xytext=(9, 3.0),
               arrowprops=dict(arrowstyle='->', color='#e67e22', lw=2,
                              connectionstyle='arc3,rad=0.3'))
    ax.text(5, 1.5, '🔄 重复直到 total_timesteps 完成', ha='center',
           fontsize=11, color='#e67e22', fontweight='bold')

    ax.set_title('Demo 4: DQN 训练 6 步循环', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, "demo4_training_process.png")


# ============================================================
# Demo 5: DQN 在 CartPole 上训练
# Demo 5: DQN Training on CartPole
# ============================================================
def demo5_dqn_cartpole():
    """在 CartPole-v1 上训练 DQN 并可视化学习曲线"""
    print("\n📊 Demo 5: DQN 在 CartPole 上训练")

    try:
        import gymnasium as gym
        from stable_baselines3 import DQN
        from stable_baselines3.common.evaluation import evaluate_policy
    except ImportError:
        print("  ⚠️ 需要 gymnasium 和 stable-baselines3，跳过此 demo")
        # 生成模拟数据
        _demo5_simulated()
        return

    # 训练 DQN
    env = gym.make("CartPole-v1")
    model = DQN(
        "MlpPolicy", env,
        learning_rate=1e-3,
        buffer_size=50000,
        learning_starts=1000,
        batch_size=64,
        gamma=0.99,
        target_update_interval=500,
        verbose=0
    )

    # 记录训练过程中的奖励
    eval_rewards = []
    eval_steps = []
    step_interval = 2000
    total_steps = 30000

    for step in range(0, total_steps, step_interval):
        model.learn(total_timesteps=step_interval, reset_num_timesteps=False)
        mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
        eval_rewards.append(mean_reward)
        eval_steps.append(step + step_interval)
        print(f"  Step {step + step_interval:>6}: reward = {mean_reward:.1f} ± {std_reward:.1f}")

    env.close()

    # 可视化
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(eval_steps, eval_rewards, 'b-o', markersize=4, linewidth=2, label='DQN Mean Reward')
    ax.fill_between(eval_steps,
                    [r - 20 for r in eval_rewards],
                    [r + 20 for r in eval_rewards],
                    alpha=0.2, color='blue')
    ax.axhline(y=500, color='green', linestyle='--', alpha=0.5, label='Max Reward (500)')
    ax.axhline(y=195, color='orange', linestyle='--', alpha=0.5, label='Solved Threshold (195)')
    ax.set_xlabel('训练步数 (Training Steps)', fontsize=11)
    ax.set_ylabel('平均奖励 (Mean Reward)', fontsize=11)
    ax.set_title('Demo 5: DQN 在 CartPole-v1 上的学习曲线\nDQN Learning Curve on CartPole-v1',
                fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    save_fig(fig, "demo5_dqn_cartpole.png")


def _demo5_simulated():
    """当 SB3 不可用时，用模拟数据生成图表"""
    np.random.seed(42)
    steps = np.arange(2000, 32000, 2000)
    # 模拟学习曲线：从低到高
    rewards = 50 + 400 * (1 - np.exp(-steps / 10000)) + np.random.randn(len(steps)) * 20
    rewards = np.clip(rewards, 0, 500)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(steps, rewards, 'b-o', markersize=4, linewidth=2, label='DQN Mean Reward (simulated)')
    ax.fill_between(steps, rewards - 20, rewards + 20, alpha=0.2, color='blue')
    ax.axhline(y=500, color='green', linestyle='--', alpha=0.5, label='Max Reward (500)')
    ax.axhline(y=195, color='orange', linestyle='--', alpha=0.5, label='Solved Threshold (195)')
    ax.set_xlabel('训练步数 (Training Steps)', fontsize=11)
    ax.set_ylabel('平均奖励 (Mean Reward)', fontsize=11)
    ax.set_title('Demo 5: DQN 学习曲线 (模拟数据)\nDQN Learning Curve (Simulated)',
                fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    save_fig(fig, "demo5_dqn_cartpole.png")


# ============================================================
# 主程序 (Main)
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 5: DQN 完整演示 (Complete Demo)")
    print("=" * 60)

    demo1_qtable_vs_dqn()
    demo2_dqn_components()
    demo3_action_flattening()
    demo4_training_process()
    demo5_dqn_cartpole()

    print("\n" + "=" * 60)
    print(f"✅ 所有图片已保存到: {OUTPUT_DIR}")
    print("=" * 60)
