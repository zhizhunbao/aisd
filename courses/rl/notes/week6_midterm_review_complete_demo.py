"""
Week 6: 期中复习完整演示 — Weeks 1-5 核心概念可视化
Week 6: Midterm Review Complete Demo — Weeks 1-5 Core Concepts Visualization

演示内容 (Demo Contents):
1. RL 框架图 — Agent-Environment 交互循环
2. MDP 与 Bellman 方程 — Q 值传播可视化
3. Q-Learning 训练过程 — CliffWalking 上的 Q-Learning vs SARSA
4. ε-Greedy 与 Q 表初始化 — 探索策略对比
5. Gymnasium → SB3 → DQN 技术演进路线图

依赖 (Dependencies): numpy, matplotlib
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# === 路径设置 (Path Setup) ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "week6_midterm_review_complete_demo_pages")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(fig, name):
    """保存图片并关闭 (Save figure and close)"""
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ Saved: {name}")


# ============================================================
# Demo 1: RL 框架图 — Agent-Environment 交互循环
# Demo 1: RL Framework — Agent-Environment Interaction Loop
# ============================================================
def demo1_rl_framework():
    """
    可视化 RL 核心框架图 (Midterm Slide 5 必考)
    Visualize the core RL framework diagram (Midterm Slide 5 required)

    核心概念 (Core Concepts):
    - Agent: 学习者/决策者 | Learner/decision-maker
    - Environment: Agent 交互的外部世界 | External world
    - State/Observation: 环境的描述 | Description of environment
    - Action: Agent 的决策 | Agent's decision
    - Reward: 标量反馈信号 | Scalar feedback signal
    """
    print("\n📊 Demo 1: RL 框架图 — Agent-Environment 交互")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- 左图: Agent-Environment 交互循环 ---
    ax = ax1
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('RL 核心框架: Agent-Environment 交互\nCore RL Framework: Agent-Environment Interaction',
                 fontsize=12, fontweight='bold')

    # Agent 方框
    agent_box = mpatches.FancyBboxPatch(
        (1, 4.5), 3, 2, boxstyle="round,pad=0.3",
        facecolor='#3498db', alpha=0.2, edgecolor='#3498db', linewidth=2
    )
    ax.add_patch(agent_box)
    ax.text(2.5, 5.8, 'Agent (智能体)', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#2c3e50')
    ax.text(2.5, 5.0, 'Policy π(a|s)\nValue V(s) / Q(s,a)\n[Model]',
            ha='center', va='center', fontsize=9, color='#34495e')

    # Environment 方框
    env_box = mpatches.FancyBboxPatch(
        (6, 4.5), 3, 2, boxstyle="round,pad=0.3",
        facecolor='#2ecc71', alpha=0.2, edgecolor='#2ecc71', linewidth=2
    )
    ax.add_patch(env_box)
    ax.text(7.5, 5.8, 'Environment (环境)', ha='center', va='center',
            fontsize=12, fontweight='bold', color='#2c3e50')
    ax.text(7.5, 5.0, 'State S\nTransition P(s\'|s,a)\nReward R(s,a)',
            ha='center', va='center', fontsize=9, color='#34495e')

    # Action 箭头 (Agent → Environment)
    ax.annotate('', xy=(6, 6.2), xytext=(4, 6.2),
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2.5))
    ax.text(5, 6.6, 'Action $a_t$', ha='center', va='center',
            fontsize=11, color='#e74c3c', fontweight='bold')

    # Reward + State 箭头 (Environment → Agent)
    ax.annotate('', xy=(4, 4.2), xytext=(6, 4.2),
                arrowprops=dict(arrowstyle='->', color='#f39c12', lw=2.5))
    ax.text(5, 3.6, 'Reward $R_{t+1}$ + State $S_{t+1}$', ha='center', va='center',
            fontsize=11, color='#f39c12', fontweight='bold')

    # 时间步标注
    ax.text(5, 2.5, 'Repeat at each timestep t:',
            ha='center', va='center', fontsize=10, style='italic', color='gray')
    ax.text(5, 1.5, r'$S_t \overset{\pi}{\rightarrow} A_t \overset{env}{\rightarrow} R_{t+1}, S_{t+1}$',
            ha='center', va='center', fontsize=12, color='#2c3e50')

    # --- 右图: Agent 三大组件分类 ---
    ax = ax2
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Agent 分类: 三大组件\nAgent Taxonomy: Three Components',
                 fontsize=12, fontweight='bold')

    # 表格数据
    categories = [
        ('Value Based\n基于价值', '❌ 隐式', '✅', '可选', '#3498db'),
        ('Policy Based\n基于策略', '✅', '❌', '可选', '#e74c3c'),
        ('Actor-Critic\n演员-评论家', '✅ actor', '✅ critic', '可选', '#9b59b6'),
        ('Model Free\n无模型', 'π/V/Q', 'π/V/Q', '❌', '#f39c12'),
        ('Model Based\n基于模型', 'π/V/Q', 'π/V/Q', '✅', '#2ecc71'),
    ]

    # 表头
    headers = ['类型 Type', 'Policy π', 'Value V/Q', 'Model']
    header_x = [1.5, 4.5, 6.5, 8.5]
    for x, h in zip(header_x, headers):
        ax.text(x, 7.3, h, ha='center', va='center', fontsize=10,
                fontweight='bold', color='#2c3e50')
    ax.plot([0.3, 9.7], [7.0, 7.0], 'k-', linewidth=1.5)

    # 数据行
    for i, (name, policy, value, model, color) in enumerate(categories):
        y = 6.2 - i * 1.2
        # 背景色
        rect = mpatches.FancyBboxPatch(
            (0.3, y - 0.45), 9.4, 0.9,
            boxstyle="round,pad=0.05", facecolor=color, alpha=0.08
        )
        ax.add_patch(rect)
        ax.text(1.5, y, name, ha='center', va='center', fontsize=9, color=color, fontweight='bold')
        ax.text(4.5, y, policy, ha='center', va='center', fontsize=9)
        ax.text(6.5, y, value, ha='center', va='center', fontsize=9)
        ax.text(8.5, y, model, ha='center', va='center', fontsize=9)

    # Q-Learning 标注
    ax.text(5, 0.5, '💡 Q-Learning = Value Based + Model Free',
            ha='center', va='center', fontsize=11, fontweight='bold',
            color='#e67e22',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffeaa7', alpha=0.5))

    fig.tight_layout()
    save_fig(fig, "demo1_rl_framework.png")


# ============================================================
# Demo 2: MDP 与 Bellman 方程 — Q 值传播可视化
# Demo 2: MDP & Bellman Equation — Q-Value Propagation
# ============================================================
def demo2_bellman_equation():
    """
    可视化 Bellman 方程的 Q 值传播过程
    Visualize Bellman equation Q-value propagation

    核心公式 (Core Formula):
    Q(s,a) = R + γ * max_a' Q(s', a')

    Q-Learning 更新 (Update Rule):
    Q(s,a) ← Q(s,a) + α * [R + γ * max Q(s',a') - Q(s,a)]
    """
    print("\n📊 Demo 2: Bellman 方程 — Q 值传播")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- 左图: Bellman 方程图解 ---
    ax = ax1
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Bellman 方程图解\nBellman Equation Illustrated',
                 fontsize=12, fontweight='bold')

    # 当前状态 s
    circle_s = plt.Circle((2, 5), 0.8, color='#3498db', alpha=0.3, edgecolor='#3498db', linewidth=2)
    ax.add_patch(circle_s)
    ax.text(2, 5, '$s$', ha='center', va='center', fontsize=16, fontweight='bold')

    # 动作 a
    ax.annotate('', xy=(4.5, 5), xytext=(2.8, 5),
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=2))
    ax.text(3.6, 5.5, '$a$', ha='center', fontsize=14, color='#e74c3c', fontweight='bold')

    # 奖励 R
    ax.text(3.6, 4.3, '$R$', ha='center', fontsize=12, color='#f39c12', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#ffeaa7', alpha=0.5))

    # 下一状态 s'
    circle_sp = plt.Circle((6, 5), 0.8, color='#2ecc71', alpha=0.3, edgecolor='#2ecc71', linewidth=2)
    ax.add_patch(circle_sp)
    ax.text(6, 5, "$s'$", ha='center', va='center', fontsize=16, fontweight='bold')

    # s' 的动作选择 (max)
    actions_sp = [("$a'_1$", 6.8, 6.8, 3.0), ("$a'_2$", 8.5, 5.0, 7.0), ("$a'_3$", 6.8, 3.2, 2.0)]
    for label, x, y, q_val in actions_sp:
        ax.annotate('', xy=(x, y), xytext=(6.7, 5),
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
        color = '#e74c3c' if q_val == 7.0 else '#95a5a6'
        ax.text(x + 0.3, y, f'{label}\nQ={q_val}', ha='center', va='center',
                fontsize=9, color=color, fontweight='bold' if q_val == 7.0 else 'normal')

    # max 标注
    ax.text(9.2, 5.0, '← max!', ha='center', va='center', fontsize=10,
            color='#e74c3c', fontweight='bold')

    # 公式
    ax.text(5, 1.5, '$Q(s, a) = R + \\gamma \\cdot \\max_{a\'} Q(s\', a\')$',
            ha='center', va='center', fontsize=14, color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#dfe6e9', alpha=0.5))
    ax.text(5, 0.5, '例: Q(s,a) = R + 0.9 × 7.0 = R + 6.3',
            ha='center', va='center', fontsize=10, color='gray')

    # --- 右图: Q-Learning 更新步骤 ---
    ax = ax2
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Q-Learning 更新: 手算示例\nQ-Learning Update: Hand Calculation',
                 fontsize=12, fontweight='bold')

    # 给定值
    given = [
        ('Q(s,a) = 2.0', '当前 Q 值'),
        ('α = 0.1', '学习率'),
        ('R = 1', '即时奖励'),
        ('γ = 0.9', '折扣因子'),
        ('max Q(s\',a\') = 5.0', '下一状态最大 Q'),
    ]
    ax.text(5, 7.5, '已知 (Given):', ha='center', fontsize=11, fontweight='bold', color='#2c3e50')
    for i, (val, desc) in enumerate(given):
        ax.text(3, 6.8 - i * 0.5, f'• {val}', fontsize=10, color='#34495e')
        ax.text(7.5, 6.8 - i * 0.5, f'← {desc}', fontsize=9, color='gray')

    ax.plot([0.5, 9.5], [4.3, 4.3], 'k-', linewidth=0.5)

    # 计算步骤
    steps = [
        ('Step 1: TD Target', 'R + γ × max Q(s\',a\') = 1 + 0.9 × 5.0 = 5.5'),
        ('Step 2: TD Error', 'Target - Q(s,a) = 5.5 - 2.0 = 3.5'),
        ('Step 3: Update', 'Q(s,a) ← 2.0 + 0.1 × 3.5 = 2.35'),
    ]
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    for i, ((step_name, calc), color) in enumerate(zip(steps, colors)):
        y = 3.8 - i * 1.2
        ax.text(1, y, step_name, fontsize=10, fontweight='bold', color=color)
        ax.text(1, y - 0.5, calc, fontsize=10, color='#2c3e50')

    # 最终结果
    ax.text(5, 0.3, 'Q(s,a): 2.0 → 2.35  (向 TD Target 5.5 靠近了一小步)',
            ha='center', fontsize=10, fontweight='bold', color='#27ae60',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#d5f5e3', alpha=0.5))

    fig.tight_layout()
    save_fig(fig, "demo2_bellman_equation.png")


# ============================================================
# Demo 3: Q-Learning vs SARSA on CliffWalking
# Demo 3: Q-Learning vs SARSA 在 CliffWalking 上的对比
# ============================================================
def demo3_qlearning_vs_sarsa():
    """
    模拟 Q-Learning 和 SARSA 在 CliffWalking 上的行为差异 (Midterm Slide 4)
    Simulate Q-Learning vs SARSA behavior on CliffWalking

    关键区别 (Key Difference):
    - Q-Learning (off-policy): 更新用 max Q(s',a') → 学到最短路径（沿悬崖边）
    - SARSA (on-policy): 更新用 Q(s', a'_actual) → 学到安全路径（远离悬崖）
    """
    print("\n📊 Demo 3: Q-Learning vs SARSA — CliffWalking")

    # --- 4x12 CliffWalking 网格 ---
    # 状态布局:
    #   Row 0: 普通格子
    #   Row 1: 普通格子
    #   Row 2: 普通格子
    #   Row 3: [S] [cliff...cliff] [G]
    rows, cols = 4, 12

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))

    for ax_idx, (algo_name, path_color, path_coords, desc) in enumerate([
        ('Q-Learning (Off-Policy)', '#e74c3c', 
         # 最短路径：沿悬崖边走
         [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3)],
         '最短路径 (沿悬崖边)\nShortest path (along cliff)'),
        ('SARSA (On-Policy)', '#3498db',
         # 安全路径：远离悬崖
         [(0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
          (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (11, 1), (11, 2), (11, 3)],
         '安全路径 (远离悬崖)\nSafe path (away from cliff)')
    ]):
        ax = axes[ax_idx]
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        # 画网格
        for r in range(rows):
            for c in range(cols):
                color = '#ecf0f1'
                label = ''
                if r == 3 and c == 0:
                    color = '#2ecc71'
                    label = 'S'
                elif r == 3 and c == 11:
                    color = '#f1c40f'
                    label = 'G'
                elif r == 3 and 1 <= c <= 10:
                    color = '#e74c3c'
                    label = '☠'

                rect = mpatches.FancyBboxPatch(
                    (c - 0.45, r - 0.45), 0.9, 0.9,
                    boxstyle="round,pad=0.02", facecolor=color,
                    edgecolor='#bdc3c7', linewidth=0.5
                )
                ax.add_patch(rect)
                if label:
                    ax.text(c, r, label, ha='center', va='center',
                            fontsize=12 if label in ('S', 'G') else 10,
                            fontweight='bold', color='white' if label == '☠' else '#2c3e50')

        # 画路径
        for i in range(len(path_coords) - 1):
            x1, y1 = path_coords[i]
            x2, y2 = path_coords[i + 1]
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle='->', color=path_color, lw=2.5, alpha=0.8))

        ax.set_title(f'{algo_name}\n{desc}', fontsize=12, fontweight='bold', color=path_color)
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(False)

    fig.suptitle('Demo 3: Q-Learning vs SARSA — 为什么路径不同？\n'
                 'Q-Learning: max 忽略探索危险 | SARSA: 考虑 ε-greedy 随机性',
                 fontsize=13, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo3_qlearning_vs_sarsa.png")


# ============================================================
# Demo 4: ε-Greedy 与 Q 表初始化对比
# Demo 4: ε-Greedy & Q-Table Initialization Comparison
# ============================================================
def demo4_epsilon_and_qtable_init():
    """
    可视化 ε-Greedy 策略和 Q 表初始化方式的影响
    Visualize ε-Greedy policy and Q-table initialization effects

    考点 (Exam Points):
    - ε-Greedy: P(greedy) = 1-ε, P(random) = ε/|A|
    - Q 表初始化: 零初始化 vs 随机 vs 乐观初始化
    - 终止状态 Q 值必须为 0
    """
    print("\n📊 Demo 4: ε-Greedy 与 Q 表初始化")

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # --- 4a: ε-Greedy 动作概率分布 ---
    ax = axes[0]
    actions = ['$a_1$', '$a_2$\n(greedy)', '$a_3$', '$a_4$']
    q_values = [1.5, 3.0, 2.0, 0.5]
    epsilon = 0.2
    n_actions = len(actions)

    # 计算概率
    probs = [epsilon / n_actions] * n_actions
    greedy_idx = np.argmax(q_values)
    probs[greedy_idx] += (1 - epsilon)

    colors = ['#95a5a6'] * n_actions
    colors[greedy_idx] = '#e74c3c'

    bars = ax.bar(actions, probs, color=colors, edgecolor='black', linewidth=0.5, alpha=0.8)
    for bar, p in zip(bars, probs):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                f'{p:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Q 值标注
    for i, (a, q) in enumerate(zip(actions, q_values)):
        ax.text(i, -0.08, f'Q={q}', ha='center', fontsize=9, color='#7f8c8d')

    ax.set_ylabel('选择概率 P(a)', fontsize=11)
    ax.set_title(f'ε-Greedy (ε={epsilon})\n动作选择概率分布', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 1.0)
    ax.axhline(y=epsilon/n_actions, color='gray', linestyle=':', alpha=0.5, label=f'ε/|A| = {epsilon/n_actions}')
    ax.legend(fontsize=9)

    # --- 4b: ε 衰减曲线 ---
    ax = axes[1]
    episodes = np.arange(1000)
    eps_values = {
        '线性衰减 (Linear)': np.maximum(0.05, 1.0 - episodes / 500),
        '指数衰减 (Exponential)': np.maximum(0.05, 1.0 * (0.995 ** episodes)),
    }
    colors_decay = ['#3498db', '#e74c3c']
    for (name, vals), color in zip(eps_values.items(), colors_decay):
        ax.plot(episodes, vals, linewidth=2, label=name, color=color)

    ax.axhline(y=0.05, color='gray', linestyle='--', alpha=0.5, label='ε_min = 0.05')
    ax.set_xlabel('Episode', fontsize=11)
    ax.set_ylabel('ε', fontsize=11)
    ax.set_title('ε 衰减策略对比\nε Decay Strategies', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.fill_between(episodes, 0, 0.05, alpha=0.05, color='green')
    ax.text(750, 0.15, '利用为主\nExploit', fontsize=9, color='green', ha='center')
    ax.text(100, 0.7, '探索为主\nExplore', fontsize=9, color='blue', ha='center')

    # --- 4c: Q 表初始化方式对比 ---
    ax = axes[2]
    states = ['$s_0$', '$s_1$', '$s_2$', '$s_3$', '$s_T$\n(终止)']
    n_states = len(states)
    x = np.arange(n_states)
    width = 0.25

    np.random.seed(42)
    zero_init = [0, 0, 0, 0, 0]
    random_init = list(np.random.uniform(-0.5, 0.5, 4)) + [0]
    optimistic_init = [5, 5, 5, 5, 0]

    ax.bar(x - width, zero_init, width, label='零初始化 (Zero)', color='#3498db', alpha=0.8)
    ax.bar(x, random_init, width, label='随机初始化 (Random)', color='#f39c12', alpha=0.8)
    ax.bar(x + width, optimistic_init, width, label='乐观初始化 (Optimistic)', color='#e74c3c', alpha=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(states, fontsize=10)
    ax.set_ylabel('初始 Q 值', fontsize=11)
    ax.set_title('Q 表初始化方式\nQ-Table Initialization', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8, loc='upper left')
    ax.axhline(y=0, color='black', linewidth=0.5)

    # 终止状态标注
    ax.annotate('⚠️ 终止状态\n必须 = 0', xy=(4, 0), xytext=(3.5, 3),
                fontsize=9, color='#e74c3c', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5))

    fig.suptitle('Demo 4: 探索策略与 Q 表初始化', fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo4_epsilon_qtable_init.png")


# ============================================================
# Demo 5: Weeks 1-5 技术演进路线图
# Demo 5: Weeks 1-5 Technology Evolution Roadmap
# ============================================================
def demo5_evolution_roadmap():
    """
    可视化 5 周知识的因果链条和技术演进
    Visualize the 5-week causal chain and technology evolution

    Week 1: 概念 → Week 2: 数学 → Week 3: 环境 → Week 4: 框架 → Week 5: DQN
    """
    print("\n📊 Demo 5: Weeks 1-5 技术演进路线图")

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    weeks = [
        (1.5, 7.5, 'Week 1\nRL 基础', '#3498db',
         ['Agent / Env / Reward', 'Policy / Value / Model', 'Markov Property', 'Agent 分类'],
         '"什么是 RL？"'),
        (4.5, 7.5, 'Week 2\nMDP', '#2ecc71',
         ['MDP ⟨S,A,P,R,γ⟩', 'Bellman 方程', 'Q-Learning 更新', 'ε-Greedy'],
         '"怎么用数学描述？"'),
        (7.5, 7.5, 'Week 3\nGymnasium', '#f39c12',
         ['reset() / step()', 'Custom Env', 'Wrapper', 'Pygame'],
         '"在哪跑实验？"'),
        (10.5, 7.5, 'Week 4\nSB3', '#9b59b6',
         ['DQN / PPO / A2C', 'VecEnv', 'Callbacks', 'Best Practices'],
         '"有现成工具吗？"'),
        (13.5, 7.5, 'Week 5\nDQN', '#e74c3c',
         ['Q-Table → NN', 'Target Network', 'Replay Buffer', 'ε-Decay'],
         '"状态太多怎么办？"'),
    ]

    for x, y, title, color, items, question in weeks:
        # 主方框
        rect = mpatches.FancyBboxPatch(
            (x - 1.3, y - 2.8), 2.6, 5.0,
            boxstyle="round,pad=0.2", facecolor=color, alpha=0.1,
            edgecolor=color, linewidth=2
        )
        ax.add_patch(rect)

        # 标题
        ax.text(x, y + 1.5, title, ha='center', va='center',
                fontsize=11, fontweight='bold', color=color)

        # 问题（动机）
        ax.text(x, y + 0.3, question, ha='center', va='center',
                fontsize=8, style='italic', color='#7f8c8d')

        # 知识点
        for i, item in enumerate(items):
            ax.text(x, y - 0.5 - i * 0.55, f'• {item}', ha='center', va='center',
                    fontsize=8, color='#2c3e50')

    # 箭头连接
    for i in range(4):
        x_start = weeks[i][0] + 1.3
        x_end = weeks[i + 1][0] - 1.3
        ax.annotate('', xy=(x_end, 7.5), xytext=(x_start, 7.5),
                    arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))

    # 底部：因果链总结
    ax.text(7.5, 0.8, '因果链: 概念 → 数学模型 → 标准环境 → 工业框架 → 深度 RL',
            ha='center', va='center', fontsize=12, fontweight='bold', color='#2c3e50',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#dfe6e9', alpha=0.5))
    ax.text(7.5, 0.1, 'Causal Chain: Concepts → Math Model → Standard Env → Industrial Framework → Deep RL',
            ha='center', va='center', fontsize=10, color='gray')

    ax.set_title('Demo 5: Weeks 1-5 知识演进路线图', fontsize=14, fontweight='bold', pad=20)
    save_fig(fig, "demo5_evolution_roadmap.png")


# ============================================================
# Demo 6: Gymnasium API 速查图
# Demo 6: Gymnasium API Quick Reference
# ============================================================
def demo6_gymnasium_api():
    """
    可视化 Gymnasium 核心 API 和 step() 返回值 (Midterm Slide 7-8)
    Visualize Gymnasium core API and step() return values
    """
    print("\n📊 Demo 6: Gymnasium API 速查")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # --- 左图: Gymnasium 交互循环 ---
    ax = ax1
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('Gymnasium 交互循环\nGymnasium Interaction Loop', fontsize=12, fontweight='bold')

    # env.reset()
    reset_box = mpatches.FancyBboxPatch(
        (1, 6), 3, 1.2, boxstyle="round,pad=0.2",
        facecolor='#2ecc71', alpha=0.2, edgecolor='#2ecc71', linewidth=2
    )
    ax.add_patch(reset_box)
    ax.text(2.5, 6.6, 'env.reset()', ha='center', fontsize=11, fontweight='bold', color='#27ae60', family='monospace')
    ax.text(2.5, 6.2, '→ (state, info)', ha='center', fontsize=9, color='#2c3e50', family='monospace')

    # 箭头 reset → loop
    ax.annotate('', xy=(5, 4.5), xytext=(2.5, 5.8),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    # env.step() 循环
    step_box = mpatches.FancyBboxPatch(
        (3, 2.5), 4.5, 3.5, boxstyle="round,pad=0.2",
        facecolor='#3498db', alpha=0.1, edgecolor='#3498db', linewidth=2
    )
    ax.add_patch(step_box)
    ax.text(5.25, 5.5, '🔄 Episode Loop', ha='center', fontsize=10, fontweight='bold', color='#2980b9')

    # 选动作
    ax.text(5.25, 4.8, '1. action = select(state)', ha='center', fontsize=9, family='monospace')
    # step
    ax.text(5.25, 4.1, '2. s, r, term, trunc, info\n   = env.step(action)',
            ha='center', fontsize=9, family='monospace', color='#2980b9')
    # 更新
    ax.text(5.25, 3.2, '3. update Q-table / policy', ha='center', fontsize=9, family='monospace')

    # 终止检查
    ax.text(5.25, 2.7, 'if terminated or truncated: break',
            ha='center', fontsize=9, family='monospace', color='#e74c3c')

    # env.close()
    close_box = mpatches.FancyBboxPatch(
        (3.5, 0.5), 3.5, 1, boxstyle="round,pad=0.2",
        facecolor='#e74c3c', alpha=0.2, edgecolor='#e74c3c', linewidth=2
    )
    ax.add_patch(close_box)
    ax.text(5.25, 1.0, 'env.close()', ha='center', fontsize=11, fontweight='bold', color='#c0392b', family='monospace')

    ax.annotate('', xy=(5.25, 1.5), xytext=(5.25, 2.3),
                arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    # --- 右图: step() 返回值 + Wrapper 概念 ---
    ax = ax2
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('step() 返回值 & Wrapper\nstep() Returns & Wrapper Concept', fontsize=12, fontweight='bold')

    # step() 返回值表
    returns = [
        ('next_state', 'int/array', '新状态 New state'),
        ('reward', 'float', '即时奖励 Immediate reward'),
        ('terminated', 'bool', '到达终止状态 Terminal state'),
        ('truncated', 'bool', '被截断 Max steps reached'),
        ('info', 'dict', '额外信息 Debug info'),
    ]

    ax.text(5, 7.5, 'env.step(action) → 5 个返回值', ha='center', fontsize=11,
            fontweight='bold', color='#2980b9')

    for i, (name, typ, desc) in enumerate(returns):
        y = 6.7 - i * 0.7
        color = '#3498db' if i < 2 else '#e74c3c' if i < 4 else '#95a5a6'
        ax.text(1, y, f'{i+1}. {name}', fontsize=10, fontweight='bold', color=color, family='monospace')
        ax.text(4.5, y, typ, fontsize=9, color='gray', family='monospace')
        ax.text(6, y, desc, fontsize=9, color='#2c3e50')

    # Wrapper 概念
    ax.plot([0.5, 9.5], [3.3, 3.3], 'k-', linewidth=0.5)
    ax.text(5, 2.8, 'Wrapper: 不修改底层代码，修改环境行为', ha='center',
            fontsize=10, fontweight='bold', color='#8e44ad')

    # Wrapper 图示
    inner = mpatches.FancyBboxPatch(
        (3, 1.0), 4, 1.2, boxstyle="round,pad=0.15",
        facecolor='#2ecc71', alpha=0.2, edgecolor='#2ecc71', linewidth=1.5
    )
    outer = mpatches.FancyBboxPatch(
        (2, 0.5), 6, 2.2, boxstyle="round,pad=0.15",
        facecolor='#8e44ad', alpha=0.1, edgecolor='#8e44ad', linewidth=1.5
    )
    ax.add_patch(outer)
    ax.add_patch(inner)
    ax.text(5, 1.6, 'Base Env', ha='center', fontsize=10, color='#27ae60', fontweight='bold')
    ax.text(5, 0.7, 'Wrapper (修改 reward / 限制步数 / ...)', ha='center', fontsize=8, color='#8e44ad')

    fig.tight_layout()
    save_fig(fig, "demo6_gymnasium_api.png")


# ============================================================
# Demo 7: 综合对比表 — 所有关键对比一图总结
# Demo 7: Comprehensive Comparison — All Key Comparisons
# ============================================================
def demo7_comprehensive_comparison():
    """
    将所有期中考试必考的对比整合到一张图中
    Consolidate all midterm-required comparisons into one figure

    必考对比 (Required Comparisons):
    - Q-Learning vs SARSA
    - V(s) vs Q(s,a)
    - Tabular Q vs DQN
    - Exploit vs Explore
    """
    print("\n📊 Demo 7: 综合对比总结")

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))

    # --- 7a: Q-Learning vs SARSA ---
    ax = axes[0, 0]
    ax.axis('off')
    ax.set_title('Q-Learning vs SARSA', fontsize=12, fontweight='bold', color='#2c3e50')

    table_data = [
        ['', 'Q-Learning', 'SARSA'],
        ['类型', 'Off-policy 离策略', 'On-policy 在策略'],
        ['更新目标', 'max Q(s\',a\')', 'Q(s\', a\'_actual)'],
        ['学习什么', '最优策略', '当前策略'],
        ['CliffWalking', '最短路径 (危险)', '安全路径 (保守)'],
        ['原因', 'max 忽略探索危险', '考虑 ε-greedy 随机性'],
    ]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    # 表头颜色
    for j in range(3):
        table[0, j].set_facecolor('#34495e')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data)):
        table[i, 0].set_facecolor('#ecf0f1')
        table[i, 0].set_text_props(fontweight='bold')

    # --- 7b: V(s) vs Q(s,a) ---
    ax = axes[0, 1]
    ax.axis('off')
    ax.set_title('V(s) vs Q(s,a)', fontsize=12, fontweight='bold', color='#2c3e50')

    table_data = [
        ['', 'V(s) 状态价值', 'Q(s,a) 动作价值'],
        ['输入', 'State only', 'State + Action'],
        ['输出', '期望回报', '期望回报'],
        ['用途', '评估状态好坏', '直接选动作'],
        ['公式', 'E[Gt | St=s]', 'E[Gt | St=s, At=a]'],
        ['位置', 'Agent 内部', 'Agent 内部'],
    ]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    for j in range(3):
        table[0, j].set_facecolor('#2980b9')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data)):
        table[i, 0].set_facecolor('#ecf0f1')
        table[i, 0].set_text_props(fontweight='bold')

    # --- 7c: Tabular Q vs DQN ---
    ax = axes[1, 0]
    ax.axis('off')
    ax.set_title('Tabular Q-Learning vs DQN', fontsize=12, fontweight='bold', color='#2c3e50')

    table_data = [
        ['', 'Tabular Q', 'DQN'],
        ['Q值存储', '表格 (dict/array)', '神经网络'],
        ['状态空间', '有限、已知', '可连续/巨大'],
        ['前提', 'S 和 A 都已知有限', '只需 A 已知'],
        ['泛化', '❌ 无', '✅ 可泛化'],
        ['内存', '随状态数线性增长', '固定网络大小'],
    ]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.5)
    for j in range(3):
        table[0, j].set_facecolor('#8e44ad')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data)):
        table[i, 0].set_facecolor('#ecf0f1')
        table[i, 0].set_text_props(fontweight='bold')

    # --- 7d: 三大子问题 ---
    ax = axes[1, 1]
    ax.axis('off')
    ax.set_title('RL 三大子问题', fontsize=12, fontweight='bold', color='#2c3e50')

    table_data = [
        ['子问题', '含义', '类比'],
        ['Exploit vs Explore', '用已知最好 vs 尝试新的', '老餐厅 vs 新餐厅'],
        ['Learning vs Planning', '真实经验 vs 模型模拟', '真吃 vs 看点评'],
        ['Prediction vs Control', '评估策略 vs 优化策略', '"多少分" vs "最高分"'],
    ]
    table = ax.table(cellText=table_data, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)
    for j in range(3):
        table[0, j].set_facecolor('#e67e22')
        table[0, j].set_text_props(color='white', fontweight='bold')
    for i in range(1, len(table_data)):
        table[i, 0].set_facecolor('#ecf0f1')
        table[i, 0].set_text_props(fontweight='bold')

    fig.suptitle('Demo 7: 期中考试必考对比总结\nMidterm Required Comparisons Summary',
                 fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save_fig(fig, "demo7_comprehensive_comparison.png")


# ============================================================
# 主程序 (Main)
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("Week 6: 期中复习完整演示 (Midterm Review Complete Demo)")
    print("=" * 60)

    demo1_rl_framework()
    demo2_bellman_equation()
    demo3_qlearning_vs_sarsa()
    demo4_epsilon_and_qtable_init()
    demo5_evolution_roadmap()
    demo6_gymnasium_api()
    demo7_comprehensive_comparison()

    print("\n" + "=" * 60)
    print(f"✅ 所有图片已保存到: {OUTPUT_DIR}")
    print("=" * 60)
