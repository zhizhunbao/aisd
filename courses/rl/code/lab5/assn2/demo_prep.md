# Assignment 2 Demo 准备

## 1. 你的状态是马尔可夫状态吗？

### 答案：**不是严格的马尔可夫状态**

当前状态定义：`Discrete(641)` — 红球中心的 **x 像素位置** (0~640)

**状态定义代码 (`041107730_aisd_examples/aisd_examples/envs/create3_red_ball.py`)：**
```python
# 观测空间: 只有一个整数 — 红球的 x 像素位置
self.observation_space = spaces.Discrete(self.IMAGE_WIDTH + 1)  # Discrete(641)

# 状态来源: listener_callback 中通过霍夫圆检测得到
self.redball_position = int(circle[0])  # 仅记录 x 坐标

# step() 返回的观测值就是这个 x 坐标
observation = self.redball.redball_position  # 一个 int，范围 0~640
```

**为什么不是马尔可夫的：**
- 马尔可夫性要求：**仅凭当前状态就能预测未来**，不需要历史信息
- 当前状态只有红球的 x 位置，**缺失了关键信息**：
  1. **红球的运动速度/方向** — 不知道球在往哪边移动、多快
  2. **机器人当前的角速度** — 不知道机器人自己在转多快
  3. **红球的 y 坐标和大小** — 不知道球的距离远近

- 例如：同样是 `x=200`，球可能在向左移动也可能在向右移动，最优动作不同

### 如何使其成为马尔可夫状态：

| 方法 | 具体做法 |
|------|---------| 
| **加入速度信息** | 状态 = `(x, dx/dt)`，用连续两帧的差分计算球的速度 |
| **帧堆叠 (Frame Stacking)** | 状态 = `(x_t, x_{t-1}, x_{t-2})`，用最近 N 帧的位置，隐式包含速度信息 |
| **加入机器人状态** | 状态 = `(x, angular_velocity)`，包含机器人自身的角速度 |
| **使用连续状态空间** | 从 `Discrete(641)` 改为 `Box`，包含 `[x, dx, robot_omega]` |

**改进代码示例（帧堆叠）：**
```python
# 改进前: 状态 = 单个 x 坐标
self.observation_space = spaces.Discrete(641)

# 改进后: 状态 = (当前x, 上一帧x) → 可以推断速度
self.observation_space = spaces.Box(
    low=np.array([0, 0]), high=np.array([640, 640]), dtype=np.float32
)
# 在 step() 中:
# velocity = current_x - previous_x  → 正=向右移动, 负=向左移动
```

> **最实用的改进**：用帧堆叠 `(x_t, x_{t-1})`，简单且有效，让 agent 能推断球的运动方向。

---

## 2. 代码工作原理

### 环境 (`CreateRedBall-v0`) — `041107730_aisd_examples/aisd_examples/envs/create3_red_ball.py`

**整体流程：**
```
摄像头图像 → HSV颜色检测 → 霍夫圆检测 → 红球 x 坐标 (状态)
                                              ↓
                              agent 选择动作 (0~640)
                                              ↓
                              动作 → Twist 角速度: (action-320)/320 * π/2
                                              ↓
                              ROS 2 发布 → Create 3 旋转
                                              ↓
                              等待轮子停止 → 读取新图像 → 新状态
```

**空间定义：**
```python
# 观测空间: 红球 x 像素位置 (0=最左, 320=中心, 640=最右)
self.observation_space = spaces.Discrete(self.IMAGE_WIDTH + 1)  # 641

# 动作空间: 映射到角速度 [-π/2, +π/2]
self.action_space = spaces.Discrete(self.IMAGE_WIDTH + 1)       # 641
```

**红球检测 (listener_callback)：**
```python
# 1. BGR → HSV 颜色空间转换
hsv_conv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# 2. 红色范围掩膜
bright_red_lower_bounds = (110, 100, 100)
bright_red_upper_bounds = (130, 255, 255)
bright_red_mask = cv2.inRange(hsv_conv_img, bright_red_lower_bounds, bright_red_upper_bounds)

# 3. 高斯模糊 + 形态学操作（去噪）
blurred_mask = cv2.GaussianBlur(bright_red_mask, (9, 9), 3, 3)
eroded_mask = cv2.erode(blurred_mask, erode_element)
dilated_mask = cv2.dilate(eroded_mask, dilate_element)

# 4. 霍夫圆检测 → 记录红球中心 x 坐标
detected_circles = cv2.HoughCircles(dilated_mask, cv2.HOUGH_GRADIENT, 1, 150,
                                     param1=100, param2=20, minRadius=2, maxRadius=2000)
if detected_circles is not None:
    self.redball_position = int(circle[0])  # 红球 x 像素位置
```

**动作执行 (RedBallNode.step)：**
```python
def step(self, action):
    twist = Twist()
    # 将离散动作转换为角速度: action=0 → 最大左转, 320 → 不转, 640 → 最大右转
    twist.angular.z = (action - 320) / 320.0 * (math.pi / 2.0)
    twist.linear.x = 0.0  # 不前进/后退
    self.twist_publisher.publish(twist)
```

**奖励函数：**
```python
def reward(self, redball_position):
    # 红球越接近中心(320)，奖励越高
    # 范围: [-1, 0]，0 = 完美居中
    distance = abs(redball_position - self.IMAGE_CENTER)
    return -(distance / self.IMAGE_CENTER)
```

**环境 step（一步交互）：**
```python
def step(self, action):
    self.step_count += 1
    self.redball.step(action)                          # 发布 Twist
    rclpy.spin_once(self.redball, timeout_sec=1.0)     # 处理 ROS 回调
    while not self.redball.create3_is_stopped:          # 等待轮子停止
        rclpy.spin_once(self.redball, timeout_sec=0.1)
    observation = self.redball.redball_position         # 读取新位置
    r = self.reward(observation)
    terminated = (self.step_count >= self.EPISODE_LENGTH)  # 100 步结束
    return observation, r, terminated, truncated, info
```

---

### Q-Learning Agent — `Assn2/qlearning.py`

```python
# Q 表初始化: 641 × 641 ≈ 411,000 个条目
Q = np.zeros((n_states, n_actions))  # n_states=641, n_actions=641

for episode in range(episodes):  # 50 回合
    state, _ = env.reset()
    while not done:
        # ε-贪心策略: 以 ε 概率随机探索，否则选 Q 值最大的动作
        if random.random() < epsilon:
            action = env.action_space.sample()          # 探索
        else:
            action = int(np.argmax(Q[state]))            # 利用

        next_state, reward, terminated, truncated, info = env.step(action)

        # Q-Learning 更新: Q(s,a) ← Q(s,a) + α[r + γ·max Q(s',a') - Q(s,a)]
        best_next = np.max(Q[next_state])
        Q[state, action] += alpha * (reward + gamma * best_next - Q[state, action])

        state = next_state

    # 衰减探索率: ε = max(0.01, ε × 0.95)
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
```
- **超参数**: α=0.1, γ=0.99, ε: 1.0→0.01 (衰减率 0.95/回合), 50 回合

---

### Non-RL Agent — `Assn2/non-rl.py`

```python
def compute_action(observation):
    """
    非 RL 策略: action = observation（直接计算，无学习）
    - 球在 x=100 (左侧) → action=100 → 向左转追球
    - 球在 x=320 (中心) → action=320 → 不转（已居中）
    - 球在 x=500 (右侧) → action=500 → 向右转追球
    """
    if int(observation) == 320:
        return 0   # 未检测到球 → 最大左转搜索
    return int(observation)

# 运行循环（无学习，纯计算）
for episode in range(50):
    observation, info = env.reset()
    while not done:
        action = compute_action(observation)
        observation, reward, terminated, truncated, info = env.step(action)
```

---

### DQN Agent — `Assn2/dqn.py` (Stable-Baselines3)

```python
from stable_baselines3 import DQN

model = DQN(
    "MlpPolicy",                          # 多层感知机策略（神经网络代替 Q 表）
    env,
    learning_rate=0.001,
    buffer_size=50000,                     # 经验回放缓冲区
    exploration_initial_eps=1.0,           # 初始探索率
    exploration_final_eps=0.05,            # 最终探索率
    exploration_fraction=0.1,              # 探索衰减比例
    verbose=1,
)
model.learn(total_timesteps=5000, callback=callback)
model.save("dqn_createredball")
```
- 用 **神经网络** 代替 Q 表，适合更大的状态/动作空间
- 包含 **经验回放** (replay buffer) 和 **目标网络**

---

### PPO Agent — `Assn2/ppo.py` (Stable-Baselines3)

```python
from stable_baselines3 import PPO

model = PPO(
    "MlpPolicy",                           # 多层感知机策略
    env,
    learning_rate=0.0003,
    n_steps=2048,                          # 每次更新的步数
    batch_size=64,
    gamma=0.99,                            # 折扣因子
    verbose=1,
)
model.learn(total_timesteps=5000, callback=callback)
model.save("ppo_createredball")
```
- **策略梯度方法**，直接优化策略（不维护 Q 表/Q 网络）
- 使用 **裁剪目标函数** 限制策略更新幅度，更稳定

---

## 3. Q-Learning vs Non-RL 图表对比讨论

### 预期图表特征

| 指标 | Q-Learning | Non-RL |
|------|-----------|--------|
| 前期 Returns | **低** (探索阶段，随机动作多) | **较高且稳定** (一开始就有合理策略) |
| 后期 Returns | **逐渐提升** (学到策略后) | **恒定** (无学习，不会改变) |
| 步数/回合 | 固定 100 步 | 固定 100 步 |
| 波动性 | **大** (探索导致) | **小** (确定性策略) |

### 讨论要点

1. **Non-RL 的优势**：
   - 不需要学习时间，**第一个回合就有好表现**
   - 策略是确定性的，**表现稳定无波动**
   - 对于这个简单问题，直接计算 `action=observation` 是一个很好的启发式

2. **Q-Learning 的特点**：
   - 初期因为 ε-贪心探索，**表现很差**（大量随机动作）
   - 随着训练推进和 ε 衰减，**逐渐学到有效策略**
   - 最终可能**接近甚至超过** Non-RL（因为它能学到更精细的映射）
   - 但 641×641 的 Q 表很大，50 回合**可能不足以充分收敛**

3. **关键结论**：
   - 对于状态→动作有**明显直接映射**的问题，Non-RL 可以很有效
   - Q-Learning 的价值在于它能**自动发现**最优策略，不需要人的领域知识
   - 但 Q-Learning **需要足够的训练时间**才能超越简单的启发式方法
